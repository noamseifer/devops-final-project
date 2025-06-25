# devops-final-project
Final Project for Devops course - CI/CD pipelin, github actions, Prometheus and Grafana

## Prerequisites
Before you begin, ensure you have the following prerequisets:

* Linux Machine / WSL
  
For local/running on a host that supports Docker Compose (with slight modifications):
* [Docker](https://www.docker.com/products/docker-desktop) : for containerization
* [Docker Compose](https://docs.docker.com/compose/) : for managing multi-container Docker applications 
* A modern browser (to access the web application)

For running with Render:
* [Docker](https://www.docker.com/products/docker-desktop) : for containerization 
* [Docker Compose](https://docs.docker.com/compose/) : for managing multi-container Docker applications
* A modern browser (to access the web application)
* You need a Render account: 

  1. Set up a key-value instance on Render.
  2. Set up a new web service on Render that uses the following Docker Image from Dockerhub "docker.io/noamseifer/devops-final-project:latest"
  3. Set up a Deploy Hook for the web service.
  4. Define the following environment variables for your app instance on Render:
     * FLASK_APP - src/app.py
     * REDIS_HOST - redis
     * REDIS_PORT - 6379
     * REDIS_URL - the key-value URL that was provided with your Render key-value instance.
 
  5. Before continueing to the next step, make sure that both your Render web service indtance and Renver key-value instance are running.


## Running Monitoring For the Project
### 1. Clone the Repository
#### If running local/on a host that supports Docker Compose, you need to clone this repo to the host :
bash
git clone https://github.com/noamseifer/devops-final-project.git----- 
cd devops-final-project

#### If running on Render :
bash
git clone https://github.com/noamseifer/devops-final-project.git----- 
cd devops-final-project/final_project_rundirectory_for_local_monitoring

(technically speaking you only need final_project_rundirectory_for_local_monitoring for this scenerio) 

### 2. Build & Run the Docker Containers
#### If running local/on a host that supports Docker Compose:

bash
docker-compose up --build


#### If running on Render :
Edit final_project_rundirectory_for_local_monitoring/prometheus/prometheus.yml : change the app's static config target to the URL of your Render web service instance.

bash
docker-compose up

(As you are only pulling docker images from Dockerhub you don't need to build the docker images)

### 3. Start the Application
<details>
  <summary> If running local/on a host that supports Docker Compose </summary>
  
* Open your browser and go to the App:
  
        
        http://localhost:5051
        
       This will load the main page of the application, where you can add your email and view the Mailling List.

* Open your browser and go to Grafana:

http://localhost:3000


* Open your browser and go to Prometheus:

http://localhost:9090

</details>

<details>
  <summary> If running on Render </summary> 

* Open your browser and go to the URL that Render provided for your web service instance. This will load the main page of the application, where you can add your email and view the Mailling List.

* Open your browser and go to Grafana:
  
  http://localhost:3000
  

* Open your browser and go to Prometheus:
  
  http://localhost:9090
  
</details>


---
Architrcture for Render Setup:

    User interacts with the web service that is hosted on Render, The web service stores information on the Render key-value instance (Render hosted Redis).
    
    A user that intrested in viewing the website's statistics, can run a monitoring backend on his local machine that composed of Grafana container, Node Exporter container and Prometheus container. The Prometheus container extracts data from the web service container by the '/metrics' metrics_path and also extracts data from the Node Exporter container.the Node Exporter container extracts the information on the preformance and resources of the monitoring host machine that are used for the Promethues, Grafana and Node Exporter containers.
    After that Grafana container recives the information from Prometheus container and displays the dashboards accordingly.


This is the directory structure for the components necessery to run local monitoring:

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

└── src

Grafana knows to automatically display the correct dashbord structure because it's defined inside the dashboard.yml in provisioning/dashboards. Grafana knows to automatically detect the correct data source because it's defined inside the datasources_provisioning.yml in provisioning/datasources.

CI:

Main branch rules: 

![WhatsApp Image 2025-06-25 at 19 13 33_dcb52f5f](https://github.com/user-attachments/assets/83a373a1-6c23-4680-9999-7c13c172b38f)

![WhatsApp Image 2025-06-25 at 19 14 07_f8a3f7dc](https://github.com/user-attachments/assets/5e27a62a-8de0-41a8-bd84-c2136d5aaf5e)

![WhatsApp Image 2025-06-25 at 19 14 42_7fc0a893](https://github.com/user-attachments/assets/0de901a9-cb15-45b6-9dd0-37a2da324981)

![WhatsApp Image 2025-06-25 at 19 16 58_7969aeca](https://github.com/user-attachments/assets/3fd29646-056f-4a3b-bd08-53268ec6b3cf)

CI:
The CI workflow "CI_Workflow.yml" that runs on pull requst to main activates linting and unit tests, and only after those pass it uses the official docker build and push action to only build a docker image of the app (in order to test for issues in docker image generation).

CD:
The CD workflow "DeploymentWorkflow.yml" runs manually on workflow_dispatch (it could be configured differently, but we chose this manner in order to guarantee that only a human approved version of the code gets deployed). The workflow uses the official build and push action to build and push the app container image to Dockerhub, and if it successfully  deployed the docker image to Dockerhub it uses the Render service deploy hook to force the service to restart which forces render to pull the up-to-date version of the app image from Dockerhub.

Graphana and Prometheus Screenshots:

<img width="1120" alt="image" src="https://github.com/user-attachments/assets/373e7f6e-98a4-4f08-b4ab-f112889a66f9" />

<img width="879" alt="image" src="https://github.com/user-attachments/assets/286e8fec-c100-4dc4-a7af-c151456f679e" />

<img width="1120" alt="image" src="https://github.com/user-attachments/assets/be9e51b4-660b-46b9-a821-2da751960f9d" />


