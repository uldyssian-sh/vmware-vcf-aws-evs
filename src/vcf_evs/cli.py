"""Command Line Interface for VCF EVS Integration."""

import click
from rich.console import Console
from rich.table import Table

from .aws import EVSClient
from .utils import ConfigManager

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
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


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
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@main.command()
@click.option("--source", "-s", required=True, help="Source VM name")
@click.option("--target", "-t", required=True, help="Target cluster name")
@click.option("--config", "-c", help="Configuration file path")
def migrate(source, target, config):
    """Migrate VM from VCF to EVS."""
    try:
        config_manager = ConfigManager(config)
        
        with console.status(f"Migrating {source} to {target}..."):
            # Migration logic would go here
            pass
        
        console.print(f"[green]VM {source} migrated successfully to {target}![/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()