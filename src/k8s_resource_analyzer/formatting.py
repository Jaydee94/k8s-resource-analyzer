from rich.table import Table
from rich.console import Console
from k8s_resource_analyzer.data import WorkloadObject
from typing import List
from pathlib import Path


def _create_workload_objects_table() -> Table:
    table = Table(title="Analyzed Objects", title_justify="left")
    table.add_column("Kind", style="blue", justify="center")
    table.add_column("Replicas", style="red", justify="center")
    table.add_column("File-Path", style="green", justify="left")
    return table


def _create_total_resource_table() -> Table:
    table = Table(title="Total Resources", title_justify="left")
    table.add_column("Kind", style="blue", justify="center")
    table.add_column("CPU Limits", style="magenta", justify="center")
    table.add_column("CPU Requests", style="magenta", justify="center")
    table.add_column("Memory Limits", style="green", justify="center")
    table.add_column("Memory Requests", style="green", justify="center")
    return table


def table_processing(
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
            analyzed_workload_object.kind,
            analyzed_workload_object.total_resources.limits.cpu,
            analyzed_workload_object.total_resources.requests.cpu,
            analyzed_workload_object.total_resources.limits.memory,
            analyzed_workload_object.total_resources.requests.memory,
        )
    console.print(info_table, justify="left")
    console.print(total_table, justify="left")


def json_processing(analyzed_workload_objects: List[WorkloadObject]) -> None:
    json = {}
    for analyzed_workload_object in analyzed_workload_objects:
        json_output = {
            key: value for key, value in analyzed_workload_object.__dict__.items()
        }
        json.update(json_output)
    print(json)
