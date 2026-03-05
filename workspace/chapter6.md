# Chapter 6: Docker Compose: Multi-Container Applications

This chapter introduces Docker Compose, a powerful tool for defining and running multi-container Docker applications. While individual Docker commands are suitable for single containers, Compose simplifies the management of interconnected services, making development, testing, and deployment of complex applications much more efficient.

## 6.1 Introduction to Docker Compose

Modern applications often consist of multiple services working together (e.g., a web server, a database, an API service). Manually starting, linking, and managing each container with individual `docker run` commands can become cumbersome and error-prone. Docker Compose addresses this challenge by allowing you to define your entire application stack in a single YAML file, typically named `docker-compose.yml`.

Docker Compose enables you to:

*   **Define Multi-Container Applications:** Describe all services, networks, and volumes required for your application in a declarative configuration file.
*   **Start and Stop All Services with a Single Command:** Orchestrate the entire application lifecycle with commands like `docker compose up` and `docker compose down`.
*   **Isolate Environments:** Easily create isolated development, testing, and production environments for your applications.
*   **Portability:** Share your application stack definition with others, ensuring everyone runs the same environment.

Docker Compose is included as part of the Docker Engine installation as a plugin (`docker-compose-plugin`), making it readily available once Docker is installed.

## 6.2 Installing Docker Compose on Ubuntu

As mentioned in Chapter 2, Docker Compose (V2) is now integrated as a Docker CLI plugin. If you followed the Docker Engine installation guide in Chapter 2 (Section 2.3), you likely already have `docker-compose-plugin` installed.

You can verify its installation and version using:
```bash
docker compose version
```
You should see output similar to `Docker Compose version v2.x.y`.

If for some reason it's not installed or you installed Docker via a different method, you can install it using `apt`:
```bash
sudo apt update
sudo apt install docker-compose-plugin -y
```

## 6.3 Understanding `docker-compose.yml` Structure (services, networks, volumes)

The `docker-compose.yml` file is at the heart of Docker Compose. It uses YAML syntax to define your application's services, networks, and volumes.

A typical `docker-compose.yml` file has a `version` key at the top, followed by `services`, `networks`, and `volumes` sections.

### Top-level Keys:

*   **`version`:** Specifies the Compose file format version. It's recommended to use the latest stable version (e.g., `'3.8'`).
*   **`services`:** Defines the individual containers (services) that make up your application. Each service typically corresponds to a container.
*   **`networks`:** Defines custom networks for your services to communicate over. This is highly recommended for better isolation and automatic service discovery.
*   **`volumes`:** Defines named volumes for persistent data storage.

### Services Section:

Each entry under `services` defines a container. Common options for a service include:

*   **`image`:** The Docker image to use for the service (e.g., `nginx:latest`, `mysql:8.0`).
*   **`build`:** Specifies a path to a directory containing a `Dockerfile` if you want to build a custom image for this service.
*   **`ports`:** Maps host ports to container ports (similar to `docker run -p`).
    *   Example: `- "8080:80"` (maps host port 8080 to container port 80)
*   **`environment`:** Sets environment variables inside the container.
    *   Example: `- DB_HOST=db`, `- DB_USER=user`
*   **`volumes`:** Mounts host paths or named volumes into the container (similar to `docker run -v`).
    *   Example: `- ./app:/var/www/html`, `- db-data:/var/lib/mysql`
*   **`networks`:** Connects the service to one or more defined networks.
*   **`depends_on`:** Defines dependencies between services. This ensures that dependent services are started before the current service. Note: `depends_on` only ensures the container is *started*, not necessarily that the application inside it is *ready*.
*   **`restart`:** Defines the restart policy for the container (e.g., `always`, `on-failure`, `no`).

### Example `docker-compose.yml` Structure:

```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/html:/usr/share/nginx/html
    networks:
      - app-network
    depends_on:
      - api

  api:
    build: ./api-service
    environment:
      - DB_HOST=database
      - DB_PORT=5432
    networks:
      - app-network
    depends_on:
      - database

  database:
    image: postgres:14
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=secret
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  db-data:
```

## 6.4 Building and Running Multi-Container Applications

Let's walk through an example of building and running a simple multi-container web application. We'll set up a static Nginx web server.

1.  **Create a Project Directory:**
    ```bash
    mkdir my-compose-app
    cd my-compose-app
    ```

2.  **Create an `index.html` file:**
    This will be served by Nginx.
    ```bash
    mkdir web
    echo "<h1>Hello from Docker Compose!</h1>" > web/index.html
    ```

3.  **Create a `docker-compose.yml` file:**
    In the `my-compose-app` directory, create a `docker-compose.yml` file with the following content:
    ```yaml
    # docker-compose.yml
    version: '3.8'
    services:
      webserver:
        image: nginx:latest
        ports:
          - "80:80"
        volumes:
          - ./web:/usr/share/nginx/html:ro  # Mount the local 'web' directory into Nginx's html directory
        container_name: my-compose-nginx
    ```
    *   `webserver`: This is the name of our service.
    *   `image: nginx:latest`: Uses the official Nginx Docker image.
    *   `ports: - "80:80"`: Maps host port 80 to container port 80.
    *   `volumes: - ./web:/usr/share/nginx/html:ro`: Mounts the `web` directory from the host (where `index.html` is) into the Nginx document root inside the container. `:ro` makes it read-only for the container.
    *   `container_name: my-compose-nginx`: Assigns a specific name to the container.

4.  **Build and Run the Application:**
    Navigate to the `my-compose-app` directory and run:
    ```bash
    docker compose up -d
    ```
    *   `up`: Builds, creates, starts, and attaches to containers for a service.
    *   `-d`: Runs containers in detached mode (in the background).

    Compose will:
    *   Check for the `nginx:latest` image. If not found, it will pull it.
    *   Create a default network for your project.
    *   Start the `webserver` container.

5.  **Verify the Application:**
    Open your web browser and go to `http://localhost`. You should see the "Hello from Docker Compose!" message.
    You can also check the running containers:
    ```bash
    docker ps
    ```
    You should see `my-compose-nginx` running.

## 6.5 Managing Compose Applications (start, stop, restart, scale, down)

Docker Compose provides a set of commands to manage the lifecycle of your multi-container applications.

*   **`docker compose up`:**
    *   Starts or restarts all services defined in the `docker-compose.yml`.
    *   If services don't exist, it creates them.
    *   `-d`: (detached mode) Runs containers in the background.
    *   `--build`: Rebuilds images if a `build` context is defined in the `docker-compose.yml`.

*   **`docker compose start`:**
    *   Starts existing stopped services.
    ```bash
    docker compose start
    ```

*   **`docker compose stop`:**
    *   Stops running services without removing them.
    ```bash
    docker compose stop
    ```

*   **`docker compose restart`:**
    *   Restarts all services.
    ```bash
    docker compose restart
    ```

*   **`docker compose ps`:**
    *   Lists the services (containers) associated with your Compose project.
    ```bash
    docker compose ps
    ```

*   **`docker compose logs`:**
    *   Displays log output from services.
    *   `-f`: (follow) Continuously stream the log output.
    ```bash
    docker compose logs -f
    ```

*   **`docker compose scale` (Deprecated in Compose V2 for `up --scale`):**
    *   In older Compose versions, `scale` was used. In Compose V2, use `docker compose up --scale <service_name>=<count>`.
    *   **Purpose:** Scales a service to a specified number of containers.
    *   **Example:** To scale the `webserver` service to 3 instances:
        ```bash
        docker compose up -d --scale webserver=3
        ```

*   **`docker compose down`:**
    *   Stops and removes containers, networks, and volumes (if defined as `external: false` or not explicitly marked as external) created by `docker compose up`.
    *   `-v`: Removes named volumes declared in the `volumes` section of the `docker-compose.yml`.
    *   `--rmi all`: Removes all images used by any service.
    ```bash
    docker compose down
    docker compose down -v # Removes volumes as well
    ```

## 6.6 Orchestrating a Simple Web Application (e.g., WordPress/MySQL)

Let's demonstrate a more complex example: deploying a WordPress application with a MySQL database using Docker Compose.

1.  **Create a Project Directory:**
    ```bash
    mkdir wordpress-app
    cd wordpress-app
    ```

2.  **Create a `docker-compose.yml` file:**
    ```yaml
    # docker-compose.yml for WordPress
    version: '3.8'

    services:
      db:
        image: mysql:8.0
        container_name: wordpress_db
        command: --default-authentication-plugin=mysql_native_password
        restart: always
        environment:
          MYSQL_ROOT_PASSWORD: root_password_secure
          MYSQL_DATABASE: wordpress
          MYSQL_USER: wordpressuser
          MYSQL_PASSWORD: wordpresspassword
        volumes:
          - db_data:/var/lib/mysql
        networks:
          - wordpress-network

      wordpress:
        image: wordpress:latest
        container_name: wordpress_app
        restart: always
        ports:
          - "80:80"
        environment:
          WORDPRESS_DB_HOST: db:3306 # 'db' is the service name for MySQL
          WORDPRESS_DB_USER: wordpressuser
          WORDPRESS_DB_PASSWORD: wordpresspassword
          WORDPRESS_DB_NAME: wordpress
        volumes:
          - wordpress_data:/var/www/html
        networks:
          - wordpress-network
        depends_on:
          - db # Ensures 'db' container starts before 'wordpress'

    networks:
      wordpress-network:
        driver: bridge

    volumes:
      db_data:    # Named volume for MySQL data persistence
      wordpress_data: # Named volume for WordPress application files
    ```
    *   **`db` service:** Uses the `mysql:8.0` image. Sets environment variables for the database name, user, and password. It mounts a named volume (`db_data`) for persistent storage of MySQL data.
    *   **`wordpress` service:** Uses the `wordpress:latest` image. Maps host port 80 to container port 80. Crucially, its `WORDPRESS_DB_HOST` environment variable points to the `db` service name, leveraging Docker Compose's internal DNS resolution. It also uses a named volume (`wordpress_data`) for its application files and content.
    *   **`networks`:** Defines a custom bridge network (`wordpress-network`) for the services to communicate.
    *   **`volumes`:** Defines two named volumes for data persistence.

3.  **Deploy the Application:**
    In the `wordpress-app` directory, run:
    ```bash
    docker compose up -d
    ```
    This will pull the `mysql` and `wordpress` images, create the network and volumes, and start both containers.

4.  **Access WordPress:**
    Once the containers are up and running (it might take a minute or two for MySQL to initialize), open your web browser and navigate to `http://localhost`. You should be greeted by the WordPress installation wizard.

5.  **Clean up:**
    When you are finished, stop and remove the application:
    ```bash
    docker compose down -v
    ```
    The `-v` flag is essential here to remove the named volumes, which contain your database and WordPress data. If you omit `-v`, the volumes will persist, and your data will remain if you bring the application up again later.

Docker Compose significantly streamlines the development and deployment of multi-container applications. By defining your entire stack in a single file, you gain consistency, reproducibility, and ease of management. This prepares you for more advanced Docker usage and orchestration discussed in later chapters.