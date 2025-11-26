# DevOps Portfolio Project — Python Flask App (CI/CD + Jenkins + GitHub Actions + Kubernetes + Monitoring)

**What this repo contains**
- A simple Python Flask web app with a health endpoint and Prometheus metrics.
- Dockerfile to build the app image.
- Jenkinsfile (Declarative) and GitHub Actions workflow for CI/CD.
- Helm chart for Kubernetes deployment.
- Kubernetes manifests and ServiceMonitor for Prometheus scraping.
- Automation scripts (cleanup, simple monitor).
- Step-by-step README sections below.

---

## Quick architecture summary
1. Developer pushes code to GitHub.
2. GitHub Actions runs CI (tests, lint, build) and can publish image to Docker registry.
3. Jenkins demonstrates a CD pipeline (optional) that can build and deploy to Kubernetes.
4. Deployment target: **Minikube** cluster using **Helm** charts.
5. Observability: **Prometheus + Grafana** (deployed to Minikube) with ServiceMonitor scraping the Flask app metrics.

---

## Files & folders
- `app/` : Flask application
- `Dockerfile`
- `requirements.txt`
- `Jenkinsfile`
- `.github/workflows/ci.yml`
- `helm-chart/` : Helm chart to deploy app
- `k8s/` : Kubernetes manifests (namespace, service, servicemonitor)
- `scripts/` : helper automation scripts
- `README.md` (this file)

---

## Run locally with Minikube (recommended for evaluation)
1. Install minikube, kubectl, helm, docker.
2. Start minikube:
   ```bash
   minikube start --driver=docker
   eval $(minikube -p minikube docker-env)
   ```
   The `eval` step ensures Docker builds are available to minikube.

3. Build the Docker image locally (example):
   ```bash
   docker build -t devops-portfolio-flask:latest .
   ```

4. Install Prometheus + Grafana (kube-prometheus-stack):
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
   ```

5. Deploy the app using Helm chart:
   ```bash
   helm install devops-flask helm-chart --namespace devops --create-namespace
   ```

6. Check pods and services:
   ```bash
   kubectl get pods -n devops
   kubectl get svc -n devops
   ```

7. Access Grafana (port-forward) and add Prometheus as data source if needed:
   ```bash
   kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090
   kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80
   # Grafana default user: admin, password: prom-operator (may vary)
   ```

---

## CI/CD (notes)
- **GitHub Actions** workflow included at `.github/workflows/ci.yml`. It runs linters, unit tests and builds Docker image. To push images to Docker Hub or GitHub Container Registry, add repo secrets:
  - `DOCKER_USERNAME`
  - `DOCKER_PASSWORD`
  - `IMAGE_NAME` (optional)

- **Jenkinsfile** demonstrates a declarative pipeline that:
  - Checks out code
  - Runs tests
  - Builds Docker image
  - Pushes image (requires credentials setup in Jenkins: dockerHubCreds)

---

## Monitoring
- The Flask app exposes Prometheus metrics at `/metrics` using `prometheus_client`.
- A `ServiceMonitor` manifest is provided in `k8s/` (requires Prometheus Operator — provided by kube-prometheus-stack).
- Grafana dashboards can be added; sample PromQL queries suggested in `README`.

---

## Mapping to skills (for CV / Interview)
- **CI/CD**: GitHub Actions + Jenkinsfile show continuous integration and deployment pipelines.
- **Scripting & Automation**: scripts in `scripts/` (cleanup, monitor) and Docker/Helm templates automate ops tasks.
- **Cloud & Containerisation**: Dockerfile + Helm + Kubernetes manifests show containerized deployment.
- **Problem-solving & Collaboration**: README documents decisions and troubleshooting steps you took.

---

## Next steps / Customization
- Hook Jenkins to your GitHub repo and install necessary plugins (Kubernetes CLI, Docker pipeline).
- Configure GitHub Actions to publish to GHCR or Docker Hub using repository secrets.
- Add Ingress / TLS via cert-manager for exposing the app externally.

---

If you want, I packaged the whole project and you can download it from the link I provide below.

Enjoy! ❤️
