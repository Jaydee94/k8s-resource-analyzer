from decimal import Decimal
from pydantic import BaseModel
from kubernetes.utils import parse_quantity


class ComputeResources(BaseModel):
    cpu: str
    memory: str

    def cpu_to_decimal(self) -> Decimal:
        return parse_quantity(self.cpu)

    def memory_to_decimal(self) -> Decimal:
        return parse_quantity(self.memory)


class ResourcesSpec(BaseModel):
    limits: ComputeResources
    requests: ComputeResources
