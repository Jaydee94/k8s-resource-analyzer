# Idea of this project.

This application should be used as a commandline tool or ad-hoc job/container to anaylse kubernetes resource quota that are configured in a namespace.

## Cluster analyse

The application will analyse a single namespace or all namespaces inside a kubernetes cluster for configured resource quota. It compares the currently deployed kubernetes objects like `deployments stateful-sets jobs` with the resource quota for its namespace. The applications includes informations like resources for containers and replica counts or autoscalers and tells you if you configured the namespace quota properly.
The app will be able to automatically create pull requests in a repository where the deployment description is placed.

### Example

```
Deployment
    Container-A:
        resources:
            limit:
                cpu: 500m
                memory: 512Mi
            requests:
                cpu: 200m
                memory: 256Mi
        replicas: 1
HPA:
    Container-B:
        resources:
            limit:
                cpu: 500m
                memory: 512Mi
            requests:
                cpu: 200m
                memory: 256Mi
        minReplicas: 1
        maxReplicas: 3
Namespace-Resources:
    limit:
        cpu: 1
        memory: 2Gi
    requests:
        cpu: 1
        memory: 512Mi
```
In this example the configured resources would work with one pod of the deployment object and one of the autoscaler. The autoscaler would never be able to scale up pods because the confgured resources for cpu limits `1` wouldn't be enough.

## Ad-Hoc or periodic analyse.

The application can be used as a periodic or ad-hoc job that can be configured inside the repositories that should be scanned.
The repos config file should be configurable to decide which type or manifests (plain, helm etc...) should be analysed. It's also necessarry to tell the clusters e.g. multiple stages and the namespace name which should be compared to the configured resources.

Planned integrations:
- plain kubernetes yaml files
- helm 

### Example config for plain manifests

#### Repo structure

```
repo1/
    manifests/
        my-plain-kubernetes-manifests.yaml
    config-k8s-resource-bot.json
```

#### Repo config (config-k8s-resource-bot.json)

```json
{
    "type": "plain",
    "cluster": {
        "dev": {
            "namespace": "my-namespace",
            "cluster-uri": "api.my-k8s-cluster.dev.example.com",
        },
        "prod": {
            "namespace": "my-namespace",
            "cluster-uri": "api.my-k8s-cluster.prod.example.com",
        },
    },
    "manifests-path": "manifests",
}
```
