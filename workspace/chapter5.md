# Chapter 5: Networking and Data Management

This chapter explores how Docker containers communicate with each other, with the host system, and with the outside world, covering various networking modes and concepts. It also details Docker's mechanisms for persistent data storage, which is crucial for stateful applications.

## 5.1 Docker Networking Concepts

Docker's networking subsystem allows containers to be isolated from or connected to each other and the host machine. By default, Docker creates networks for you, but understanding how they work and creating custom networks is essential for more complex deployments.

### 5.1.1 Bridge Networks (Default)

When you install Docker, it creates a default `bridge` network. Unless you specify otherwise, all newly created containers connect to this bridge network.

*   **How it works:** Docker creates a software bridge (`docker0`) on the host machine. Containers connected to this bridge network are assigned an IP address from a private, internal subnet (e.g., 172.17.0.x). Docker then forwards traffic between the container's virtual network interface and the host's physical network interface.
*   **Isolation:** Containers on the default bridge network can communicate with each other by their IP addresses. However, for communication by name, or for enhanced isolation, custom bridge networks are preferred.
*   **External Access:** To allow external access to a container on a bridge network, you must explicitly publish or map its ports to the host's ports (covered in Section 5.2).

To inspect the default bridge network:
```bash
docker network inspect bridge
```
To run a container on the default bridge network (this is the default behavior if no network is specified):
```bash
docker run --name my-bridge-app -d nginx
```

### 5.1.2 Host Networks

When a container uses the `host` network mode, it shares the network namespace of the host machine. This means the container does not get its own IP address; instead, it uses the host's IP address and port space directly.

*   **Benefits:** This mode offers the best network performance because it bypasses the Docker network stack. It's useful for scenarios where network overhead is critical, or when an application needs to access services on `localhost` of the host directly.
*   **Considerations:** Reduced isolation. If multiple containers run in `host` mode and try to bind to the same port, it will lead to conflicts.
*   **Usage:**
    ```bash
    docker run --network host --name my-host-app -d nginx
    ```
    If Nginx is configured to listen on port 80 inside the container, and you run it with `--network host`, it will directly listen on port 80 of your Ubuntu host.

### 5.1.3 Overlay Networks (Brief Introduction for Swarm)

Overlay networks are specifically designed for multi-host container deployments, especially within Docker Swarm (a native orchestration tool).

*   **Purpose:** They enable containers running on different Docker hosts to communicate securely as if they were on the same network.
*   **Mechanism:** Overlay networks use VXLAN encapsulation to create a virtual network across multiple physical hosts. Docker handles the routing and encryption.
*   **Scope:** While primarily used in Swarm mode, understanding their existence is important for scaling Docker beyond a single host. Detailed coverage of Swarm and overlay networks is beyond the scope of this fundamental chapter but will be briefly touched upon in Chapter 9.

### 5.1.4 Custom Bridge Networks

Creating custom bridge networks is a best practice for most multi-container applications.

*   **Benefits:**
    *   **Improved Isolation:** Containers on a custom bridge network are isolated from containers on the default bridge network.
    *   **Automatic DNS Resolution:** Containers connected to the same custom bridge network can resolve each other by name (service discovery). This is a significant advantage over the default bridge network where you typically need to use IP addresses.
    *   **Better Organization:** You can create separate networks for different applications or environments.

*   **Creating a Custom Bridge Network:**
    ```bash
    docker network create my-custom-network
    ```

*   **Running Containers on a Custom Network:**
    ```bash
    docker run -d --name web-server --network my-custom-network nginx
    docker run -d --name db-server --network my-custom-network postgres
    ```
    Now, the `web-server` container can reach the `db-server` container using the hostname `db-server` (e.g., `ping db-server`).

*   **Listing Networks:**
    ```bash
    docker network ls
    ```

*   **Inspecting a Network:**
    ```bash
    docker network inspect my-custom-network
    ```

*   **Removing a Network:**
    A network can only be removed if no containers are connected to it.
    ```bash
    docker network rm my-custom-network
    ```

## 5.2 Container Port Mapping and Publishing

While `EXPOSE` in a Dockerfile documents which ports a container listens on, `docker run -p` or `--publish` is used to actually map and publish those ports to the host machine. This allows external clients to access services running inside the container.

*   **Syntax:** `docker run -p <host_port>:<container_port> <image>`
*   **Example:**
    Let's run an Nginx container and map host port 8080 to container port 80:
    ```bash
    docker run -d -p 8080:80 --name my-web-app nginx
    ```
    Now, you can access the Nginx web server from your host's browser at `http://localhost:8080`.

*   **Mapping to a specific host IP:**
    ```bash
    docker run -d -p 192.168.1.100:80:80 nginx
    ```
    This maps container port 80 to host port 80 on the specific IP address `192.168.1.100`.

*   **Random Host Port:** If you only specify the container port, Docker will pick a random available host port. This is useful for testing.
    ```bash
    docker run -d -p 80 --name random-port-nginx nginx
    ```
    To find out which port Docker assigned, use `docker port <container_name>` or `docker ps`.

*   **Publishing all exposed ports:** The `-P` or `--publish-all` flag publishes all ports exposed by the image to random host ports.
    ```bash
    docker run -d -P --name all-ports-nginx nginx
    ```

## 5.3 DNS Resolution in Docker

Docker provides an internal DNS server that allows containers to resolve each other's names, especially when connected to custom bridge networks.

*   **Default Bridge Network:** Containers on the default `bridge` network can only resolve each other by IP address.
*   **Custom Bridge Networks:** When containers are connected to the same user-defined bridge network, they can resolve each other by their container names (or service names in Docker Compose). Docker's embedded DNS server handles this resolution.
    *   **Example:** If you have containers named `web` and `db` on the same custom network, `web` can reach `db` using `db` as the hostname.
*   **External DNS:** Docker containers inherit DNS settings from the host by default. You can also configure custom DNS servers for containers:
    ```bash
    docker run -d --name my-app --dns 8.8.8.8 --dns 8.8.4.4 alpine
    ```
    This sets Google's public DNS servers for the `my-app` container.

## 5.4 Docker Data Management

Containers are ephemeral by design; when a container is removed, any data written inside it is lost. For stateful applications (databases, logging systems, etc.), persistent data storage is critical. Docker offers several options for managing data: Volumes, Bind Mounts, and tmpfs Mounts.

### 5.4.1 Volumes: Persistent Data Storage

Volumes are the preferred mechanism for persisting data generated by and used by Docker containers. They are entirely managed by Docker.

*   **Benefits:**
    *   **Docker-managed:** Volumes are stored in a part of the host filesystem (`/var/lib/docker/volumes/` on Linux) that is managed by Docker.
    *   **High Performance:** Volumes are directly mounted into containers, offering good I/O performance.
    *   **Portable:** Volumes can be easily backed up, restored, and moved between Docker hosts.
    *   **Supports volume drivers:** Allows integration with external storage systems (e.g., cloud storage, NFS).
    *   **No host path knowledge needed:** You only need to know the volume name.

*   **Creating a Volume:**
    ```bash
    docker volume create my-data-volume
    ```

*   **Mounting a Volume to a Container:**
    Use the `-v` or `--volume` flag with `docker run`.
    ```bash
    docker run -d -p 80:80 --name my-nginx-with-volume -v my-data-volume:/usr/share/nginx/html nginx
    ```
    This mounts `my-data-volume` to `/usr/share/nginx/html` inside the Nginx container. Any content written to `/usr/share/nginx/html` will persist even if the container is removed.

*   **Listing Volumes:**
    ```bash
    docker volume ls
    ```

*   **Inspecting a Volume:**
    ```bash
    docker volume inspect my-data-volume
    ```

*   **Removing a Volume:**
    A volume can only be removed if no containers are using it.
    ```bash
    docker volume rm my-data-volume
    ```
    To remove all unused local volumes:
    ```bash
    docker volume prune
    ```

### 5.4.2 Bind Mounts: Sharing Files from the Host

Bind mounts allow you to mount a file or directory from the host machine directly into a container.

*   **Benefits:**
    *   **Simple:** Easy to use for development, especially when source code needs to be reflected in the container immediately.
    *   **Direct Host Access:** Gives containers direct access to host files and directories.

*   **Considerations:**
    *   **Host Dependent:** The container relies on the host's filesystem structure. Not portable.
    *   **Security Risk:** If a container has write access to host files, it can potentially alter or delete critical host data.
    *   **Performance:** Can have performance implications compared to volumes in certain scenarios.

*   **Mounting a Bind Mount:**
    Use the `-v` or `--volume` flag with `docker run`.
    ```bash
    docker run -d -p 8080:80 --name my-nginx-bind -v /path/to/your/html:/usr/share/nginx/html nginx
    ```
    Replace `/path/to/your/html` with an actual path on your Ubuntu host. Changes made to `index.html` on your host will immediately be reflected in the container.

### 5.4.3 tmpfs Mounts

`tmpfs` mounts store data only in the host's memory, not in the filesystem.

*   **Benefits:**
    *   **Highly Performant:** Data access is very fast as it resides in RAM.
    *   **Non-Persistent:** Data is discarded when the container stops, making it ideal for sensitive information or temporary files that should not persist.
    *   **Security:** Data is never written to disk, enhancing security for temporary sensitive data.

*   **Mounting a `tmpfs` Mount:**
    Use the `--tmpfs` flag with `docker run`.
    ```bash
    docker run -d --name my-temp-app --tmpfs /app/temp-data alpine
    ```
    Any data written to `/app/temp-data` inside the `my-temp-app` container will only exist in memory and will be lost when the container stops.

Choosing between volumes, bind mounts, and `tmpfs` mounts depends on your application's requirements for data persistence, performance, and security. For most persistent application data, volumes are the recommended approach.

This chapter has provided a detailed overview of Docker's networking models and data persistence mechanisms. Mastering these concepts is fundamental to deploying robust and scalable containerized applications. The next chapter will build on this by introducing Docker Compose, a tool for defining and running multi-container Docker applications.