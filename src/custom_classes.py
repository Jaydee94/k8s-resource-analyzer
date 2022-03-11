from pydantic import BaseModel


class ComputeResourcesSpec(BaseModel):
    cpu: str
    memory: str

class ResourcesSpec(BaseModel):
    limits: ComputeResourcesSpec
    requests: ComputeResourcesSpec
