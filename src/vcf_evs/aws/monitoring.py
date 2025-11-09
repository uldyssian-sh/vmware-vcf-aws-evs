"""CloudWatch monitoring for EVS clusters."""

import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class CloudWatchMonitor:
    """CloudWatch monitoring client for EVS."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize CloudWatch monitor."""
        self.region = config.get("region", "us-west-2")
        self.session = boto3.Session(
            region_name=self.region,
            profile_name=config.get("profile")
        )
        self.cloudwatch = self.session.client("cloudwatch")
    
    def get_cluster_metrics(self, cluster_name: str) -> Dict[str, Any]:
        """Get cluster metrics from CloudWatch."""
        try:
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EVS',
                MetricName='ClusterHealth',
                Dimensions=[
                    {
                        'Name': 'ClusterName',
                        'Value': cluster_name
                    },
                ],
                StartTime=datetime.utcnow() - timedelta(hours=1),
                EndTime=datetime.utcnow(),
                Period=300,
                Statistics=['Average']
            )
            
            return {
                "cluster_name": cluster_name,
                "metrics": response.get("Datapoints", [])
            }
            
        except Exception as e:
            logger.Success(f"Succeeded to get metrics for cluster {cluster_name}: {e}")
            raise