# 🌦️ WeatherApp CI/CD Pipeline with Jenkins, GitLab & Docker on AWS 🚀

## 🧭 Overview 🌟

This project establishes a CI/CD pipeline for the WeatherApp using Jenkins, GitLab, and Docker, deployed across AWS EC2 instances. The pipeline automates building, testing, and deploying the application, ensuring efficient and reliable delivery. ✨

## 🖥️ Infrastructure 🏗️

The architecture comprises four AWS EC2 instances:

### 1. GitLab Server 🦊

- **Instance Type:** t3.medium ⚙️
- **Storage:** 20 GB 💾
- **OS:** Ubuntu Linux 🐧
- **Security Groups:**
  - SSH: 🔒 Open only to your IP
  - HTTP/HTTPS/TCP: 🌐 Open to all
- **Purpose:** Hosts the GitLab repository for source code management, version control, and webhook triggers for CI/CD. 📂

### 2. Jenkins Server 🛠️

- **Instance Type:** t3.medium ⚙️
- **Storage:** 20 GB 💾
- **OS:** Ubuntu Linux 🐧
- **Security Groups:**
  - SSH: 🔒 Open only to your IP
  - HTTP/HTTPS/TCP: 🌐 Open to all
  - Port 8080: 🔗 Open for Jenkins Web UI
- **Purpose:** Runs the Jenkins master, orchestrating the CI/CD pipeline, managing jobs, and coordinating with the agent. 🎮

### 3. Jenkins Agent 🤖

- **Instance Type:** t2.micro ⚙️
- **Storage:** 10 GB 💾
- **OS:** Ubuntu Linux 🐧
- **Security Groups:**
  - SSH: 🔒 Open to Jenkins Server and your IP
- **Purpose:** Executes pipeline stages like building, testing, and running Pylint for code analysis. 🧪
- **dependencies:** Via the script bellow.

### 4. WeatherApp Instance ☁️

- **Instance Type:** t2.micro ⚙️
- **Storage:** 8 GB 💾
- **OS:** Ubuntu Linux 🐧
- **Security Groups:**
  - SSH: 🔒 Open only to your IP
  - HTTP/HTTPS/TCP: 🌐 Open to all
- **Purpose:** Hosts the deployed WeatherApp in a Docker container, serving the application to users. 🌍
- **dependencies:** Downloaded docker + the app docker image

```
 echo "🐳 Installing Docker..."
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


```

## Jenkins Configuration 🧑‍🔧

### Plugins Installed 🧩

- **GitLab Plugin:** 🦊 Integrates Jenkins with GitLab for repository access and webhook triggers.
- **Slack Notification:** 💬 Sends pipeline status updates to Slack.
- **Docker Pipeline:** 🐳 Enables Docker commands in the pipeline for building and pushing images.
- **SSH Agent:** 🔑 Facilitates SSH connections to the Jenkins Agent and WeatherApp instance.

### Credentials Setup 🔐

- **GitLab Token:** 🦊 Created in GitLab, added to Jenkins for secure repository access.
- **DockerHub Token:** 🐳 Generated for Jenkins to authenticate and push Docker images to DockerHub.
- **Jenkins API Token:** 🔧 Used for agent authentication (via setup script).

### Agent Configuration 🤖

- **Java Installation:** ☕ Installed via script to run the Jenkins agent.jar.
- **Pylint Installation:** 🧪 Added for static code analysis during pipeline execution.
- **SSH Setup:** 🔑 Configured SSH keys for Jenkins to securely connect to the Agent.
- **Private IP:** 🌐 Used the Agent’s private IP for secure communication with Jenkins.
- **Dependency Script:** 📦 Automated installation of agent dependencies (Java, Docker, Git, Python, Pylint) to ensure the agent is ready for pipeline tasks.

**Agent Setup Script:** 📜

```bash
#!/bin/bash

set -e

echo "=================================="
echo "🔥 Jenkins Agent SSH Setup Script 🔥"
echo "=================================="

# === updating system ===
echo "🔧 Updating system package index..."
sudo apt-get update -y

# === install dependencies ===
install_if_missing() {
    if ! dpkg -s "$1" &> /dev/null; then
        echo "📦 Installing $1..."
        sudo apt-get install -y "$1"
    else
        echo "✅ $1 already installed."
    fi
}

DEPENDENCIES=(curl ca-certificates lsb-release gnupg git python3 python3-venv python3-pip openjdk-11-jdk openssh-server)

for pkg in "${DEPENDENCIES[@]}"; do
    install_if_missing "$pkg"
done

# === install docker if missing ===
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
    echo "✅ Docker already installed."
fi

# === check Java ===
echo "☕ Verifying Java version:"
java -version

# === check SSH ===
echo "🔐 Verifying SSH server status..."
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl status ssh --no-pager

echo "✅ Jenkins SSH-based agent setup complete. You can now connect from the controller!"

```

## 🧑‍🔧 Jenkins Configurations & Pipeline ♾️

- **GitLab Configurations:** 🦊
  - **Connection Name:** ✨ As you desire.
  - **GitLab Host URL:** 🌐 The private IP of your GitLab server.
  - **Credentials:** 🔑 The GitLab API token.
- **Pipeline Creation:** 📦 A new pipeline item was created in Jenkins, configured to pull the WeatherApp repository from GitLab using the stored GitLab token.
- **Pipeline Stages:** 🚀 The pipeline (Jenkinsfile) includes:
  - **Checkout:** 📥 Clones the repository from GitLab.
  - **Lint Check:** 🧪 Tests the Python code of app.py (lint test).
  - **Build:** 🛠️ Builds the Docker image for WeatherApp using the Dockerfile.
  - **Deploy Locally & Test:** 🌍 Runs the app locally to test the Docker image before push (reachability test).
  - **Push:** 📤 Pushes the Docker image to DockerHub using the DockerHub token.
  - **Deploy & Test:** 🚀 Deploys the Docker container to the WeatherApp instance via SSH, using Docker Compose to manage the service + reachability test again on the production instance.
  - **Clean & Slack Notification:** 🧹 Cleans all resources and notifies about the pipeline status via Slack.
- **Triggers:** ⏰ Configured to start automatically on GitLab push events via webhook integration.
- **Agent Assignment:** 🤖 Pipeline stages are executed on the Jenkins Agent to offload tasks from the master.
- **Slack Notifications:** 💬 Sends pipeline status (success/failure) to a Slack channel for team visibility.
- **Dependency File:** 📋 Dependencies for the pipeline:
  ```
  requests
  pylint
  ```
- **Error Handling:** ⚠️ Pipeline includes error handling (failing the build if Pylint score is below threshold or reachability test fails).
- **Security:** 🔒 Credentials are securely stored in Jenkins and accessed via environment variables in the pipeline.

---

- **The Pipeline📜:**

```
pipeline {
    agent { label 'weatherApp-agent' }

    environment {
        DOCKER_IMAGE = '<YOUR-IMAGE-NAME>:latest'
        CONTAINER_NAME = '<YOUR-CONTAINER-NAME>'
        APP_HOST =  <APP-HOST-PRIVATE-IP>
        WORKSPACE = 'workspace'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }


        stage('Lint Check') {
            steps {
                sh '''
                    docker --version
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install pylint
                    . venv/bin/activate
                    pylint app.py --fail-under=5
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $CONTAINER_NAME:latest .'
            }
        }

        stage('Deploy Locally for Testing') {
            steps {
                sh '''
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true

                    docker run -d -p 5000:5000 --name $CONTAINER_NAME $CONTAINER_NAME:latest || {
                        echo "❗ Port 5000 might already be in use. Showing usage:"
                        sudo lsof -i :5000
                        exit 1
                    }


                    echo "⏳ Waiting for container to initialize..."
                    sleep 5

                    echo "🧪 Running reachability test script..."
                    python3 /home/ubuntu/workspace/weatherApp-pipeline/isreachable.py

                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag $CONTAINER_NAME:latest $DOCKER_IMAGE
                        docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to Remote Server') {
            steps {
                 sshagent(credentials: ['gitlab-instance-key.pem']) {
                     sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@APP_HOST << 'ENDSSH'
                        echo "🔍 Navigating to application directory..."
                        cd /home/ubuntu/weatherApp/

                        echo "🔍 Stopping and removing existing containers..."
                        docker-compose down

                        echo "⬇️ Pulling latest image..."
                        docker compose pull

                        echo "🚀 Starting application with Docker Compose..."
                        docker compose up -d --force-recreate
                        docker image prune -f
ENDSSH
            '''
            }
        }
    }

        stage('Verify Remote Deployment') {
            steps {
                sshagent(credentials: ['gitlab-instance-key.pem']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@APP_HOST << 'ENDSSH'
                            echo "🧐 Checking if weatherapp is running..."
                            sudo docker ps -a

                            echo "📡 Sending request to http://localhost:5000..."
                            sleep 5
                            curl -I http://localhost:5000 || echo "⚠️ App is not responding as expected."
ENDSSH
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'

            sh '''
                echo "🧹 Cleaning local Docker resources..."
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
                docker rmi $CONTAINER_NAME:latest || true
                docker container prune -f
                docker image prune -af
                docker volume prune -f
                docker network prune -f

                echo "🧹 Cleaning Jenkins workspace and cache..."

                # Clean all files and subdirectories inside the workspace
                rm -rf $WORKSPACE/* || true
                find $WORKSPACE -type f -name ".*" -delete || true  # Delete hidden files

                # Clean hidden directories inside the workspace if any
                find $WORKSPACE -type d -name ".*" -exec rm -rf {} + || true

                # Clean the user's cache (there might be important files here, be careful)
                rm -rf ~/.cache/* || true

                # Clean Jenkins agent logs
                rm -f ~/agent/remoting/logs/* || true

                echo "✅ Workspace and cache cleaned successfully!"            '''
        }
        success {
            slackSend (
                channel: '#all-amitor2002',
                color: 'good',
                message: "✅ Build #${env.BUILD_NUMBER} succeeded in ${env.JOB_NAME}"
            )

            echo '✅ Pipeline executed successfully.'
        }
        failure {
            slackSend (
                channel: '#all-amitor2002',
                color: 'danger',
                message: "❌ Build #${env.BUILD_NUMBER} failed in ${env.JOB_NAME}"
            )
            echo '❌ Pipeline failed. Please check the logs for details.'
        }
    }
}
```

---

## GitLab Configurations 🦊

- **Repository Setup:** 📂 The WeatherApp source code is hosted in a GitLab repository, with branches for development and production.
- **Webhook Integration:** 🔗 A webhook is configured in GitLab to trigger the Jenkins pipeline on push events to the main branch, ensuring automatic CI/CD execution.
- **Webhook Integration:** ⏰ An integration setting for push triggers the Jenkins server job (pipeline).
- **Token Security:** 🔒 A GitLab access token was generated with repository read/write permissions and added to Jenkins credentials for secure API access.
- **Pipeline Status:** 📊 GitLab displays pipeline status (success/failure) from Jenkins, providing visibility into CI/CD progress.

## Testing & Validation ✅

- **Pylint Integration:** 🧪 The pipeline runs Pylint on the WeatherApp codebase to enforce coding standards, with a configurable score threshold (more than 5/10). Failures below the threshold halt the pipeline.
- **Reachability Test:** 📡

```
import requests

def check_url(name, url):
    try:
        print(f"🔍 Checking {name} at {url}")
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            print(f"✅ {name} is UP!")
            return True
        else:
            print(f"⚠️ {name} responded with status code: {res.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name} is DOWN! Error: {e}")
        return False

if __name__ == "__main__":
    REMOTE_IP = '<PRODUCTION-PUBLIC-IP>'
    local_ok = check_url("Local Container", "http://localhost:5000")
    remote_ok = check_url("Remote Production", f"http://{REMOTE_IP}:5000")

    if not local_ok or not remote_ok:
        exit(1)
```

- **Validation Post-Deployment🔍:** The pipeline SSHes into the WeatherApp instance to verify the Docker container is running and accessible after deployment.
