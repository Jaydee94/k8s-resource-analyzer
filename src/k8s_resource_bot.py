import click
import logging
import json_logging
import sys


def get_logger():
    json_logging.init_non_web(enable_json=True)
    logger = logging.getLogger("main")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger


@click.command()
@click.option(
    "--type",
    prompt="Enter the type (plain|helm)",
    help="The type of kubernetes manifests which should be analysed (plain|helm).",
)
@click.option(
    "--cluster-uri",
    prompt="Enter the uri of the desired kubernetes cluster",
    help="The uri of the kubernetes cluster to check for resource quota.",
)
@click.option(
    "--namespace-name",
    prompt="Enter the namespace name",
    help="The namespace name to analyse.",
)
def cmd(type, cluster_uri, namespace_name):
    logger = get_logger()
    logger.info(
        "Started with type %s in cluster %s for namespace %s",
        type,
        cluster_uri,
        namespace_name,
    )


if __name__ == "__main__":
    cmd()
