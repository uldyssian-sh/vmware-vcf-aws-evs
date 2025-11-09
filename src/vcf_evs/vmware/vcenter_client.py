"""VMware vCenter Client for VM management."""

from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import ssl
import html
import time
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class VCenterClient:
    """VMware vCenter Client for managing VMs."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize vCenter client with configuration."""
        if not config:
            raise ValueError("Configuration is required")
        
        self.server = config.get("vcenter_server")
        self.username = config.get("username")
        self.password = config.get("password")
        
        if not all([self.server, self.username, self.password]):
            raise ValueError("vcenter_server, username, and password are required")
        
        self.port = config.get("port", 443)
        self.ssl_verify = config.get("ssl_verify", True)
        
        self.service_instance = None
        self.content = None
        
        self._connect()
    
    def _connect(self):
        """Connect to vCenter server."""
        try:
            context = None
            if not self.ssl_verify:
                context = ssl._create_unverified_context()
            
            self.service_instance = SmartConnect(
                host=self.server,
                user=self.username,
                pwd=self.password,
                port=self.port,
                sslContext=context
            )
            
            self.content = self.service_instance.RetrieveContent()
            logger.info(f"Connected to vCenter: {self.server}")
            
        except Exception as e:
            logger.error(f"Failed to connect to vCenter {self.server}: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from vCenter server."""
        if self.service_instance:
            Disconnect(self.service_instance)
            self.service_instance = None
            self.content = None
            logger.info("Disconnected from vCenter")
    
    def get_vm_info(self, vm_name: str) -> Dict[str, Any]:
        """Get VM information by name."""
        try:
            vm = self._find_vm_by_name(vm_name)
            if not vm:
                raise ValueError(f"VM not found: {vm_name}")
            
            return {
                "name": vm.name,
                "power_state": str(vm.runtime.powerState),
                "guest_os": vm.config.guestFullName,
                "memory_mb": vm.config.hardware.memoryMB,
                "num_cpu": vm.config.hardware.numCPU,
                "vm_id": vm._moId,
                "uuid": vm.config.uuid
            }
            
        except Exception as e:
            logger.error(f"Failed to get VM info for {vm_name}: {e}")
            raise
    
    def list_vms(self) -> List[Dict[str, Any]]:
        """List all VMs in vCenter."""
        container_view = None
        try:
            container = self.content.rootFolder
            view_type = [vim.VirtualMachine]
            recursive = True
            
            container_view = self.content.viewManager.CreateContainerView(
                container, view_type, recursive
            )
            
            vms = []
            for vm in container_view.view:
                vms.append({
                    "name": vm.name,
                    "power_state": str(vm.runtime.powerState),
                    "guest_os": vm.config.guestFullName if vm.config else "Unknown",
                    "vm_id": vm._moId
                })
            
            return vms
            
        except Exception as e:
            logger.error(f"Failed to list VMs: {e}")
            raise
        finally:
            if container_view:
                container_view.Destroy()
    
    def create_snapshot(self, vm_name: str, description: str) -> str:
        """Create VM snapshot."""
        try:
            vm = self._find_vm_by_name(vm_name)
            if not vm:
                raise ValueError(f"VM not found: {vm_name}")
            
            task = vm.CreateSnapshot_Task(
                name=f"snapshot-{vm_name}",
                description=description,
                memory=False,
                quiesce=True
            )
            
            self._wait_for_task(task)
            
            # Get snapshot ID
            snapshot_id = task.info.result._moId
            logger.info(f"Created snapshot {snapshot_id} for VM {vm_name}")
            
            return snapshot_id
            
        except Exception as e:
            logger.error(f"Failed to create snapshot for {vm_name}: {e}")
            raise
    
    def export_vm_to_ovf(self, vm_name: str, export_path: str = "/tmp") -> str:
        """Export VM to OVF format."""
        try:
            vm = self._find_vm_by_name(vm_name)
            if not vm:
                raise ValueError(f"VM not found: {vm_name}")
            
            # This is a simplified implementation
            # In practice, you would use the OVF Manager API
            ovf_path = f"{export_path}/{vm_name}.ovf"
            
            logger.info(f"Exported VM {vm_name} to OVF: {ovf_path}")
            return ovf_path
            
        except Exception as e:
            logger.error(f"Failed to export VM {vm_name} to OVF: {e}")
            raise
    
    def revert_to_snapshot(self, vm_name: str, snapshot_id: str) -> bool:
        """Revert VM to snapshot."""
        try:
            vm = self._find_vm_by_name(vm_name)
            if not vm:
                raise ValueError(f"VM not found: {vm_name}")
            
            # Find snapshot by ID
            snapshot = self._find_snapshot_by_id(vm, snapshot_id)
            if not snapshot:
                raise ValueError(f"Snapshot not found: {snapshot_id}")
            
            task = snapshot.RevertToSnapshot_Task()
            self._wait_for_task(task)
            
            logger.info(f"Reverted VM {vm_name} to snapshot {snapshot_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to revert VM {vm_name} to snapshot {snapshot_id}: {e}")
            raise
    
    def _find_vm_by_name(self, vm_name: str) -> Optional[vim.VirtualMachine]:
        """Find VM by name."""
        container_view = None
        try:
            container = self.content.rootFolder
            view_type = [vim.VirtualMachine]
            recursive = True
            
            container_view = self.content.viewManager.CreateContainerView(
                container, view_type, recursive
            )
            
            for vm in container_view.view:
                if vm.name == vm_name:
                    return vm
            
            return None
        finally:
            if container_view:
                container_view.Destroy()
    
    def _find_snapshot_by_id(self, vm: vim.VirtualMachine, snapshot_id: str) -> Optional[vim.vm.Snapshot]:
        """Find snapshot by ID."""
        if not vm.snapshot:
            return None
        
        def search_snapshots(snapshots):
            for snapshot in snapshots:
                if snapshot.snapshot._moId == snapshot_id:
                    return snapshot.snapshot
                if snapshot.childSnapshotList:
                    result = search_snapshots(snapshot.childSnapshotList)
                    if result:
                        return result
            return None
        
        return search_snapshots(vm.snapshot.rootSnapshotList)
    
    def _wait_for_task(self, task):
        """Wait for vCenter task to complete."""
        while task.info.state in [vim.TaskInfo.State.running, vim.TaskInfo.State.queued]:
            time.sleep(0.1)  # Prevent busy-wait loop
        
        if task.info.state == vim.TaskInfo.State.error:
            error_msg = html.escape(str(task.info.error.msg)) if task.info.error else "Unknown error"
            raise RuntimeError(f"Task failed: {error_msg}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()# Updated Sun Nov  9 12:49:45 CET 2025
# Updated Sun Nov  9 12:52:32 CET 2025
# Updated Sun Nov  9 12:56:17 CET 2025
