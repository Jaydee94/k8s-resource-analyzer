import yaml
from os import PathLike
import pathlib
from typing import Any, Dict, List
from shared_configs import get_logger
from custom_classes import ComputeResources, ResourcesSpec

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


def compute_configured_resources(file_path: PathLike) -> Dict:
    input_file_as_dict = _load_yaml_file(pathlib.Path(file_path))
    kind = _get_resource_value(input_file_as_dict, "kind")
    replica_count = _get_resource_value(input_file_as_dict, "replicas")
    container_defs = _get_resource_value(input_file_as_dict, "containers")
    for container in container_defs:
        resources = _get_container_resources(container)
        print(resources)
        print(resources.limits.cpu_to_decimal())
        print(resources.limits.memory_to_decimal())
        print(resources.requests.cpu_to_decimal())
        print(resources.requests.memory_to_decimal())
