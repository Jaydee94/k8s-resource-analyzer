import yaml
from os import PathLike
from typing import Any, Dict, List
from shared_configs import get_logger

logger = get_logger()

def _finditem(data: Dict, key: str) -> Any:
    if key in data: return data[key]
    for _, v in data.items():
        if isinstance(v,dict):
            item = _finditem(v, key)
            if item is not None:
                return item

def get_replica_count(file_path: PathLike) -> int:
    with open(file_path) as file:
        loaded_yaml = yaml.safe_load(file)
        return _finditem(data=loaded_yaml, key="replicas")

def get_containers_definitions(file_path: PathLike) -> List[Dict]:
    with open(file_path) as file:
        loaded_yaml = yaml.safe_load(file)
        return _finditem(data=loaded_yaml, key="containers")