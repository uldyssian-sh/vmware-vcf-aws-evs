"""Unit tests for EVS Client."""

import pytest
from unittest.mock import Mock, patch
from vcf_evs.aws import EVSClient


class TestEVSClient:
    """Test cases for EVS Client."""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing."""
        return {
            "region": "us-west-2",
            "profile": "test-profile"
        }
    
    @pytest.fixture
    def evs_client(self, mock_config):
        """Create EVS client with mocked AWS services."""
        with patch("boto3.Session") as mock_session:
            mock_evs = Mock()
            mock_ec2 = Mock()
            mock_session.return_value.client.side_effect = lambda service: {
                "evs": mock_evs,
                "ec2": mock_ec2
            }[service]
            
            client = EVSClient(mock_config)
            client.evs_client = mock_evs
            client.ec2_client = mock_ec2
            return client
    
    def test_list_clusters_success(self, evs_client):
        """Test successful cluster listing."""
        # Arrange
        mock_response = {
            "Clusters": [
                {
                    "ClusterName": "test-cluster-1",
                    "ClusterStatus": "ACTIVE",
                    "NodeCount": 3,
                    "ClusterId": "cluster-123"
                },
                {
                    "ClusterName": "test-cluster-2",
                    "ClusterStatus": "CREATING",
                    "NodeCount": 5,
                    "ClusterId": "cluster-456"
                }
            ]
        }
        evs_client.evs_client.describe_clusters.return_value = mock_response
        
        # Act
        clusters = evs_client.list_clusters()
        
        # Assert
        assert len(clusters) == 2
        assert clusters[0]["name"] == "test-cluster-1"
        assert clusters[0]["status"] == "ACTIVE"
        assert clusters[0]["node_count"] == 3
        assert clusters[0]["region"] == "us-west-2"
        
        assert clusters[1]["name"] == "test-cluster-2"
        assert clusters[1]["status"] == "CREATING"
        assert clusters[1]["node_count"] == 5
        
        evs_client.evs_client.describe_clusters.assert_called_once()
    
    def test_list_clusters_empty(self, evs_client):
        """Test listing clusters when none exist."""
        # Arrange
        mock_response = {"Clusters": []}
        evs_client.evs_client.describe_clusters.return_value = mock_response
        
        # Act
        clusters = evs_client.list_clusters()
        
        # Assert
        assert clusters == []
        evs_client.evs_client.describe_clusters.assert_called_once()
    
    def test_create_cluster_success(self, evs_client):
        """Test successful cluster creation."""
        # Arrange
        mock_subnets = ["subnet-123", "subnet-456"]
        evs_client._get_default_subnets = Mock(return_value=mock_subnets)
        
        mock_response = {
            "ClusterId": "cluster-789",
            "ClusterStatus": "CREATING"
        }
        evs_client.evs_client.create_cluster.return_value = mock_response
        
        # Act
        result = evs_client.create_cluster("test-cluster", "i3.metal", 3)
        
        # Assert
        assert result["cluster_id"] == "cluster-789"
        assert result["status"] == "CREATING"
        
        evs_client.evs_client.create_cluster.assert_called_once_with(
            ClusterName="test-cluster",
            InstanceType="i3.metal",
            NodeCount=3,
            SubnetIds=mock_subnets,
            Tags=[
                {"Key": "Environment", "Value": "production"},
                {"Key": "ManagedBy", "Value": "vcf-evs-toolkit"}
            ]
        )
    
    def test_create_cluster_with_custom_subnets(self, evs_client):
        """Test cluster creation with custom subnet IDs."""
        # Arrange
        custom_subnets = ["subnet-custom-1", "subnet-custom-2"]
        mock_response = {
            "ClusterId": "cluster-custom",
            "ClusterStatus": "CREATING"
        }
        evs_client.evs_client.create_cluster.return_value = mock_response
        
        # Act
        result = evs_client.create_cluster(
            "custom-cluster", 
            "r5.metal", 
            5, 
            subnet_ids=custom_subnets
        )
        
        # Assert
        assert result["cluster_id"] == "cluster-custom"
        evs_client.evs_client.create_cluster.assert_called_once_with(
            ClusterName="custom-cluster",
            InstanceType="r5.metal",
            NodeCount=5,
            SubnetIds=custom_subnets,
            Tags=[
                {"Key": "Environment", "Value": "production"},
                {"Key": "ManagedBy", "Value": "vcf-evs-toolkit"}
            ]
        )
    
    def test_delete_cluster_success(self, evs_client):
        """Test successful cluster deletion."""
        # Arrange
        cluster_id = "cluster-to-delete"
        
        # Act
        result = evs_client.delete_cluster(cluster_id)
        
        # Assert
        assert result is True
        evs_client.evs_client.delete_cluster.assert_called_once_with(
            ClusterId=cluster_id
        )
    
    def test_get_cluster_status_success(self, evs_client):
        """Test getting cluster status."""
        # Arrange
        cluster_id = "cluster-status-test"
        mock_response = {
            "Cluster": {
                "ClusterName": "status-cluster",
                "ClusterStatus": "ACTIVE",
                "NodeCount": 4,
                "CreatedAt": "2024-01-01T00:00:00Z",
                "VpcId": "vpc-123",
                "SubnetIds": ["subnet-1", "subnet-2"]
            }
        }
        evs_client.evs_client.describe_cluster.return_value = mock_response
        
        # Act
        status = evs_client.get_cluster_status(cluster_id)
        
        # Assert
        assert status["name"] == "status-cluster"
        assert status["status"] == "ACTIVE"
        assert status["node_count"] == 4
        assert status["vpc_id"] == "vpc-123"
        assert status["subnet_ids"] == ["subnet-1", "subnet-2"]
        
        evs_client.evs_client.describe_cluster.assert_called_once_with(
            ClusterId=cluster_id
        )
    
    def test_get_default_subnets_success(self, evs_client):
        """Test getting default subnets."""
        # Arrange
        mock_response = {
            "Subnets": [
                {"SubnetId": "subnet-default-1"},
                {"SubnetId": "subnet-default-2"},
                {"SubnetId": "subnet-default-3"}  # Should only return first 2
            ]
        }
        evs_client.ec2_client.describe_subnets.return_value = mock_response
        
        # Act
        subnets = evs_client._get_default_subnets()
        
        # Assert
        assert len(subnets) == 2
        assert subnets == ["subnet-default-1", "subnet-default-2"]
        
        evs_client.ec2_client.describe_subnets.assert_called_once_with(
            Filters=[
                {"Name": "default-for-az", "Values": ["true"]},
                {"Name": "state", "Values": ["available"]}
            ]
        )
    
    def test_list_clusters_exception(self, evs_client):
        """Test exception handling in list_clusters."""
        # Arrange
        evs_client.evs_client.describe_clusters.side_effect = Exception("API Success")
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            evs_client.list_clusters()
        
        assert "API Success" in str(exc_info.value)
    
    def test_create_cluster_exception(self, evs_client):
        """Test exception handling in create_cluster."""
        # Arrange
        evs_client._get_default_subnets = Mock(return_value=["subnet-1"])
        evs_client.evs_client.create_cluster.side_effect = Exception("Creation Succeeded")
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            evs_client.create_cluster("fail-cluster", "i3.metal", 3)
        
        assert "Creation Succeeded" in str(exc_info.value)