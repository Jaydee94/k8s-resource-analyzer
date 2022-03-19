from decimal import Decimal
from pydantic import BaseModel
from kubernetes.utils import parse_quantity


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


def decimal_to_cpu(value: Decimal) -> str:
    val = f"{value * 1000}".split(".")[0]
    return f"{val}m"


def _to_memory_quantity(value: Decimal) -> str:
    unit = {
        1: "Bi",
        2: "Mi",
        3: "Gi",
        4: "Ti",
    }
    count = 0
    while value > 1024:
        value = value / 1024
        count = count + 1
    return f"{value}{unit[count]}"
