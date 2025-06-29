# DevOps Final Project
Final Project for DevOps course — demonstrating a full CI/CD pipeline using GitHub Actions, Docker, Prometheus, and Grafana.

## Prerequisites
Before you begin, make sure you understand the two ways to run the project:


### Option 1: Run the App Locally (Everything runs on your machine)

> Choose this option if you want to run both the web application and the monitoring stack on your local machine.

**You will need:**

- ✅ A Linux machine or WSL (for Windows users)
- ✅ [Docker](https://www.docker.com/products/docker-desktop) — for containerization  
- ✅ [Docker Compose](https://docs.docker.com/compose/) — for running multiple containers  
- ✅ A modern browser (to access the app and monitoring dashboards)



### Option 2: Host the App on Render (and monitor it locally)

> Choose this option if you want to deploy your app to the cloud using [Render](https://render.com), while running Prometheus and Grafana locally for monitoring.

**You will need:**

- ✅ A [Render](https://render.com) account
- ✅ Docker & Docker Compose on your local machine (Linux/WSL)
- ✅ A modern browser (to access the app & dashboards)

#### Steps for this setup:

1. Set up a **Key-Value (Redis)** instance on Render.
2. Set up a **Web Service** using the Docker image:  
   `docker.io/noamseifer/devops-final-project:latest`
3. Set up a **Deploy Hook** for the service.
4. Define the following **environment variables** in the Render service:
   - `FLASK_APP` = `src/app.py`
   - `REDIS_HOST` = `redis`
   - `REDIS_PORT` = `6379`
   - `REDIS_URL` = *(from your Render Key-Value instance)*
5. Make sure both the Web Service and Redis instance are up and running.

---

## Running Monitoring for the Project
### 1️⃣ Clone the Repository
#### If running locally (on Linux / WSL with Docker Compose):

```bash
git clone https://github.com/noamseifer/devops-final-project.git
cd devops-final-project
```

#### If monitoring the app hosted on Render:

```bash
git clone https://github.com/noamseifer/devops-final-project.git
cd devops-final-project/final_project_rundirectory_for_local_monitoring
```
> You only need the `final_project_rundirectory_for_local_monitoring` folder for this scenario.



### 2️⃣ Build & Run the Docker Containers
#### If running locally (on Linux / WSL with Docker Compose):

```bash
docker-compose up --build
```


#### If monitoring the app hosted on Render:
1. Edit the following file:
   ```
   final_project_rundirectory_for_local_monitoring/prometheus/prometheus.yml
   ```
   Change the app's `static_configs` target to match the URL of your Render web service instance.

2. Then run:
   ```bash
   docker-compose up
   ```

> Since you're only pulling Docker images from Docker Hub, there's no need to build them manually.


### 3️⃣ Start the Application
#### If running locally (on Linux / WSL with Docker Compose):

- Open the app in your browser:  
  http://localhost:5051  
  This will load the main page of the application where you can add emails to the mailing list.

- Open Grafana:  
  http://localhost:3000

- Open Prometheus:  
  http://localhost:9090


#### If monitoring the app hosted on Render:

- Open the app using the URL provided by Render (your deployed web service).  
  This will load the main page of the application where you can add emails to the mailing list.

- Open Grafana (running locally):  
  http://localhost:3000

- Open Prometheus (running locally):  
  http://localhost:9090

---

## Architecture: Render Deployment + Local Monitoring
In our setup, the application itself is deployed to the cloud using [Render](https://render.com), while the monitoring stack (Prometheus, Grafana, and Node Exporter) runs locally.

### 🔁 How the System Works:

1. The **user interacts** with the web application hosted on Render.
2. The app stores and retrieves data using a **Render Key-Value database (Redis)**.
3. A user who wants to **monitor the app** can run the monitoring stack locally. This includes:
   - **Prometheus** (collects metrics)
   - **Grafana** (visualizes metrics)
   - **Node Exporter** (collects host system stats)

4. Prometheus pulls data from two sources:
   - The Flask web service on Render, via the `/metrics` endpoint.
   - The local Node Exporter container, for host-level resource metrics.

5. **Grafana** receives the data from Prometheus and displays it on preconfigured dashboards.


### Overview of Monitoring Files and Grafana Configuration
This is the directory layout for the local monitoring setup:

```
final_project_rundirectory_for_local_monitoring/
├── docker-compose.yml
├── grafana
│   ├── dashboards
│   │   └── main_dashboard.json
│   └── provisioning
│       ├── dashboards
│       │   └── dashboard.yml
│       └── datasources
│           └── datasources_provisioning.yml
├── prometheus
│   └── prometheus.yml
├── requirements.txt
└── src/
```
Grafana automatically loads the correct dashboard layout because it is defined in the `dashboard.yml` file located in `provisioning/dashboards`. Similarly, the data source connection is automatically configured via the `datasources_provisioning.yml` file found in `provisioning/datasources`. This setup allows Grafana to be ready-to-use as soon as the containers start, without any manual configuration.

---

## CI/CD Overview

### Continuous Integration (CI)

Our CI workflow (`CI_Workflow.yml`) runs automatically on every pull request to the **main** branch. It ensures code quality by performing:

- Linting to verify code style and catch syntax issues.  
- Unit tests to verify that the code behaves correctly.  
- Building a Docker image of the app using the official Docker build and push GitHub Action to catch any issues with image generation.

This pipeline blocks merging if any step fails, ensuring that only tested and clean code reaches the main branch.

[![CI PR Configuration Workflow](https://github.com/noamseifer/devops-final-project/actions/workflows/CI_Workflow.yml/badge.svg)](https://github.com/noamseifer/devops-final-project/actions/workflows/CI_Workflow.yml)



### Main Branch Protection Rules for CI

The following screenshots illustrate the rules we configured on the main branch to enforce the CI process before merging:

**Branch Protection Rule Overview:**  
This screenshot shows the general branch protection rules applied to the main branch.  

![Branch protection rule overview](https://github.com/user-attachments/assets/83a373a1-6c23-4680-9999-7c13c172b38f)

**Required Status Checks:**  
Here you can see which status checks (like linting and tests) must pass before a pull request can be merged.  

![Required status checks](https://github.com/user-attachments/assets/5e27a62a-8de0-41a8-bd84-c2136d5aaf5e)

**Pull Request Review Settings:**  
This image shows the settings related to pull request reviews, such as how many approvals are needed.  

![Pull request review settings](https://github.com/user-attachments/assets/0de901a9-cb15-45b6-9dd0-37a2da324981)

**Merge Restrictions:**  
Finally, this screenshot displays restrictions that prevent merging if the branch is out of date or other conditions are not met. 

![Merge restrictions](https://github.com/user-attachments/assets/3fd29646-056f-4a3b-bd08-53268ec6b3cf)




### Continuous Deployment (CD)

The deployment process is handled by the `DeploymentWorkflow.yml` workflow, which is triggered manually via the `workflow_dispatch` event.  
We intentionally chose manual triggering to ensure that only a **human-approved version** of the application is deployed.

The workflow performs the following steps:

1. **Builds and pushes** the Docker image of the application to **Docker Hub**, using the official Docker Build and Push action.
2. Once the image is successfully pushed, the workflow **calls a deploy hook** from the Render platform.
3. This hook **forces the Render service to restart**, which causes it to pull the latest version of the Docker image from Docker Hub.

This guarantees that only verified and reviewed code gets deployed to the live environment.

[![Publish Docker Image and Deploy to Render](https://github.com/noamseifer/devops-final-project/actions/workflows/DeploymentWorkflow.yml/badge.svg)](https://github.com/noamseifer/devops-final-project/actions/workflows/DeploymentWorkflow.yml)

---

## Monitoring UI – Prometheus and Grafana

The following screenshots demonstrate the local monitoring stack in action, showing how Prometheus collects metrics and how Grafana visualizes them.

### Prometheus Targets Page   
This screenshot shows the `/targets` page in Prometheus. It confirms that Prometheus is successfully scraping metrics from three targets:  
- The Flask web application  
- The local Node Exporter (system stats)  
- Prometheus itself

All targets have a status of `UP`, meaning the data collection is working correctly.

<img width="1120" alt="Prometheus - Targets" src="https://github.com/user-attachments/assets/373e7f6e-98a4-4f08-b4ab-f112889a66f9" />

### Grafana Dashboards
The following Grafana dashboards visualize the collected metrics in real time.  
These include system resource usage (CPU, memory, disk I/O), application-level metrics, and insights from Prometheus itself.  

<img width="879" alt="Grafana Dashboard 1" src="https://github.com/user-attachments/assets/286e8fec-c100-4dc4-a7af-c151456f679e" />

<img width="1120" alt="Grafana Dashboard 2" src="https://github.com/user-attachments/assets/be9e51b4-660b-46b9-a821-2da751960f9d" />

