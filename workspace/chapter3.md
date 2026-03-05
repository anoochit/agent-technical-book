# Chapter 3: Docker Fundamentals: Images and Containers

This chapter delves into the core components of Docker: images and containers. Understanding these fundamental concepts is crucial for effectively utilizing Docker. We will explore Docker's architecture, how images are built and managed, and the lifecycle of containers.

## 3.1 Docker Architecture Overview

To grasp how Docker works, it's essential to understand its architecture. Docker uses a client-server architecture. The Docker client communicates with the Docker daemon, which handles the heavy lifting of building, running, and distributing your Docker containers.

*   **The Docker Daemon (dockerd):** This is the persistent background process that manages Docker objects such as images, containers, networks, and volumes. The daemon listens for Docker API requests and processes them.
*   **The Docker Client:** This is how users interact with Docker. The Docker client (`docker`) is a command-line interface (CLI) that takes commands from the user (e.g., `docker run`, `docker build`) and sends them to the Docker daemon. The client can communicate with a daemon running on the same host or a remote host.
*   **Docker Registries:** A Docker registry stores Docker images. Docker Hub is a public registry that anyone can use, and Docker is configured by default to look for images on Docker Hub. You can also run private registries.
*   **Docker Images:** Images are read-only templates with instructions for creating a Docker container. An image is a snapshot of an application and its environment.
*   **Docker Containers:** A container is a runnable instance of an image. You can create, start, stop, move, or delete a container using the Docker API or CLI.

```
+---------------------------------------------------------------------------------------+
| User                                                                                  |
| +---------------------+                                                               |
| | Docker Client (CLI) |                                                               |
| | (e.g., docker run)  |                                                               |
| +----------^----------+                                                               |
|            | REST API                                                                  |
|            v                                                                           |
| +-----------------------------------------------------------------------------------+ |
| | Docker Host                                                                       | |
| |                                                                                   | |
| | +-----------------------------------------------------+   +---------------------+ | |
| | | Docker Daemon (dockerd)                             |   | Docker Registry     | | |
| | |                                                     |   | (e.g., Docker Hub)  | | |
| | | +-------------------+ +-------------------+         |   |                     | | |
| | | | Images            | | Containers        |         |<--| Push/Pull Images  | | |
| | | | (read-only layers)| | (runnable instances)|         |   +---------------------+ | |
| | | +-------------------+ +-------------------+         |                             |
| | |                                                     |                             |
| | +-----------------------------------------------------+                             |
| |                                                                                   | |
| | Host OS (Ubuntu)                                                                  | |
| +-----------------------------------------------------------------------------------+ |
| Host Hardware                                                                         |
+---------------------------------------------------------------------------------------+
```

## 3.2 Docker Images: What they are and how they work

A Docker image is a lightweight, standalone, executable package that includes everything needed to run a piece of software, including the code, a runtime, system tools, libraries, and settings. Images are built from a `Dockerfile`, which is a text file containing instructions for assembling an image.

Images are composed of a series of read-only layers. Each layer represents a Dockerfile instruction. When you change an image (e.g., by adding a file), a new layer is created on top of the previous ones. This layered approach makes images efficient; multiple images can share common base layers, saving disk space.

### 3.2.1 Pulling Images from Docker Hub

Docker Hub is the default public registry for Docker images. You can pull pre-built images from Docker Hub using the `docker pull` command.

To pull an image:
```bash
docker pull ubuntu:latest
```
This command downloads the `ubuntu` image with the `latest` tag from Docker Hub. If no tag is specified, Docker defaults to `latest`.

You can also pull a specific version (tag) of an image:
```bash
docker pull ubuntu:22.04
```

To list all locally downloaded images:
```bash
docker images
```

### 3.2.2 Inspecting Images

You can inspect the detailed information of a Docker image using the `docker inspect` command. This provides a JSON output containing metadata about the image, including its history, layers, configuration, and environment variables.

To inspect an image:
```bash
docker inspect ubuntu:latest
```

You can also get a summary of an image's history, showing how its layers were created:
```bash
docker history ubuntu:latest
```

### 3.2.3 Deleting Images

To free up disk space, you might need to remove old or unused images.

To remove a single image:
```bash
docker rmi ubuntu:22.04
```
You can use either the image name and tag (e.g., `ubuntu:22.04`) or the image ID. If an image is used by a container, you cannot delete it directly unless you first remove the container.

To remove multiple images:
```bash
docker rmi image1:tag image2:tag
```

To remove all unused Docker images (images that are not associated with any containers):
```bash
docker image prune
```
This command helps clean up your local image cache. To remove all dangling images (images that are not tagged and not referenced by any container) and all unused images, you can use:
```bash
docker image prune -a
```

## 3.3 Docker Containers: Creating, Starting, Stopping, and Removing

A Docker container is a runnable instance of a Docker image. When you run an image, Docker creates a container from it. Containers are isolated processes running on the host, with their own filesystem, network interfaces, and process space.

### 3.3.1 Running Your First Container ("Hello World")

The most basic way to run a container is with the `docker run` command.

To run the `hello-world` container, which simply prints a message and exits:
```bash
docker run hello-world
```
If the image is not found locally, Docker will automatically pull it from Docker Hub before running the container.

### 3.3.2 Detached vs. Foreground Mode

Containers can run in two modes:

*   **Foreground Mode:** The container runs in the foreground, and its output is displayed directly in your terminal. The terminal remains attached to the container's process, and if you close the terminal, the container will stop (unless configured otherwise).
    ```bash
    docker run ubuntu:latest echo "Hello from a foreground container!"
    ```

*   **Detached Mode:** The container runs in the background, freeing up your terminal. This is ideal for long-running applications. To run a container in detached mode, use the `-d` or `--detach` flag.
    ```bash
    docker run -d ubuntu:latest sleep 3600
    ```
    This command runs an Ubuntu container in the background, executing the `sleep 3600` command, which keeps the container running for one hour. Docker will print the container ID.

To list all running containers:
```bash
docker ps
```
To list all containers, including stopped ones:
```bash
docker ps -a
```

### 3.3.3 Attaching to Running Containers

If a container is running in detached mode, you might need to attach to its input/output streams to interact with it.

To attach to a running container:
```bash
docker attach <container_id_or_name>
```
For example, if you ran the `sleep 3600` container, you could attach to it. However, if the container doesn't have an interactive process, attaching might not show much.

A more common scenario for interacting with a running container is to execute commands inside it.

### 3.3.4 Executing Commands in Containers

The `docker exec` command allows you to run new commands inside an already running container. This is very useful for debugging, installing packages, or making temporary changes.

To open an interactive Bash shell inside a running Ubuntu container:
```bash
docker exec -it <container_id_or_name> bash
```
*   `-i`: Keeps STDIN open even if not attached.
*   `-t`: Allocates a pseudo-TTY.
*   `bash`: The command to execute inside the container.

Once inside the container, you can run Linux commands as usual. Type `exit` to leave the container's shell without stopping the container.

## 3.4 Managing Container Lifecycle

Managing containers involves starting, stopping, restarting, and removing them.

*   **Starting a container:**
    If a container is stopped, you can restart it using its ID or name.
    ```bash
    docker start <container_id_or_name>
    ```

*   **Stopping a container:**
    To gracefully stop a running container, Docker sends a `SIGTERM` signal, allowing the application to shut down cleanly. After a timeout (default 10 seconds), it sends `SIGKILL` if the application hasn't stopped.
    ```bash
    docker stop <container_id_or_name>
    ```

*   **Restarting a container:**
    This command stops and then starts a container.
    ```bash
    docker restart <container_id_or_name>
    ```

*   **Pausing and Unpausing a container:**
    You can pause all processes within a container. This is different from `stop` as it doesn't shut down the container's processes; it merely suspends them.
    ```bash
    docker pause <container_id_or_name>
    docker unpause <container_id_or_name>
    ```

*   **Removing a container:**
    To remove a stopped container:
    ```bash
    docker rm <container_id_or_name>
    ```
    You cannot remove a running container unless you use the `-f` (force) flag, which will first stop it.
    ```bash
    docker rm -f <container_id_or_name>
    ```

*   **Removing all stopped containers:**
    To clean up your system by removing all stopped containers:
    ```bash
    docker container prune
    ```
    This command is very useful for development environments where many temporary containers might accumulate.

By understanding these fundamental operations, you can effectively manage individual Docker images and containers on your Ubuntu host. The next chapter will build on this knowledge by demonstrating how to create your own custom Docker images using Dockerfiles.