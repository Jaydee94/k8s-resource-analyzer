from decimal import Decimal
from pydantic import BaseModel
from kubernetes.utils import parse_quantity
from typing import List, Dict, Iterable
from os import PathLike
from dataclasses import dataclass
import yaml


class ComputeResources(BaseModel):
    cpu: str
    memory: str

    def cpu_to_decimal(self) -> Decimal:
        return parse_quantity(self.cpu).normalize()

    def memory_to_decimal(self) -> Decimal:
        return parse_quantity(self.memory).normalize()


class ResourcesSpec(BaseModel):
    limits: ComputeResources
    requests: ComputeResources


@dataclass
class WorkloadObject:
    kind: str
    replicas: str
    resource_specs: List[ResourcesSpec]
    total_resources: ResourcesSpec
    file_path: str


def decimal_to_cpu(value: Decimal) -> str:
    val = f"{value * 1000}".split(".")[0]
    return f"{val}m"


def decimal_to_memory(value: Decimal) -> str:
    unit = {
        1: "Bi",
        2: "Mi",
        3: "Gi",
        4: "Ti",
    }
    count = 0
    while value > 1024:
        value = round(value / 1024, 2)
        count = count + 1
    return f"{value}{unit[count]}"


def find_items(object: Dict, search_value: str) -> Iterable:
    """Recusively find a key inside a given dict."""
    if isinstance(object, list):
        for i in object:
            for x in find_items(i, search_value):
                yield x
    elif isinstance(object, dict):
        if search_value in object:
            yield object[search_value]
        for j in object.values():
            for x in find_items(j, search_value):
                yield x


def load_yaml_file(file_path: PathLike) -> Dict:
    """Load a yaml file from a provided path and return its content as a dictionary."""
    with open(file_path) as file:
        return yaml.safe_load(file)


def is_workload_object(file: PathLike) -> bool:
    workload_kinds = [
        "Deployment",
        "StatefulSet",
        "DaemonSet",
        "Pod",
        "ReplicaSet",
        "Job",
        "CronJob",
        "ReplicationController",
    ]
    yaml_file = load_yaml_file(file)
    if yaml_file["kind"] in workload_kinds:
        return True
    return False
