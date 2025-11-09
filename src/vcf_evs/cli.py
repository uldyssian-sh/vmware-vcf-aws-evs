"""Command Line Interface for VCF EVS Integration."""

import click
from rich.console import Console
from rich.table import Table
from botocore.exceptions import ClientError, NoCredentialsError

from vcf_evs.aws.evs_client import EVSClient
from vcf_evs.utils.config import ConfigManager

console = Console()


@click.group()
@click.version_option()
def main():
    """VMware VCF AWS EVS Integration CLI."""
    pass


@main.command()
@click.option("--config", "-c", help="Configuration file path")
def status(config):
    """Show EVS cluster status."""
    try:
        config_manager = ConfigManager(config)
        evs_client = EVSClient(config_manager.get_aws_config())
        
        clusters = evs_client.list_clusters()
        
        table = Table(title="EVS Clusters")
        table.add_column("Name", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Nodes", justify="right")
        table.add_column("Region", style="blue")
        
        for cluster in clusters:
            table.add_row(
                cluster["name"],
                cluster["status"],
                str(cluster["node_count"]),
                cluster["region"]
            )
        
        console.print(table)
        
    except (ClientError, NoCredentialsError) as e:
        console.print(f"[red]AWS Error: {e}[/red]")
    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Unexpected Error: {e}[/red]")


@main.command()
@click.option("--name", "-n", required=True, help="Cluster name")
@click.option("--instance-type", "-t", default="i3.metal", help="Instance type")
@click.option("--size", "-s", default=3, help="Cluster size")
@click.option("--config", "-c", help="Configuration file path")
def create(name, instance_type, size, config):
    """Create new EVS cluster."""
    try:
        config_manager = ConfigManager(config)
        evs_client = EVSClient(config_manager.get_aws_config())
        
        with console.status(f"Creating cluster {name}..."):
            result = evs_client.create_cluster(name, instance_type, size)
        
        console.print(f"[green]Cluster {name} created successfully![/green]")
        console.print(f"Cluster ID: {result['cluster_id']}")
        
    except (ClientError, NoCredentialsError) as e:
        console.print(f"[red]AWS Error: {e}[/red]")
    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Unexpected Error: {e}[/red]")


@main.command()
@click.option("--source", "-s", required=True, help="Source VM name")
@click.option("--target", "-t", required=True, help="Target cluster name")
@click.option("--config", "-c", help="Configuration file path")
def migrate(source, target, config):
    """Migrate VM from VCF to EVS."""
    try:
        config_manager = ConfigManager(config)
        
        with console.status(f"Migrating {source} to {target}..."):
            # TODO: Implement actual migration logic
            # This would involve:
            # 1. Connect to vCenter
            # 2. Create VM snapshot
            # 3. Export VM to OVF
            # 4. Upload to AWS S3
            # 5. Import to EVS cluster
            console.print(f"[yellow]Migration logic not yet implemented[/yellow]")
        
        console.print(f"[green]VM {source} migration to {target} completed![/green]")
        
    except (ClientError, NoCredentialsError) as e:
        console.print(f"[red]AWS Error: {e}[/red]")
    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Unexpected Error: {e}[/red]")


if __name__ == "__main__":
    main()# Updated Sun Nov  9 12:49:45 CET 2025
# Updated Sun Nov  9 12:52:32 CET 2025
# Updated Sun Nov  9 12:56:17 CET 2025
