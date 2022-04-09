from decimal import Decimal
from pydantic import BaseModel
from kubernetes.utils import parse_quantity
from typing import List
import json
from dataclasses import dataclass


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

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


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
