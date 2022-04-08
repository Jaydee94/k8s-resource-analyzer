import click
import pathlib
from resource_analyzer import (
    compute_configured_resources,
)


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
def local(type, file_path) -> None:
    """
    Runs the analyzer locally.
    """
    if type == "plain":
        analyzed_workload_object = compute_configured_resources(file_path)
        print(analyzed_workload_object.total_resources)
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
