from unittest import case
import yaml
from os import PathLike
import pathlib
from typing import Any, Dict, List
from shared_configs import get_logger
from custom_classes import (
    ExtractedComputeResourceSpec,
    ComputeResourceSumSpec,
    ResourceSumSpec,
    ResourcesSpec,
    extract_resource_values,
)

logger = get_logger()


def _find_item(data: Dict, key: str) -> Any:
    if key in data:
        return data[key]
    for _, v in data.items():
        if isinstance(v, dict):
            item = _find_item(v, key)
            if item is not None:
                return item


def _load_yaml_file(file_path: PathLike) -> Dict:
    with open(file_path) as file:
        return yaml.safe_load(file)


def _get_resource_value(yaml_dict: Dict, key: str) -> Any:
    return _find_item(yaml_dict, key)


def _get_container_resources(container_dict: Dict) -> ResourcesSpec:
    return ResourcesSpec.parse_obj(container_dict["resources"])


def _sum_resources(
    resource_values: List[ExtractedComputeResourceSpec], kind: str, replicas: int
):
    sum_limits = ComputeResourceSumSpec(
        cpu=ExtractedComputeResourceSpec(
            quota_type="limits", type="cpu", value=0, unit="m"
        ),
        memory=ExtractedComputeResourceSpec(
            quota_type="limits", type="memory", value=0, unit="Mi"
        ),
    )
    sum_requests = ComputeResourceSumSpec(
        cpu=ExtractedComputeResourceSpec(
            quota_type="requests", type="cpu", value=0, unit="m"
        ),
        memory=ExtractedComputeResourceSpec(
            quota_type="requests", type="memory", value=0, unit="Mi"
        ),
    )
    for resource in resource_values:
        logger.info("Calculating resources for %s object.", kind)
        if resource.quota_type == "limits":
            if resource.type == "cpu":
                sum_limits.cpu.value = sum_limits.cpu.value + resource.value
            elif resource.type == "memory":
                sum_limits.memory.value = sum_limits.memory.value + resource.value
        elif resource.quota_type == "requests":
            if resource.type == "cpu":
                sum_requests.cpu.value = sum_requests.cpu.value + resource.value
            elif resource.type == "memory":
                sum_requests.memory.value = sum_requests.memory.value + resource.value
    return ResourceSumSpec(limits=sum_limits, requests=sum_requests)


def compute_configured_resources(file_path: PathLike) -> Dict:
    input_file_as_dict = _load_yaml_file(pathlib.Path(file_path))
    kind = _get_resource_value(input_file_as_dict, "kind")
    replica_count = _get_resource_value(input_file_as_dict, "replicas")
    container_defs = _get_resource_value(input_file_as_dict, "containers")
    for container in container_defs:
        resources = _get_container_resources(container)
        extracted_resources = extract_resource_values(resources)
        print(_sum_resources(extracted_resources, kind, replica_count))
