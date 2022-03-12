import click
import pathlib
from resource_analyzer import (
    get_replica_count,
    get_containers_definitions,
    compute_configured_resources,
)
from shared_configs import get_logger

# @click.command()
# @click.option(
#     "--type",
#     prompt="Enter the type (plain|helm)",
#     help="The type of kubernetes manifests which should be analysed (plain|helm).",
# )
# @click.option(
#     "--cluster-uri",
#     prompt="Enter the uri of the desired kubernetes cluster",
#     help="The uri of the kubernetes cluster to check for resource quota.",
# )
# @click.option(
#     "--namespace-name",
#     prompt="Enter the namespace name",
#     help="The namespace name to analyse.",
# )
# def cmd(type, cluster_uri, namespace_name):
def cmd():
    logger = get_logger()
    # logger.info(
    #     "Started with type %s in cluster %s for namespace %s",
    #     type,
    #     cluster_uri,
    #     namespace_name,
    # )
    # print(get_replica_count(input_file_as_dict))
    # print(get_containers_definitions(input_file_as_dict))
    compute_configured_resources(
        file_path="/home/jaydee/git/k8s-resource-bot/dev/test-case/example.yaml"
    )


if __name__ == "__main__":
    cmd()
