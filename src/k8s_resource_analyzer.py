import json
import click
from pathlib import Path
from typing import List
from rich.console import Console
from rich.table import Table
from rich.text import Text
from data import WorkloadObject, is_workload_object
from resource_analyzer import (
    compute_configured_resources,
)


def _create_workload_objects_table() -> Table:
    table = Table(title="Analyzed Objects", title_justify="left")
    table.add_column("Kind", style="blue", justify="center")
    table.add_column("Replicas", style="red", justify="center")
    table.add_column("File-Path", style="green", justify="left")
    return table


def _table_processing(
    analyzed_workload_objects: List[WorkloadObject], console: Console
) -> None:
    info_table = _create_workload_objects_table()
    total_table = _create_total_resource_table()
    for analyzed_workload_object in analyzed_workload_objects:
        info_table.add_row(
            analyzed_workload_object.kind,
            str(analyzed_workload_object.replicas),
            str(Path(analyzed_workload_object.file_path).absolute()),
        )
        total_table.add_row(
            analyzed_workload_object.total_resources.limits.cpu,
            analyzed_workload_object.total_resources.requests.cpu,
            analyzed_workload_object.total_resources.limits.memory,
            analyzed_workload_object.total_resources.requests.memory,
        )
    console.print(info_table, justify="left")
    console.print(total_table, justify="left")


def _create_total_resource_table() -> Table:
    table = Table(title="Total Resources", title_justify="left")
    table.add_column("CPU Limits", style="magenta", justify="center")
    table.add_column("CPU Requests", style="magenta", justify="center")
    table.add_column("Memory Limits", style="green", justify="center")
    table.add_column("Memory Requests", style="green", justify="center")
    return table


def _json_processing(analyzed_workload_objects: List[WorkloadObject]) -> None:
    for analyzed_workload_object in analyzed_workload_objects:
        json_workload_object = json.dumps(analyzed_workload_object.toJson())
        print(json.loads(json_workload_object))


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
    "--file",
    help="Path to the plain file to analyze. Can`t be used together with --path.",
    type=str,
)
@click.option(
    "--path",
    help="A path that should be searched for workload objects. Can`t be used together with --file.",
    type=str,
)
@click.option(
    "--format",
    help="The output format of the results. Possible options are [table|json]. Default is table.",
    required=True,
    type=str,
    default="table",
)
def local(type: str, file: str, path: str, format: str) -> None:
    """
    Runs the analyzer locally.
    """
    console = Console()
    if (not file and not path) or (file and path):
        text = Text("Invalid Arguments: Either choose --file or --path.")
        text.stylize("bold red")
        console.print(text)
        exit(1)

    if type == "plain":
        analyzed_workload_objects = []
        if path:
            p = Path(path).glob("**/*")
            files = [file for file in p if file.is_file() and is_workload_object(file)]
            for file in files:
                analyzed_workload_objects.append(compute_configured_resources(file))
        else:
            analyzed_workload_objects.append(compute_configured_resources(file))

        if format == "table":
            _table_processing(analyzed_workload_objects, console)
        if format == "json":
            _json_processing(analyzed_workload_objects)
    else:
        print("Not yet.")


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
