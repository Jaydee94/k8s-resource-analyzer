import yaml
from os import PathLike
import pathlib
from typing import Any, Dict, List
from shared_configs import get_logger
from custom_classes import ResourcesSpec, extract_resource_values

logger = get_logger()


def _find_item(data: Dict, key: str) -> Any:
    if key in data:
        return data[key]
    for _, v in data.items():
        if isinstance(v, dict):
            item = _find_item(v, key)
            if item is not None:
                return item


def load_yaml_file(file_path: PathLike) -> Dict:
    with open(file_path) as file:
        return yaml.safe_load(file)


def get_replica_count(yaml_dict: Dict) -> int:
    return _find_item(data=yaml_dict, key="replicas")


def get_containers_definitions(yaml_dict: Dict) -> List[Dict]:
    return _find_item(data=yaml_dict, key="containers")


def _get_container_resources(container_dict: Dict) -> ResourcesSpec:
    return ResourcesSpec.parse_obj(container_dict["resources"])


def compute_configured_resources(file_path: PathLike) -> Dict:
    input_file_as_dict = load_yaml_file(pathlib.Path(file_path))
    replica_count = get_replica_count(input_file_as_dict)
    container_defs = get_containers_definitions(input_file_as_dict)
    for container in container_defs:
        resources = _get_container_resources(container)
        extracted_resources = extract_resource_values(resources)
        for extracted_resource in extracted_resources:
            print(extracted_resource)
