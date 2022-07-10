from typing import List
import pathlib
from typing import Dict
from k8s_resource_analyzer.shared_configs import setup_logging
from k8s_resource_analyzer.data import (
    ResourcesSpec,
    WorkloadObject,
    ComputeResources,
    decimal_to_cpu,
    decimal_to_memory,
    load_yaml_file,
    find_items,
)
from pydantic import ValidationError

logger = setup_logging()


def _get_container_resources(container_dict: Dict) -> ResourcesSpec:
    """Parse a dictionary for being a valid ResourceSpec object and return the object."""
    try:
        return ResourcesSpec.parse_obj(container_dict["resources"])
    except ValidationError as error:
        logger.error(
            "The container specification %s does not contain valid resource definitions. Reason: %s",
            container_dict,
            error,
        )


def _sum_up_resources(resources: List[ResourcesSpec], replicas: int) -> ResourcesSpec:
    """Sums up compute resources for a list of ResourceSpec objects."""
    limit_cpu_sum = 0
    limit_memory_sum = 0
    requests_cpu_sum = 0
    requests_memory_sum = 0
    for resource in resources:
        limit_cpu_sum = (limit_cpu_sum + resource.limits.cpu_to_decimal()) * replicas
        limit_memory_sum = (
            limit_memory_sum + resource.limits.memory_to_decimal()
        ) * replicas
        requests_cpu_sum = (
            requests_cpu_sum + resource.requests.cpu_to_decimal()
        ) * replicas
        requests_memory_sum = (
            requests_memory_sum + resource.requests.memory_to_decimal()
        ) * replicas
    return ResourcesSpec(
        limits=ComputeResources(
            cpu=decimal_to_cpu(limit_cpu_sum),
            memory=decimal_to_memory(limit_memory_sum),
        ),
        requests=ComputeResources(
            cpu=decimal_to_cpu(requests_cpu_sum),
            memory=decimal_to_memory(requests_memory_sum),
        ),
    )


def compute_configured_resources(file_path: str) -> WorkloadObject:
    """Create a WorkloadObject that contains type information and total contained compute resources.

    Args:
        file_path (PathLike): Path to a file containing a workload object.

    Returns:
        WorkloadObject: Contains type information and total contained compute resources.
    """
    logger.info("Sum up resources...")
    input_file_as_dict = load_yaml_file(pathlib.Path(file_path))
    kind = input_file_as_dict["kind"]
    replica_count = input_file_as_dict["spec"]["replicas"]
    container_defs = find_items(input_file_as_dict, "containers")
    resources = []
    for container_def in container_defs:
        container_spec = container_def
    for spec in container_spec:
        resources.append(_get_container_resources(spec))
    workload_object = WorkloadObject(
        kind=kind,
        replicas=replica_count,
        resource_specs=container_spec,
        total_resources=_sum_up_resources(resources, replica_count),
        file_path=file_path,
    )
    return workload_object
