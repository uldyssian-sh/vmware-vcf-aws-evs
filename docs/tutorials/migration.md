# VM Migration Tutorial

This comprehensive guide walks you through migrating virtual machines from on-premises VMware Cloud Foundation (VCF) to Amazon Elastic VMware Service (EVS), following official AWS best practices.

## Overview

VM migration to EVS supports multiple strategies based on your requirements:

- **Cold Migration**: VM is powered off during migration
- **Hot Migration**: Live migration with minimal downtime using vMotion
- **Bulk Migration**: Multiple VMs migrated in parallel
- **Hybrid Migration**: Gradual migration maintaining hybrid operations

## Prerequisites

### On-Premises Requirements

- [ ] **VMware vCenter** 6.7 or later with administrative access
- [ ] **ESXi hosts** version 6.7 or later
- [ ] **Network connectivity** to AWS (Direct Connect or VPN recommended)
- [ ] **VM compatibility** check completed
- [ ] **Backup verification** of source VMs

### AWS Requirements

- [ ] **EVS cluster** deployed and healthy
- [ ] **Network connectivity** configured between on-premises and EVS
- [ ] **S3 bucket** for temporary OVF storage (for cold migration)
- [ ] **IAM permissions** for EVS and S3 operations
- [ ] **vCenter credentials** for target EVS cluster

## Migration Methods

### Method 1: vMotion (Hot Migration)

Best for production workloads requiring minimal downtime.

#### Prerequisites for vMotion

Based on [AWS EVS documentation](https://docs.aws.amazon.com/pdfs/evs/latest/userguide/evs-ug.pdf):

- Layer 2 network extension between sites
- Compatible vSphere versions (6.7+ to 7.0+)
- Shared storage or vSAN stretched cluster
- Network latency < 150ms RTT

#### Step-by-Step vMotion Migration

1. **Establish Network Connectivity**
   ```bash
   # Verify network connectivity
   ping <evs-vcenter-ip>
   
   # Test vMotion network
   vmkping -I vmk1 <target-vmk-ip>
   ```

2. **Configure Cross-vCenter vMotion**
   ```bash
   # Using PowerCLI
   Connect-VIServer -Server <source-vcenter>
   Connect-VIServer -Server <evs-vcenter>
   
   # Enable Enhanced Linked Mode (if required)
   New-VICredentialStoreItem -Host <evs-vcenter> -User cloudadmin@vmc.local -Password <password>
   ```

3. **Perform vMotion Migration**
   ```bash
   # Using our CLI tool
   vcf-evs migrate \
     --source "VM-Name" \
     --target "evs-cluster-name" \
     --method vmotion \
     --config config/config.yaml
   ```

### Method 2: Cold Migration via OVF

Suitable for non-critical workloads or when vMotion is not feasible.

#### Step-by-Step Cold Migration

1. **Prepare Source VM**
   ```bash
   # Power off VM
   vcf-evs vm-power --name "VM-Name" --state off
   
   # Create pre-migration snapshot
   vcf-evs snapshot --vm "VM-Name" --description "Pre-migration backup"
   ```

2. **Export VM to OVF**
   ```bash
   # Using our migration script
   python scripts/migration/migrate_vm.py \
     --vm-name "VM-Name" \
     --target-cluster "evs-cluster" \
     --method cold \
     --config config/config.yaml
   ```

3. **Monitor Migration Progress**
   ```bash
   # Check migration status
   vcf-evs migration-status --job-id <migration-job-id>
   
   # View detailed logs
   tail -f logs/migration.log
   ```

### Method 3: Bulk Migration

For migrating multiple VMs efficiently.

#### Bulk Migration Configuration

Create a migration manifest file:

```yaml
# migration-manifest.yaml
migration:
  source_vcenter: "vcenter.onprem.local"
  target_cluster: "production-evs"
  method: "cold"  # or "vmotion"
  
  vms:
    - name: "web-server-01"
      priority: "high"
      target_datastore: "vsan-datastore"
      target_network: "VM Network"
      
    - name: "app-server-01"
      priority: "medium"
      target_datastore: "vsan-datastore"
      target_network: "App Network"
      
    - name: "db-server-01"
      priority: "high"
      target_datastore: "vsan-datastore"
      target_network: "DB Network"
      pre_migration_script: "scripts/db-prep.sh"
      post_migration_script: "scripts/db-verify.sh"

  settings:
    max_concurrent: 3
    retry_attempts: 2
    notification_email: "admin@company.com"
```

Execute bulk migration:

```bash
# Start bulk migration
python scripts/migration/bulk_migrate.py \
  --manifest migration-manifest.yaml \
  --config config/config.yaml

# Monitor progress
vcf-evs bulk-status --manifest migration-manifest.yaml
```

## Network Configuration

### Network Mapping

Configure network mapping between source and target:

```yaml
# network-mapping.yaml
network_mapping:
  source_networks:
    - name: "VM Network"
      target: "EVS-VM-Network"
      
    - name: "App-Tier"
      target: "EVS-App-Network"
      
    - name: "DB-Tier"
      target: "EVS-DB-Network"
      
  port_groups:
    - source: "Web-DMZ"
      target: "EVS-Web-DMZ"
      vlan_id: 100
```

### Security Group Configuration

Ensure proper security groups are configured:

```bash
# Create security group for migrated VMs
aws ec2 create-security-group \
  --group-name migrated-vms \
  --description "Security group for migrated VMs"

# Add rules for application traffic
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 80 \
  --cidr 10.0.0.0/8
```

## Post-Migration Validation

### Automated Validation

```bash
# Run post-migration validation
python scripts/migration/validate_migration.py \
  --vm-name "VM-Name" \
  --target-cluster "evs-cluster" \
  --config config/config.yaml
```

### Manual Validation Checklist

- [ ] **VM Power State**: Verify VM is powered on
- [ ] **Network Connectivity**: Test network access
- [ ] **Application Functionality**: Verify applications are working
- [ ] **Performance Metrics**: Compare performance with baseline
- [ ] **Backup Verification**: Ensure backup jobs are configured
- [ ] **Monitoring Setup**: Configure monitoring for migrated VM

### Validation Script Example

```python
#!/usr/bin/env python3
"""Post-migration validation script."""

import subprocess
import sys
from vcf_evs import EVSClient, ConfigManager

def validate_vm_migration(vm_name, cluster_name, config_path):
    """Validate VM migration success."""
    config = ConfigManager(config_path)
    evs_client = EVSClient(config.get_aws_config())
    
    # Check VM exists in target cluster
    vm_info = evs_client.get_vm_info(vm_name, cluster_name)
    assert vm_info['power_state'] == 'poweredOn'
    
    # Test network connectivity
    result = subprocess.run(['ping', '-c', '3', vm_info['ip_address']], 
                          capture_output=True)
    assert result.returncode == 0
    
    # Verify application ports
    for port in [80, 443, 22]:
        result = subprocess.run(['nc', '-z', vm_info['ip_address'], str(port)],
                              capture_output=True)
        if result.returncode == 0:
            print(f"Port {port} is accessible")
    
    print(f"VM {vm_name} migration validation successful")

if __name__ == "__main__":
    validate_vm_migration(sys.argv[1], sys.argv[2], sys.argv[3])
```

## Rollback Procedures

### Automatic Rollback

```bash
# Rollback using pre-migration snapshot
vcf-evs rollback \
  --vm-name "VM-Name" \
  --snapshot-id <snapshot-id> \
  --config config/config.yaml
```

### Manual Rollback Steps

1. **Power off migrated VM** in EVS cluster
2. **Revert to snapshot** on source vCenter
3. **Power on original VM** on source cluster
4. **Update DNS/load balancer** to point to original VM
5. **Clean up** migrated VM and associated resources

## Troubleshooting Common Issues

### Migration Fails with Network Error

```bash
# Check network connectivity
ping <evs-vcenter-ip>

# Verify firewall rules
aws ec2 describe-security-groups --group-ids <security-group-id>

# Test vCenter API access
curl -k https://<evs-vcenter-ip>/ui
```

### VM Won't Power On After Migration

```bash
# Check VM hardware compatibility
vcf-evs vm-info --name "VM-Name" --cluster "evs-cluster"

# Verify resource allocation
vcf-evs cluster-resources --name "evs-cluster"

# Check vSAN datastore health
vcf-evs storage-health --cluster "evs-cluster"
```

### Performance Issues After Migration

```bash
# Check VM resource allocation
vcf-evs vm-resources --name "VM-Name"

# Monitor cluster performance
vcf-evs cluster-metrics --name "evs-cluster" --duration 1h

# Verify network performance
iperf3 -c <target-ip> -t 60
```

## Best Practices

### Pre-Migration

1. **Inventory Assessment**: Document all VMs and dependencies
2. **Compatibility Check**: Verify OS and application compatibility
3. **Network Planning**: Design target network architecture
4. **Backup Strategy**: Ensure reliable backup and recovery
5. **Testing Plan**: Develop comprehensive testing procedures

### During Migration

1. **Phased Approach**: Migrate in small batches
2. **Monitoring**: Continuously monitor migration progress
3. **Communication**: Keep stakeholders informed
4. **Documentation**: Record any issues and resolutions
5. **Validation**: Test each VM after migration

### Post-Migration

1. **Performance Monitoring**: Establish baseline metrics
2. **Backup Configuration**: Set up backup jobs for migrated VMs
3. **Security Review**: Verify security configurations
4. **Cost Optimization**: Right-size resources based on usage
5. **Documentation Update**: Update infrastructure documentation

## Migration Planning Template

Use this template for planning your migrations:

```yaml
# migration-plan.yaml
project:
  name: "Production Workload Migration"
  timeline: "Q1 2024"
  stakeholders:
    - "Infrastructure Team"
    - "Application Team"
    - "Security Team"

phases:
  - name: "Phase 1 - Development VMs"
    vms: ["dev-web-01", "dev-app-01", "dev-db-01"]
    method: "cold"
    timeline: "Week 1"
    
  - name: "Phase 2 - Staging VMs"
    vms: ["stage-web-01", "stage-app-01", "stage-db-01"]
    method: "vmotion"
    timeline: "Week 2"
    
  - name: "Phase 3 - Production VMs"
    vms: ["prod-web-01", "prod-app-01", "prod-db-01"]
    method: "vmotion"
    timeline: "Week 3"
    maintenance_window: "Saturday 2AM-6AM"

success_criteria:
  - "Zero data loss"
  - "< 4 hours downtime per VM"
  - "Application performance within 5% of baseline"
  - "All security controls maintained"

rollback_plan:
  trigger_conditions:
    - "Migration time exceeds 6 hours"
    - "Application performance degrades > 20%"
    - "Data integrity issues detected"
  
  procedures:
    - "Power off migrated VM"
    - "Revert to pre-migration snapshot"
    - "Update DNS records"
    - "Notify stakeholders"
```

## Official Resources

- **[AWS EVS User Guide (PDF)](https://docs.aws.amazon.com/pdfs/evs/latest/userguide/evs-ug.pdf)** - Migration best practices
- **[VMware vMotion Documentation](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.vcenterhost.doc/GUID-8B6B8A0A-1B0C-4F0C-8B0A-1B0C4F0C8B0A.html)** - vMotion requirements
- **[AWS Direct Connect](https://aws.amazon.com/directconnect/)** - Network connectivity options
- **[Re:Invent 2024 Migration Session](https://reinvent.awsevents.com/content/dam/reinvent/2024/slides/mam/MAM237-NEW_Deep-dive-into-Amazon-Elastic-VMware-Service.pdf)** - Migration strategies

## Next Steps

After successful migration:

1. **[Set up monitoring](monitoring.md)** for your migrated workloads
2. **[Configure backup](backup.md)** and disaster recovery
3. **[Optimize costs](../architecture/cost-optimization.md)** based on usage patterns
4. **[Review security](../architecture/security.md)** configurations