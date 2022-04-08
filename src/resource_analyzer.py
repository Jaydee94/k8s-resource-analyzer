import logging
from typing import Iterable, List
from decimal import Decimal
import yaml
from os import PathLike
import pathlib
from typing import Dict
from shared_configs import setup_logging
from data import (
    ResourcesSpec,
    WorkloadObject,
    ComputeResources,
    decimal_to_cpu,
    decimal_to_memory,
)
from pydantic import ValidationError

logger = setup_logging()


def _find_items(object: Dict, search_value: str) -> Iterable:
    """Recusively find a key inside a given dict."""
    if isinstance(object, list):
        for i in object:
            for x in _find_items(i, search_value):
                yield x
    elif isinstance(object, dict):
        if search_value in object:
            yield object[search_value]
        for j in object.values():
            for x in _find_items(j, search_value):
                yield x


def _load_yaml_file(file_path: PathLike) -> Dict:
    """Load a yaml file from a provided path and return its content as a dictionary."""
    with open(file_path) as file:
        return yaml.safe_load(file)


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


def _sum_up_resources(resources: List[ResourcesSpec]) -> ResourcesSpec:
    """Sums up compute resources for a list of ResourceSpec objects."""
    limit_cpu_sum = Decimal(0)
    limit_memory_sum = 0
    requests_cpu_sum = 0
    requests_memory_sum = 0
    for resource in resources:
        limit_cpu_sum = limit_cpu_sum + resource.limits.cpu_to_decimal()
        limit_memory_sum = limit_memory_sum + resource.limits.memory_to_decimal()
        requests_cpu_sum = requests_cpu_sum + resource.limits.cpu_to_decimal()
        requests_memory_sum = requests_memory_sum + resource.limits.memory_to_decimal()
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


def compute_configured_resources(file_path: PathLike) -> WorkloadObject:
    """Create a WorkloadObject that contains type information and total contained compute resources.

    Args:
        file_path (PathLike): Path to a file containing a workload object.

    Returns:
        WorkloadObject: Contains type information and total contained compute resources.
    """
    logger.info("Sum up resources...")
    input_file_as_dict = _load_yaml_file(pathlib.Path(file_path))
    kind = input_file_as_dict["kind"]
    replica_count = input_file_as_dict["spec"]["replicas"]
    container_defs = _find_items(input_file_as_dict, "containers")
    resources = []
    for container_def in container_defs:
        container_spec = container_def
    for spec in container_spec:
        resources.append(_get_container_resources(spec))
    workload_object = WorkloadObject(
        kind=kind,
        replicas=replica_count,
        resource_specs=container_spec,
        total_resources=_sum_up_resources(resources),
    )
    return workload_object
