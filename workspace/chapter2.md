# Chapter 2: Installing Docker on Ubuntu

This chapter provides a comprehensive guide to installing Docker Engine on an Ubuntu system. It covers prerequisites, recommended installation methods, step-by-step instructions for installation, post-installation configurations, verification, and common troubleshooting tips.

## 2.1 Prerequisites and System Requirements

Before proceeding with the Docker installation, ensure your Ubuntu system meets the following prerequisites:

*   **Operating System:** A 64-bit version of one of these Ubuntu releases:
    *   Ubuntu Jammy 22.04 (LTS)
    *   Ubuntu Focal 20.04 (LTS)
    *   Ubuntu Bionic 18.04 (LTS)
    Docker also supports non-LTS releases, but LTS versions are recommended for stability in production environments.
*   **Kernel:** Docker requires a Linux kernel version 3.10 or higher. Modern Ubuntu LTS releases fulfill this requirement.
*   **Hardware:**
    *   **RAM:** Minimum 2 GB RAM is recommended for basic Docker operations. More RAM will be required depending on the number and complexity of containers you plan to run.
    *   **Disk Space:** At least 20 GB of free disk space is recommended. Docker images and container layers can consume significant storage. Using an SSD is highly recommended for better performance.
*   **User Privileges:** You need `sudo` privileges (a user account with administrative rights) to install Docker and perform post-installation steps.
*   **Internet Connectivity:** Required for downloading Docker packages and dependencies.

## 2.2 Recommended Installation Methods (Repository vs. Script)

There are several ways to install Docker Engine on Ubuntu. This book focuses on the two most common and recommended methods:

1.  **Installing using the Docker repository (Recommended):** This is the most robust and recommended method. It involves setting up Docker's official APT repository, allowing you to install and update Docker directly using Ubuntu's package manager (`apt`). This ensures you always get the latest stable version of Docker and receive updates alongside your regular system updates.
2.  **Installing using the convenience script (For testing/development):** Docker provides a convenience script that automates the installation process. While quick and easy for testing or development environments, it is **not recommended for production environments** as it may not install the latest stable version and lacks proper version control.

For this guide, we will primarily focus on the **repository method** due to its reliability and maintainability.

## 2.3 Installing Docker Engine

Follow these steps to install Docker Engine, Containerd, and Docker Compose from the official Docker repository.

1.  **Update the `apt` package index and install necessary packages:**
    These packages are required to allow `apt` to use a repository over HTTPS.
    ```bash
    sudo apt update
    sudo apt install -y ca-certificates curl gnupg lsb-release
    ```

2.  **Add Docker's official GPG key:**
    This key is used to verify the authenticity of Docker packages.
    ```bash
    sudo mkdir -m 0755 -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    ```

3.  **Set up the Docker repository:**
    This command adds the Docker repository to your APT sources.
    ```bash
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

4.  **Update the `apt` package index again:**
    Now that the Docker repository has been added, update `apt` to include packages from this new source.
    ```bash
    sudo apt update
    ```

5.  **Install Docker Engine, Containerd, and Docker Compose:**
    Install the Docker Engine, `containerd.io` (a core container runtime), and `docker-compose-plugin` (the Docker Compose V2 plugin).
    ```bash
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

    *   `docker-ce`: The Docker Community Edition daemon.
    *   `docker-ce-cli`: The Docker command-line interface.
    *   `containerd.io`: A high-level container runtime.
    *   `docker-buildx-plugin`: A Docker CLI plugin for extended build capabilities.
    *   `docker-compose-plugin`: The new Docker Compose V2.

## 2.4 Post-Installation Steps (Non-Root Access, Auto-Start)

After installing Docker, it's essential to perform some post-installation steps for better security and usability.

### 2.4.1 Manage Docker as a Non-Root User

By default, the Docker daemon binds to a Unix socket owned by the `root` user, and other users can only access it using `sudo`. This means you'd have to prefix every `docker` command with `sudo`, which can be cumbersome and a security risk if not managed carefully.

To allow non-root users to execute Docker commands, you can add your user to the `docker` group. The `docker` group is created automatically during the Docker Engine installation.

1.  **Add your user to the `docker` group:**
    Replace `your-username` with your actual username.
    ```bash
    sudo usermod -aG docker your-username
    ```
    To apply the new group membership, you need to log out and log back in, or restart your system. Alternatively, you can run `newgrp docker` to activate the changes in your current terminal session without logging out, but this is only temporary for that session.

2.  **Verify non-root access:**
    After logging back in or using `newgrp docker`, test if you can run Docker commands without `sudo`.
    ```bash
    docker run hello-world
    ```
    If you see a message indicating that Docker is working correctly, you have successfully configured non-root access.

### 2.4.2 Configure Docker to Start on Boot

Docker is usually configured to start automatically on system boot when installed via the official repository. You can verify its status and enable it if necessary.

1.  **Check Docker service status:**
    ```bash
    sudo systemctl status docker
    ```
    You should see output indicating `Active: active (running)`.

2.  **Enable Docker to start on boot (if not already enabled):**
    ```bash
    sudo systemctl enable docker
    ```

## 2.5 Verifying Docker Installation

After installation and post-installation steps, it's crucial to verify that Docker is correctly installed and functioning.

1.  **Check Docker version:**
    This command displays the Docker client and server versions.
    ```bash
    docker version
    ```

2.  **Run the `hello-world` container:**
    This command pulls a test image from Docker Hub and runs it in a container. It's a simple way to confirm Docker Engine is working.
    ```bash
    docker run hello-world
    ```
    If successful, you will see a message similar to:
    ```
    Hello from Docker!
    This message shows that your installation appears to be working correctly.
    ...
    ```

3.  **Check Docker Compose version:**
    Verify that Docker Compose (V2 plugin) is correctly installed.
    ```bash
    docker compose version
    ```

## 2.6 Troubleshooting Common Installation Issues

Here are some common issues encountered during Docker installation and their potential solutions:

*   **"Permission denied" when running Docker commands:**
    *   **Cause:** Your user is not in the `docker` group, or the group membership hasn't been applied.
    *   **Solution:** Follow the steps in "Manage Docker as a Non-Root User" (Section 2.4.1). Ensure you have logged out and back in, or restarted your system after adding your user to the `docker` group.

*   **"Cannot connect to the Docker daemon" or "Is the docker daemon running?"**:
    *   **Cause:** The Docker service is not running.
    *   **Solution:**
        ```bash
        sudo systemctl start docker
        sudo systemctl status docker
        ```
        If it fails to start, check the Docker logs for more information:
        ```bash
        sudo journalctl -u docker.service
        ```

*   **`apt update` or `apt install` errors related to GPG keys or repositories:**
    *   **Cause:** The GPG key was not correctly added, or the repository URL is incorrect.
    *   **Solution:** Double-check the GPG key and repository setup steps in Section 2.3. Ensure there are no typos. Sometimes, old or incorrect repository entries can cause conflicts; you might need to clean up `/etc/apt/sources.list.d/docker.list` and re-add it.

*   **Docker not starting after a system reboot:**
    *   **Cause:** Docker is not enabled to start on boot.
    *   **Solution:** Enable the Docker service using `sudo systemctl enable docker`. (Section 2.4.2)

*   **Issues with older Ubuntu releases or kernel versions:**
    *   **Cause:** The Ubuntu version or Linux kernel is too old to support modern Docker features or installations.
    *   **Solution:** Upgrade your Ubuntu system to a supported LTS release.

*   **Conflicts with other container technologies (e.g., `podman`):**
    *   **Cause:** Some systems might have other container runtimes installed which can conflict with Docker's default configurations.
    *   **Solution:** Ensure that only one container runtime is actively managing the Docker socket. If you've been experimenting with `podman` or similar tools, ensure they are not interfering.

By following these installation steps and troubleshooting tips, you should have a fully functional Docker environment on your Ubuntu system.