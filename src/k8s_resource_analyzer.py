import json
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from resource_analyzer import (
    compute_configured_resources,
)


def _create_workload_objects_table() -> Table:
    table = Table(title="Analyzed Objects", title_justify="left")
    table.add_column("Kind", style="blue", justify="center")
    table.add_column("Replicas", style="red", justify="center")
    table.add_column("File-Path", style="green", justify="left")
    return table


def _create_total_resource_table() -> Table:
    table = Table(title="Total Resources", title_justify="left")
    table.add_column("CPU Limits", style="magenta", justify="center")
    table.add_column("CPU Requests", style="magenta", justify="center")
    table.add_column("Memory Limits", style="green", justify="center")
    table.add_column("Memory Requests", style="green", justify="center")
    return table


@click.group()
def cli() -> None:
    """
    This analyzer computes the total consumption of kubernetes workload objects.
    """


@cli.command()
@click.option(
    "--type",
    default="plain",
    help="The type of file to analyse. Possible options are [plain|helm]. Default is plain.",
    required=True,
    type=str,
)
@click.option(
    "--file-path", help="Path to the plain file or helm chart.", required=True, type=str
)
@click.option(
    "--format",
    help="The output format of the results. Possible options are [table|json]. Default is table.",
    required=True,
    type=str,
    default="table",
)
def local(type, file_path, format) -> None:
    """
    Runs the analyzer locally.
    """
    if type == "plain":
        analyzed_workload_object = compute_configured_resources(file_path)
        if format == "table":
            info_table = _create_workload_objects_table()
            total_table = _create_total_resource_table()
            console = Console()
            info_table.add_row(
                analyzed_workload_object.kind,
                str(analyzed_workload_object.replicas),
                str(Path(file_path).absolute()),
            )
            total_table.add_row(
                analyzed_workload_object.total_resources.limits.cpu,
                analyzed_workload_object.total_resources.requests.cpu,
                analyzed_workload_object.total_resources.limits.memory,
                analyzed_workload_object.total_resources.requests.memory,
            )
            console.print(info_table, justify="left")
            console.print(total_table, justify="left")
        if format == "json":
            json_workload_object = json.dumps(analyzed_workload_object.toJson())
            print(json.loads(json_workload_object))
    else:
        print("Wrong type!!!!")


@cli.command()
def cluster() -> None:
    """
    Runs the analyzer against a kubernetes cluster.
    """
    pass


if __name__ == "__main__":
    cli.add_command(local)
    cli.add_command(cluster)
    cli()
