# Integration Tests

The current integration test suite requires:

- [argo cli](https://argoproj.github.io/argo/cli/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)

Star a k8s cluster using minikube:

```sh
minikube config set vm-driver docker
minikube config set kubernetes-version 1.18.3
minikube start
```

Install Argo Workflows:

```sh
kubectl create ns argo
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo/v2.11.1/manifests/quick-start-minimal.yaml
```

Run the integration tests:
```sh
scripts/integration_tests.sh
```

## Workflows

The workflows of the integration test are located in the following directory: [test/workflows](tests/workflows).

Each workflow python file must contain the following code:

```python
if __name__ == "__main__":
    wf = HelloWorld() # Workflow class to be tested
    wf_file = ntpath.basename(__file__).replace(".py", ".yaml")
    wf.to_file(f"{pathlib.Path(__file__).parent}/{wf_file}")
```