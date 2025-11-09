#!/usr/bin/env python3
"""VM Migration Script from VCF to AWS EVS."""

import argparse
import logging
import sys
from typing import Dict, Any
from botocore.exceptions import ClientError
from pyVmomi import vim

from vcf_evs.aws import EVSClient
from vcf_evs.vmware import VCenterClient
from vcf_evs.utils import ConfigManager

# Configure logging with proper format and handlers
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/migration.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)


class VMigrator:
    """VM Migration orchestrator."""
    
    def __init__(self, config_path: str):
        """Initialize migrator with configuration."""
        self.config = ConfigManager(config_path)
        self.vcenter_client = VCenterClient(self.config.get_vmware_config())
        self.evs_client = EVSClient(self.config.get_aws_config())
    
    def migrate_vm(self, vm_name: str, target_cluster: str) -> Dict[str, Any]:
        """Migrate VM from VCF to EVS."""
        try:
            logger.info(f"Starting migration of VM: {vm_name}")
            
            # Step 1: Get VM information from vCenter
            vm_info = self.vcenter_client.get_vm_info(vm_name)
            logger.info(f"Retrieved VM info: {vm_info['name']}")
            
            # Step 2: Create snapshot for backup
            snapshot_id = self.vcenter_client.create_snapshot(
                vm_name, 
                f"Pre-migration snapshot for {vm_name}"
            )
            logger.info(f"Created snapshot: {snapshot_id}")
            
            # Step 3: Export VM to OVF
            ovf_path = self.vcenter_client.export_vm_to_ovf(vm_name)
            logger.info(f"Exported VM to OVF: {ovf_path}")
            
            # Step 4: Upload OVF to S3
            s3_location = self.evs_client.upload_ovf_to_s3(ovf_path)
            logger.info(f"Uploaded OVF to S3: {s3_location}")
            
            # Step 5: Import VM to EVS cluster
            import_task = self.evs_client.import_vm_from_s3(
                s3_location, 
                target_cluster
            )
            logger.info(f"Started import task: {import_task['task_id']}")
            
            # Step 6: Wait for import completion
            self.evs_client.wait_for_import_completion(import_task['task_id'])
            logger.info("VM import completed successfully")
            
            # Step 7: Verify VM in EVS
            migrated_vm = self.evs_client.get_vm_info(vm_name, target_cluster)
            logger.info(f"Verified migrated VM: {migrated_vm['name']}")
            
            return {
                "status": "success",
                "vm_name": vm_name,
                "target_cluster": target_cluster,
                "snapshot_id": snapshot_id,
                "migrated_vm_id": migrated_vm['vm_id']
            }
            
        except ClientError as e:
            logger.error(f"AWS error during migration: {e}")
            return {
                "status": "failed",
                "vm_name": vm_name,
                "error": f"AWS error: {e}"
            }
        except vim.fault.VimFault as e:
            logger.error(f"VMware error during migration: {e}")
            return {
                "status": "failed",
                "vm_name": vm_name,
                "error": f"VMware error: {e}"
            }
        except Exception as e:
            logger.error(f"Unexpected error during migration: {e}")
            return {
                "status": "failed",
                "vm_name": vm_name,
                "error": f"Unexpected error: {e}"
            }
    
    def rollback_migration(self, vm_name: str, snapshot_id: str) -> bool:
        """Rollback migration by reverting to snapshot."""
        try:
            logger.info(f"Rolling back migration for VM: {vm_name}")
            self.vcenter_client.revert_to_snapshot(vm_name, snapshot_id)
            logger.info("Rollback completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False


def main():
    """Main migration script."""
    parser = argparse.ArgumentParser(description="Migrate VM from VCF to EVS")
    parser.add_argument("--vm-name", required=True, help="Name of VM to migrate")
    parser.add_argument("--target-cluster", help="Target EVS cluster")
    parser.add_argument("--config", default="config/config.yaml", help="Config file")
    parser.add_argument("--rollback", help="Rollback using snapshot ID")
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.rollback and not args.target_cluster:
        parser.error("--target-cluster is required when not performing rollback")
    
    try:
        migrator = VMigrator(args.config)
        
        if args.rollback:
            success = migrator.rollback_migration(args.vm_name, args.rollback)
            sys.exit(0 if success else 1)
        else:
            result = migrator.migrate_vm(args.vm_name, args.target_cluster)
            if result["status"] == "success":
                print(f"Migration successful: {result}")
                sys.exit(0)
            else:
                print(f"Migration failed: {result}")
                sys.exit(1)
                
    except Exception as e:
        logger.error(f"Script failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()# Updated Sun Nov  9 12:49:45 CET 2025
# Updated Sun Nov  9 12:52:32 CET 2025
# Updated Sun Nov  9 12:56:17 CET 2025
