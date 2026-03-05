# Chapter 4: Building Custom Docker Images with Dockerfiles

This chapter focuses on the powerful capability of Docker to create custom images using Dockerfiles. Dockerfiles provide a clear, declarative way to define the steps required to build a Docker image, ensuring consistency and reproducibility. We will cover the basic structure of a Dockerfile, common instructions, best practices, and the process of building, tagging, and sharing your custom images.

## 4.1 Introduction to Dockerfiles

A Dockerfile is a plain text file that contains a set of instructions for building a Docker image. These instructions are executed sequentially by the Docker daemon to create an image layer by layer. Each instruction typically creates a new layer on the image, making images efficient and enabling caching during builds.

The primary benefits of using Dockerfiles include:
*   **Automation:** Automates the image creation process, eliminating manual steps.
*   **Version Control:** Dockerfiles can be stored in version control systems (like Git), allowing you to track changes to your image definitions.
*   **Reproducibility:** Ensures that the same image can be built consistently across different environments.
*   **Collaboration:** Facilitates sharing and collaboration among development teams.

A typical Dockerfile is named `Dockerfile` (without any file extension) and is placed in the root directory of your project.

## 4.2 Common Dockerfile Instructions (FROM, RUN, CMD, ENTRYPOINT, COPY, ADD, WORKDIR, EXPOSE, ENV, LABEL)

Here's a breakdown of the most commonly used Dockerfile instructions:

*   **FROM:**
    *   **Purpose:** Specifies the base image for your build. Every Dockerfile must start with a `FROM` instruction.
    *   **Syntax:** `FROM <image>[:<tag>]`
    *   **Example:** `FROM ubuntu:22.04` (uses Ubuntu 22.04 as the base)

*   **RUN:**
    *   **Purpose:** Executes commands during the image build process. These commands are typically used to install packages, create directories, compile applications, etc. Each `RUN` instruction creates a new layer.
    *   **Syntax:**
        *   `RUN <command>` (shell form, runs in a shell like `/bin/sh -c`)
        *   `RUN ["executable", "param1", "param2"]` (exec form, preferred for clarity)
    *   **Example:** `RUN apt update && apt install -y nginx`

*   **CMD:**
    *   **Purpose:** Provides default commands and arguments for an executing container. There can only be one `CMD` instruction in a Dockerfile. If multiple `CMD` instructions are present, only the last one takes effect.
    *   **Syntax:**
        *   `CMD ["executable", "param1", "param2"]` (exec form, recommended)
        *   `CMD ["param1", "param2"]` (as default parameters to ENTRYPOINT)
        *   `CMD command param1 param2` (shell form)
    *   **Example:** `CMD ["nginx", "-g", "daemon off;"]` (starts Nginx in the foreground)

*   **ENTRYPOINT:**
    *   **Purpose:** Configures a container to run as an executable. When an `ENTRYPOINT` is defined, the `CMD` instruction becomes the default arguments to the `ENTRYPOINT`.
    *   **Syntax:** `ENTRYPOINT ["executable", "param1", "param2"]` (exec form, recommended)
    *   **Example:**
        ```dockerfile
        ENTRYPOINT ["/usr/bin/python3"]
        CMD ["app.py"]
        ```
        This would run `python3 app.py` when the container starts.

*   **COPY:**
    *   **Purpose:** Copies new files or directories from `<src>` (relative to the build context) and adds them to the filesystem of the container at path `<dest>`.
    *   **Syntax:** `COPY <src>... <dest>`
    *   **Example:** `COPY . /app` (copies all files from the current directory into `/app` in the image)

*   **ADD:**
    *   **Purpose:** Similar to `COPY`, but has additional features: it can extract compressed files (tar, gzip, bzip2) and fetch remote URLs. However, `COPY` is generally preferred unless these extra features are specifically needed due to `ADD`'s potentially less predictable behavior.
    *   **Syntax:** `ADD <src>... <dest>`
    *   **Example:** `ADD https://example.com/app.tar.gz /app/`

*   **WORKDIR:**
    *   **Purpose:** Sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, and `ADD` instructions that follow it in the Dockerfile.
    *   **Syntax:** `WORKDIR /path/to/workdir`
    *   **Example:**
        ```dockerfile
        WORKDIR /app
        COPY . . # Copies files into /app
        ```

*   **EXPOSE:**
    *   **Purpose:** Informs Docker that the container listens on the specified network ports at runtime. It does not actually publish the port; it's documentation and helps with `docker run -P` (publish all exposed ports).
    *   **Syntax:** `EXPOSE <port> [<port>...]`
    *   **Example:** `EXPOSE 80 443`

*   **ENV:**
    *   **Purpose:** Sets environment variables. These variables are available to subsequent instructions in the Dockerfile and to the container at runtime.
    *   **Syntax:** `ENV <key>=<value> ...`
    *   **Example:** `ENV NODE_VERSION=16.14.0`

*   **LABEL:**
    *   **Purpose:** Adds metadata to an image as key-value pairs. This can be used for organizing, filtering, or providing information about the image.
    *   **Syntax:** `LABEL <key>="<value>" [<key2>="<value2>" ...]`
    *   **Example:** `LABEL maintainer="John Doe <john.doe@example.com>" version="1.0"`

## 4.3 Best Practices for Writing Dockerfiles

Writing efficient and secure Dockerfiles is crucial for effective containerization.

*   **Use Specific Base Images:** Avoid `latest` tags for production. Use specific version tags (e.g., `ubuntu:22.04`, `node:16-alpine`) to ensure reproducibility.
*   **Minimize Layers:** Each `RUN`, `COPY`, `ADD` instruction creates a new layer. Combine multiple `RUN` commands into a single `RUN` instruction using `&&` to reduce the number of layers and image size.
    *   **Bad:**
        ```dockerfile
        RUN apt update
        RUN apt install -y some-package
        ```
    *   **Good:**
        ```dockerfile
        RUN apt update && apt install -y some-package
        ```
*   **Remove Unnecessary Files and Caches:** Clean up after installing packages to reduce image size. For `apt`, remove `apt` caches.
    *   **Example:**
        ```dockerfile
        RUN apt update && \
            apt install -y some-package && \
            rm -rf /var/lib/apt/lists/*
        ```
*   **Leverage Build Cache:** Docker caches layers. Order your Dockerfile instructions from least-frequently changing to most-frequently changing. For example, `COPY` application code after installing dependencies so that dependency installation is only re-run if the base image or dependencies change.
*   **Use `.dockerignore`:** Similar to `.gitignore`, a `.dockerignore` file specifies files and directories to exclude from the build context. This prevents unnecessary files from being sent to the Docker daemon, speeding up builds and reducing image size.
*   **Run as a Non-Root User:** By default, containers run as `root`. For security reasons, it's best practice to create a dedicated user inside the container and switch to it using the `USER` instruction.
    *   **Example:**
        ```dockerfile
        RUN adduser --system --no-create-home appuser
        USER appuser
        ```
*   **Multi-Stage Builds:** Use multi-stage builds to create smaller, more secure images. This involves using multiple `FROM` statements in a single Dockerfile, where each `FROM` starts a new build stage. You can then selectively copy artifacts from one stage to another, discarding build tools and intermediate files from the final image.
    *   **Example:**
        ```dockerfile
        # Stage 1: Build the application
        FROM node:16 as builder
        WORKDIR /app
        COPY package*.json ./
        RUN npm install
        COPY . .
        RUN npm run build

        # Stage 2: Create the final lean image
        FROM nginx:alpine
        COPY --from=builder /app/build /usr/share/nginx/html
        EXPOSE 80
        CMD ["nginx", "-g", "daemon off;"]
        ```

## 4.4 Building Images from Dockerfiles

Once you have a Dockerfile, you can build an image using the `docker build` command.

1.  **Create a Sample Dockerfile:**
    Let's create a simple web application using Nginx.
    Create a directory named `my-nginx-app`:
    ```bash
    mkdir my-nginx-app
    cd my-nginx-app
    ```
    Create an `index.html` file:
    ```html
    <!-- index.html -->
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Dockerized Nginx App</title>
    </head>
    <body>
        <h1>Hello from Nginx in a Docker Container!</h1>
        <p>This page is served by a custom Docker image.</p>
    </body>
    </html>
    ```
    Create a `Dockerfile` in the same directory:
    ```dockerfile
    # Dockerfile
    FROM nginx:latest
    COPY index.html /usr/share/nginx/html/index.html
    EXPOSE 80
    CMD ["nginx", "-g", "daemon off;"]
    ```

2.  **Build the Image:**
    Navigate to the directory containing your `Dockerfile` (e.g., `my-nginx-app`).
    The `docker build` command requires a *build context* (the set of files at a specified path) and optionally a *tag* for the image. The `.` at the end of the command specifies that the current directory is the build context.
    ```bash
    docker build -t my-nginx-app:1.0 .
    ```
    *   `-t my-nginx-app:1.0`: Tags the image with the name `my-nginx-app` and version `1.0`.
    *   `.`: Specifies the build context (the current directory).

    Docker will execute the instructions in the `Dockerfile`, displaying the output for each step.

3.  **Verify the Built Image:**
    After the build completes, list your local images to confirm `my-nginx-app:1.0` is present.
    ```bash
    docker images
    ```

4.  **Run a Container from Your Custom Image:**
    ```bash
    docker run -d -p 8080:80 --name my-web-server my-nginx-app:1.0
    ```
    *   `-d`: Runs the container in detached mode.
    *   `-p 8080:80`: Maps port 8080 on your host to port 80 inside the container (where Nginx is listening).
    *   `--name my-web-server`: Assigns a human-readable name to the container.

    You can now access your Nginx web server by opening a web browser and navigating to `http://localhost:8080` (or `http://your_ubuntu_ip:8080`).

## 4.5 Tagging Images

Tagging an image gives it a human-readable name and version (e.g., `my-app:1.0`, `ubuntu:22.04`). Tags are crucial for organizing and managing images, especially when pushing them to registries.

*   **During Build:** You can tag an image directly when building it using the `-t` flag:
    ```bash
    docker build -t my-app:latest .
    docker build -t my-app:v1.0 .
    ```

*   **After Build:** You can add additional tags to an existing image using the `docker tag` command:
    ```bash
    docker tag my-nginx-app:1.0 my-nginx-app:production
    docker tag my-nginx-app:1.0 your_dockerhub_username/my-nginx-app:1.0
    ```
    The last example shows how to tag an image with a full repository path, which is necessary before pushing to Docker Hub.

To view all tags for an image, use `docker images`. Multiple tags can point to the same image ID.

## 4.6 Pushing Images to Docker Hub (or Private Registry)

Sharing your custom images with others or deploying them across multiple environments typically involves pushing them to a Docker registry. Docker Hub is the most common public registry.

1.  **Log in to Docker Hub:**
    You need a Docker ID and must be logged in to push images.
    ```bash
    docker login
    ```
    Enter your Docker ID and password when prompted.

2.  **Tag Your Image for the Registry:**
    Before you can push an image, it must be tagged with your Docker Hub username (or the registry URL for private registries) and the repository name.
    ```bash
    docker tag my-nginx-app:1.0 your_dockerhub_username/my-nginx-app:1.0
    docker tag my-nginx-app:1.0 your_dockerhub_username/my-nginx-app:latest
    ```
    Replace `your_dockerhub_username` with your actual Docker Hub username.

3.  **Push the Image:**
    Now, push the tagged image to Docker Hub.
    ```bash
    docker push your_dockerhub_username/my-nginx-app:1.0
    docker push your_dockerhub_username/my-nginx-app:latest
    ```
    The image will be uploaded to your Docker Hub repository.

4.  **Verify on Docker Hub:**
    You can verify the successful push by logging into Docker Hub in your web browser and navigating to your repositories.

For private registries (e.g., a corporate registry), the `docker login` command would point to the registry's URL, and image tags would include the registry URL as a prefix (e.g., `myregistry.com/my-app:1.0`).

This chapter has provided a foundational understanding of creating and managing custom Docker images. With Dockerfiles, you gain precise control over your application environments, enabling consistent builds and deployments. The next chapter will explore Docker's networking and data management capabilities, which are essential for running more complex, stateful applications.