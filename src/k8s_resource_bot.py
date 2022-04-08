from re import A
import click
import pathlib
from resource_analyzer import (
    compute_configured_resources,
)

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
    # logger.info(
    #     "Started with type %s in cluster %s for namespace %s",
    #     type,
    #     cluster_uri,
    #     namespace_name,
    # )
    analyzed_workload_object = compute_configured_resources(
        file_path=pathlib.Path(
            "/home/jaydee/git/k8s-resource-bot/dev/test-case/example.yaml"
        )
    )
    print(analyzed_workload_object.total_resources)


if __name__ == "__main__":
    cmd()
