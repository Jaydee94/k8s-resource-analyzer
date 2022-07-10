import click
from pathlib import Path
from rich.console import Console
from k8s_resource_analyzer.data import is_workload_object
from k8s_resource_analyzer.resource_analyzer import (
    compute_configured_resources,
)
from k8s_resource_analyzer.formatting import json_processing, table_processing


@click.group()
def cli() -> None:
    """
    This analyzer computes the total consumption of kubernetes workload objects.
    """


@cli.command()
@click.option(
    "--input",
    help="Path to the plain file to analyze. Can`t be used together with --path.",
    type=str,
)
@click.option(
    "--format",
    help="The output format of the results. Possible options are [table|json]. Default is table.",
    required=True,
    type=str,
    default="table",
)
def local(input: str, format: str) -> None:
    """
    Runs the analyzer locally.
    """
    console = Console()

    analyzed_workload_objects = []
    if input:
        p = Path(input).glob("**/*")
        files = [file for file in p if file.is_file() and is_workload_object(file)]
        for input in files:
            analyzed_workload_objects.append(compute_configured_resources(input))
    else:
        analyzed_workload_objects.append(compute_configured_resources(input))

    if format == "table":
        table_processing(analyzed_workload_objects, console)
    if format == "json":
        json_processing(analyzed_workload_objects)


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
