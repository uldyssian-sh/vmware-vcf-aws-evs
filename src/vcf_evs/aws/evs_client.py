"""AWS EVS Client for cluster management."""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class EVSClient:
    """AWS EVS Client for managing clusters."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize EVS client with configuration."""
        try:
            self.region = config.get("region", "us-west-2")
            
            # Validate region format
            if not self.region or not isinstance(self.region, str):
                raise ValueError("Invalid AWS region specified")
            
            self.session = boto3.Session(
                region_name=self.region,
                profile_name=config.get("profile")
            )
            self.evs_client = self.session.client("evs")
            self.ec2_client = self.session.client("ec2")
            
            logger.info(f"EVS client initialized for region: {self.region}")
            
        except (ClientError, NoCredentialsError, BotoCoreError) as e:
            logger.error(f"AWS configuration error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize EVS client: {e}")
            raise
    
    def list_clusters(self) -> List[Dict[str, Any]]:
        """List all EVS clusters."""
        try:
            response = self.evs_client.describe_clusters()
            
            return [{
                "name": cluster["ClusterName"],
                "status": cluster["ClusterStatus"],
                "node_count": cluster["NodeCount"],
                "region": self.region,
                "cluster_id": cluster["ClusterId"]
            } for cluster in response.get("Clusters", [])]
            
        except (ClientError, NoCredentialsError, BotoCoreError) as e:
            logger.error(f"AWS error listing clusters: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error listing clusters: {e}")
            raise
    
    def create_cluster(
        self, 
        name: str, 
        instance_type: str = "i3.metal", 
        size: int = 3,
        subnet_ids: Optional[List[str]] = None,
        environment: str = "development"
    ) -> Dict[str, Any]:
        """Create new EVS cluster."""
        try:
            if not subnet_ids:
                subnet_ids = self._get_default_subnets()
            
            response = self.evs_client.create_cluster(
                ClusterName=name,
                InstanceType=instance_type,
                NodeCount=size,
                SubnetIds=subnet_ids,
                Tags=[
                    {"Key": "Environment", "Value": environment},
                    {"Key": "ManagedBy", "Value": "vcf-evs-toolkit"}
                ]
            )
            
            return {
                "cluster_id": response["ClusterId"],
                "status": response["ClusterStatus"]
            }
            
        except (ClientError, NoCredentialsError, BotoCoreError) as e:
            logger.error(f"AWS error creating cluster {name}: {e}")
            raise
        except ValueError as e:
            logger.error(f"Invalid parameters for cluster {name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating cluster {name}: {e}")
            raise
    
    def delete_cluster(self, cluster_id: str) -> bool:
        """Delete EVS cluster."""
        try:
            self.evs_client.delete_cluster(ClusterId=cluster_id)
            return True
            
        except (ClientError, NoCredentialsError, BotoCoreError) as e:
            logger.error(f"AWS error deleting cluster {cluster_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error deleting cluster {cluster_id}: {e}")
            raise
    
    def get_cluster_status(self, cluster_id: str) -> Dict[str, Any]:
        """Get detailed cluster status."""
        try:
            response = self.evs_client.describe_cluster(ClusterId=cluster_id)
            cluster = response["Cluster"]
            
            return {
                "name": cluster["ClusterName"],
                "status": cluster["ClusterStatus"],
                "node_count": cluster["NodeCount"],
                "created_at": cluster["CreatedAt"],
                "vpc_id": cluster["VpcId"],
                "subnet_ids": cluster["SubnetIds"]
            }
            
        except Exception as e:
            logger.error(f"Failed to get cluster status {cluster_id}: {e}")
            raise
    
    def _get_default_subnets(self) -> List[str]:
        """Get default subnet IDs for the region."""
        try:
            response = self.ec2_client.describe_subnets(
                Filters=[
                    {"Name": "default-for-az", "Values": ["true"]},
                    {"Name": "state", "Values": ["available"]}
                ]
            )
            
            subnets = [subnet["SubnetId"] for subnet in response["Subnets"]]
            # Return at least 2 subnets for multi-AZ deployment, but allow more if available
            return subnets[:min(len(subnets), 3)]
            
        except Exception as e:
            logger.error(f"Failed to get default subnets: {e}")
            raise# Updated Sun Nov  9 12:49:45 CET 2025
# Updated Sun Nov  9 12:52:32 CET 2025
# Updated Sun Nov  9 12:56:17 CET 2025
