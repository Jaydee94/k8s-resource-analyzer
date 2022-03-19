import yaml
from decimal import Decimal
from os import PathLike
import pathlib
from typing import Any, Dict
from shared_configs import get_logger
from data import ResourcesSpec, decimal_to_cpu, _to_memory_quantity
from pydantic import ValidationError

logger = get_logger()


def _find_item(data: Dict, key: str) -> Any:
    """Search for a key in a dictionary an return its value."""
    if key in data:
        return data[key]
    for _, v in data.items():
        if isinstance(v, dict):
            item = _find_item(v, key)
            if item is not None:
                return item


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


def compute_configured_resources(file_path: PathLike) -> Dict:
    input_file_as_dict = _load_yaml_file(pathlib.Path(file_path))
    kind = _find_item(input_file_as_dict, "kind")
    replica_count = _find_item(input_file_as_dict, "replicas")
    container_defs = _find_item(input_file_as_dict, "containers")
    for container in container_defs:
        resources = _get_container_resources(container)
