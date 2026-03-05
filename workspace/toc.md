# Table of Contents: Using Docker on Ubuntu

*   **Chapter 1: Introduction to Docker and Ubuntu**
    *   1.1 What is Docker?
    *   1.2 Why Use Docker? Benefits and Use Cases
    *   1.3 Understanding Containerization vs. Virtualization
    *   1.4 Introduction to Ubuntu as a Docker Host
    *   1.5 Setting Up Your Ubuntu Environment (Basic Installation)
*   **Chapter 2: Installing Docker on Ubuntu**
    *   2.1 Prerequisites and System Requirements
    *   2.2 Recommended Installation Methods (Repository vs. Script)
    *   2.3 Installing Docker Engine
    *   2.4 Post-Installation Steps (Non-Root Access, Auto-Start)
    *   2.5 Verifying Docker Installation
    *   2.6 Troubleshooting Common Installation Issues
*   **Chapter 3: Docker Fundamentals: Images and Containers**
    *   3.1 Docker Architecture Overview
    *   3.2 Docker Images: What they are and how they work
        *   3.2.1 Pulling Images from Docker Hub
        *   3.2.2 Inspecting Images
        *   3.2.3 Deleting Images
    *   3.3 Docker Containers: Creating, Starting, Stopping, and Removing
        *   3.3.1 Running Your First Container ("Hello World")
        *   3.3.2 Detached vs. Foreground Mode
        *   3.3.3 Attaching to Running Containers
        *   3.3.4 Executing Commands in Containers
    *   3.4 Managing Container Lifecycle
*   **Chapter 4: Building Custom Docker Images with Dockerfiles**
    *   4.1 Introduction to Dockerfiles
    *   4.2 Common Dockerfile Instructions (FROM, RUN, CMD, ENTRYPOINT, COPY, ADD, WORKDIR, EXPOSE, ENV, LABEL)
    *   4.3 Best Practices for Writing Dockerfiles
    *   4.4 Building Images from Dockerfiles
    *   4.5 Tagging Images
    *   4.6 Pushing Images to Docker Hub (or Private Registry)
*   **Chapter 5: Networking and Data Management**
    *   5.1 Docker Networking Concepts
        *   5.1.1 Bridge Networks (Default)
        *   5.1.2 Host Networks
        *   5.1.3 Overlay Networks (Brief Introduction for Swarm)
        *   5.1.4 Custom Bridge Networks
    *   5.2 Container Port Mapping and Publishing
    *   5.3 DNS Resolution in Docker
    *   5.4 Docker Data Management
        *   5.4.1 Volumes: Persistent Data Storage
        *   5.4.2 Bind Mounts: Sharing Files from the Host
        *   5.4.3 tmpfs Mounts
*   **Chapter 6: Docker Compose: Multi-Container Applications**
    *   6.1 Introduction to Docker Compose
    *   6.2 Installing Docker Compose on Ubuntu
    *   6.3 Understanding `docker-compose.yml` Structure (services, networks, volumes)
    *   6.4 Building and Running Multi-Container Applications
    *   6.5 Managing Compose Applications (start, stop, restart, scale, down)
    *   6.6 Orchestrating a Simple Web Application (e.g., WordPress/MySQL)
*   **Chapter 7: Docker Security and Best Practices**
    *   7.1 Container Security Fundamentals
    *   7.2 Limiting Container Privileges (User Namespaces, Capabilities)
    *   7.3 Image Security (Base Images, Scanning, Multi-stage Builds)
    *   7.4 Network Security (Firewall rules, custom networks)
    *   7.5 Volume Security
    *   7.6 Securing the Docker Daemon
    *   7.7 Best Practices for Production Environments
*   **Chapter 8: Monitoring, Logging, and Troubleshooting**
    *   8.1 Monitoring Docker Containers ( `docker stats`, cAdvisor)
    *   8.2 Docker Logging Drivers (json-file, syslog, journald, fluentd)
    *   8.3 Viewing Container Logs ( `docker logs`)
    *   8.4 Troubleshooting Common Docker Issues
        *   8.4.1 Container startup failures
        *   8.4.2 Network connectivity problems
        *   8.4.3 Image build issues
        *   8.4.4 Resource constraints
*   **Chapter 9: Advanced Topics and Integration (Optional/Brief)**
    *   9.1 Introduction to Docker Swarm for Orchestration
    *   9.2 Using Docker with CI/CD Pipelines (e.g., Jenkins, GitLab CI)
    *   9.3 Integrating with Cloud Providers (AWS ECS, Azure Container Instances, Google Cloud Run - brief overview)
    *   9.4 Serverless Containers
    *   9.5 Future Trends in Containerization