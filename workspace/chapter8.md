# Chapter 8: Monitoring, Logging, and Troubleshooting

Effectively managing Docker containers in production requires robust monitoring, comprehensive logging, and systematic troubleshooting. This chapter provides an overview of tools and techniques for observing the health and performance of your Dockerized applications on Ubuntu, collecting and managing container logs, and diagnosing common issues.

## 8.1 Monitoring Docker Containers (`docker stats`, cAdvisor)

Monitoring is essential to understand the resource consumption, performance, and overall health of your Docker containers.

### `docker stats`

The `docker stats` command is a built-in Docker utility that provides a live stream of resource usage statistics for running containers. It's a quick and easy way to get real-time insights into CPU, memory, network I/O, and disk I/O.

*   **Usage:**
    ```bash
    docker stats
    ```
    This command displays statistics for all running containers.

*   **Monitoring specific containers:**
    ```bash
    docker stats <container_name_or_id>
    ```

*   **Output fields include:**
    *   **`CONTAINER ID`:** The ID of the container.
    *   **`NAME`:** The name of the container.
    *   **`CPU %`:** The current CPU usage percentage.
    *   **`MEM USAGE / LIMIT`:** The current memory usage and the hard memory limit (if set).
    *   **`MEM %`:** The current memory usage percentage.
    *   **`NET I/O`:** Network input/output.
    *   **`BLOCK I/O`:** Block (disk) input/output.
    *   **`PIDS`:** The number of processes running inside the container.

While `docker stats` is useful for quick checks, it provides a very basic, point-in-time view and is not suitable for historical data collection or advanced alerting.

### cAdvisor (Container Advisor)

cAdvisor is an open-source tool from Google that collects, aggregates, processes, and exports information about running containers. It provides a more comprehensive monitoring solution, including historical data, and can expose metrics for integration with other monitoring systems.

*   **Features:**
    *   Real-time and historical resource usage (CPU, memory, network, file system).
    *   Container-specific metrics.
    *   Web UI for visualization.
    *   Exports metrics in various formats (e.g., Prometheus).

*   **Running cAdvisor as a Docker Container:**
    You can easily run cAdvisor itself as a Docker container.
    ```bash
    docker run \
      --volume=/:/rootfs:ro \
      --volume=/var/run:/var/run:rw \
      --volume=/sys:/sys:ro \
      --volume=/var/lib/docker/:/var/lib/docker:ro \
      --volume=/dev/disk/:/dev/disk:ro \
      --publish=8080:8080 \
      --detach=true \
      --name=cadvisor \
      --privileged \
      google/cadvisor:latest
    ```
    *   The `--volume` flags mount various host paths into the cAdvisor container, allowing it to collect metrics.
    *   `--publish=8080:8080` maps port 8080 of the host to port 8080 of the cAdvisor container, where its web UI is accessible.
    *   `--privileged` grants the container extended privileges needed to access host system information.

*   **Accessing cAdvisor UI:**
    Once cAdvisor is running, open your web browser and navigate to `http://localhost:8080` (or `http://your_ubuntu_ip:8080`). You will see detailed graphs and statistics for your host and all running Docker containers.

For production environments, cAdvisor is often used in conjunction with other tools like Prometheus for metric storage and Grafana for dashboard visualization.

## 8.2 Docker Logging Drivers (json-file, syslog, journald, fluentd)

Docker allows you to configure different logging drivers for your containers, determining where and how container logs are collected. Each container can have its own logging driver, or you can set a default for the Docker daemon.

*   **`json-file` (Default):**
    *   **Description:** The default logging driver. It writes container logs to JSON files on the host machine.
    *   **Location:** Logs are stored in `/var/lib/docker/containers/<container-id>/<container-id>-json.log`.
    *   **Pros:** Simple, no external setup required.
    *   **Cons:** Not scalable for centralized logging. Files can grow large.
    *   **Configuration (per container):**
        ```bash
        docker run --log-driver json-file --log-opt max-size=10m --log-opt max-file=3 my-app
        ```
        This limits log files to 10MB each, rotating up to 3 files.

*   **`syslog`:**
    *   **Description:** Forwards container logs to the `syslog` daemon on the host (or a remote syslog server).
    *   **Pros:** Integrates with existing syslog infrastructure.
    *   **Cons:** Requires syslog setup.
    *   **Configuration (per container):**
        ```bash
        docker run --log-driver syslog --log-opt syslog-address=udp://192.168.1.10:514 my-app
        ```

*   **`journald`:**
    *   **Description:** Sends container logs to the `journald` daemon on the host. This is particularly useful on Ubuntu, which uses `systemd` and `journald`.
    *   **Pros:** Centralized logging on the host, easy filtering with `journalctl`.
    *   **Cons:** Primarily host-local.
    *   **Configuration (per container):**
        ```bash
        docker run --log-driver journald my-app
        ```

*   **`fluentd`:**
    *   **Description:** Forwards logs to a Fluentd daemon, which can then send them to various destinations (e.g., Elasticsearch, S3, cloud logging services).
    *   **Pros:** Highly flexible, scalable, and ideal for centralized logging in complex environments.
    *   **Cons:** Requires a Fluentd agent setup.
    *   **Configuration (per container):**
        ```bash
        docker run --log-driver fluentd --log-opt fluentd-address=localhost:24224 my-app
        ```

### Configuring a Default Logging Driver for the Docker Daemon:

You can configure a default logging driver for all containers by editing `/etc/docker/daemon.json`.
```json
# /etc/docker/daemon.json
{
  "log-driver": "journald",
  "log-opts": {
    "tag": "{{.ImageName}}/{{.Name}}/{{.ID}}"
  }
}
```
After modifying `daemon.json`, restart the Docker daemon:
```bash
sudo systemctl restart docker
```

## 8.3 Viewing Container Logs (`docker logs`)

Regardless of the configured logging driver (if it's not forwarding logs externally), the `docker logs` command is your primary tool for retrieving logs from containers.

*   **Viewing all logs from a container:**
    ```bash
    docker logs <container_name_or_id>
    ```

*   **Following logs in real-time:**
    ```bash
    docker logs -f <container_name_or_id>
    ```
    Similar to `tail -f`, this command continuously streams new log output.

*   **Viewing logs from a specific time:**
    ```bash
    docker logs --since "2023-01-01T00:00:00Z" <container_name_or_id>
    docker logs --since 5m <container_name_or_id> # Logs from the last 5 minutes
    ```

*   **Viewing the last N lines:**
    ```bash
    docker logs --tail 100 <container_name_or_id>
    ```

*   **Viewing with timestamps:**
    ```bash
    docker logs -t <container_name_or_id>
    ```

When using `journald` as a logging driver, you can also use `journalctl` to view Docker container logs.
```bash
sudo journalctl -u docker.service -f # Follow Docker daemon logs
sudo journalctl CONTAINER_NAME=<container_name> # Filter by container name
```

## 8.4 Troubleshooting Common Docker Issues

Troubleshooting Docker issues often involves inspecting logs, checking network configurations, verifying resource availability, and understanding image build processes.

### 8.4.1 Container Startup Failures

*   **Symptoms:** Container exits immediately after `docker run`, `docker ps -a` shows `Exited (...)`.
*   **Common Causes:**
    *   **Incorrect `CMD` or `ENTRYPOINT`:** The command specified in the Dockerfile (or overridden by `docker run`) is incorrect, or the application fails to start.
    *   **Missing Dependencies:** Application requires a library or package not present in the image.
    *   **Port Conflicts:** Application tries to bind to a port already in use inside the container.
    *   **Configuration Errors:** Application configuration file is missing or malformed.
*   **Troubleshooting Steps:**
    1.  **Check Logs:** The first step is always to check the container logs:
        ```bash
        docker logs <container_name_or_id>
        ```
    2.  **Run Interactively:** Run the container in interactive mode to see direct output:
        ```bash
        docker run -it --rm my-failing-image /bin/bash
        # Then manually try to execute the CMD/ENTRYPOINT command
        ```
    3.  **Inspect Image:**
        ```bash
        docker inspect <image_name>
        ```
        Look at `Cmd` and `Entrypoint` in the output.
    4.  **Check `docker events`:**
        ```bash
        docker events
        ```
        This can show real-time events, including container failures.

### 8.4.2 Network Connectivity Problems

*   **Symptoms:** Containers cannot communicate with each other, or external access to a published port fails.
*   **Common Causes:**
    *   **Incorrect Port Mapping:** `host_port:container_port` is wrong, or port is not exposed in `Dockerfile` or published with `-p`.
    *   **Firewall on Host:** Ubuntu's UFW (or other firewall) blocks traffic to the published host port.
    *   **Incorrect Network Configuration:** Containers are not on the same Docker network (e.g., trying to communicate by name on the default bridge).
    *   **DNS Resolution Issues:** Container cannot resolve the hostname of another service.
*   **Troubleshooting Steps:**
    1.  **Check `docker ps`:** Verify port mappings (`PORTS` column).
    2.  **Verify Firewall:** Check UFW status: `sudo ufw status`. Allow necessary ports.
    3.  **Inspect Network:**
        ```bash
        docker network inspect <network_name>
        ```
        Check connected containers and their IP addresses.
    4.  **Test Connectivity from Host:** `curl http://localhost:<mapped_port>`
    5.  **Test Connectivity from another Container:**
        ```bash
        docker exec -it <source_container> ping <destination_container_name_or_ip>
        docker exec -it <source_container> curl <destination_container_name_or_ip>:<port>
        ```

### 8.4.3 Image Build Issues

*   **Symptoms:** `docker build` fails with an error during one of the `RUN` steps.
*   **Common Causes:**
    *   **Typo in Dockerfile instruction:** Syntax errors.
    *   **Missing packages/dependencies:** `apt install` fails because a package isn't found.
    *   **Network issues during build:** `RUN apt update` or `curl` commands fail.
    *   **Incorrect file paths in `COPY`/`ADD`:** Source files don't exist in the build context.
*   **Troubleshooting Steps:**
    1.  **Read the build output carefully:** Docker's build output is usually very descriptive about which step failed and why.
    2.  **Inspect the failed layer:** If a `RUN` command fails, Docker often keeps the intermediate container from that layer. You can start it and debug:
        ```bash
        docker run -it <image_id_of_failed_layer> bash
        # Manually run the command that failed to see the error in detail.
        ```
    3.  **Check `.dockerignore`:** Ensure you haven't accidentally excluded necessary files from the build context.
    4.  **Rebuild with `--no-cache`:** If you suspect caching issues, try rebuilding without the cache:
        ```bash
        docker build --no-cache -t my-failing-image .
        ```

### 8.4.4 Resource Constraints

*   **Symptoms:** Containers crash unexpectedly, applications inside containers are slow, `docker stats` shows high CPU/memory usage.
*   **Common Causes:**
    *   **Insufficient RAM:** Application exceeds the host's available memory or the container's allocated memory limit.
    *   **CPU Starvation:** Application requires more CPU than available on the host or allocated to the container.
    *   **Disk I/O Bottlenecks:** Heavy disk operations within the container overwhelm the host's storage.
*   **Troubleshooting Steps:**
    1.  **Monitor with `docker stats` or cAdvisor:** Identify which resource is being exhausted.
    2.  **Check Host Resources:** Use `htop`, `free -h`, `iotop` on the Ubuntu host to see overall system resource usage.
    3.  **Increase Limits (if appropriate):** If containers are hitting their configured memory or CPU limits, consider increasing them (e.g., `--memory`, `--cpus` with `docker run`).
    4.  **Optimize Application:** Profile the application inside the container to identify resource-intensive processes.
    5.  **Clean up unused resources:** `docker system prune -a` can remove unused images, containers, volumes, and networks, freeing up disk space.

By familiarizing yourself with these monitoring, logging, and troubleshooting techniques, you can effectively manage and maintain healthy Docker environments on your Ubuntu systems. The final chapter will briefly touch upon advanced topics and integration possibilities, expanding on the concepts learned throughout this book.