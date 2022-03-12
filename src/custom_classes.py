from typing_extensions import Self
from pydantic import BaseModel
import re
from typing import List


class ExtractedComputeResourceSpec(BaseModel):
    quota_type: str
    type: str
    value: int
    unit: str


class ComputeResourcesSpec(BaseModel):
    cpu: str
    memory: str


class ResourcesSpec(BaseModel):
    limits: ComputeResourcesSpec
    requests: ComputeResourcesSpec


def extract_resource_values(
    resource_spec: ResourcesSpec,
) -> List[ExtractedComputeResourceSpec]:
    res = []
    for quota_type in ["limits", "requests"]:
        cpu = re.split("(\d+)", getattr(resource_spec, quota_type).cpu)
        memory = re.split("(\d+)", getattr(resource_spec, quota_type).memory)
        res.append(
            ExtractedComputeResourceSpec(
                quota_type=quota_type, type="cpu", value=cpu[1], unit=cpu[2]
            )
        )
        res.append(
            ExtractedComputeResourceSpec(
                quota_type=quota_type, type="memory", value=memory[1], unit=memory[2]
            )
        )
    return res
