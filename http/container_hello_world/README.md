# 🚀 container_hello_world - Container-based HTTP Trigger Function

This is a containerized Azure Functions HTTP Trigger written in Python using the `FunctionApp` SDK style (`@app.route`).  
It returns a personalized greeting if a `name` is provided via query string or JSON body.  
Additionally, the container includes an SSH server for debugging purposes (port 2222).

---

## 📂 Directory Structure

```
container_hello_world/
├── Dockerfile              # Custom container definition
├── README.md               # Project documentation
├── entrypoint.sh           # Entrypoint script to launch SSHD + Azure Functions
├── function_app.py         # Python code for the HTTP-triggered Azure Function
├── host.json               # Host-level configuration
├── local.settings.json     # Local development settings
├── requirements.txt        # Python dependencies
└── sshd_config             # SSH server configuration
```

---

## ▶️ How It Works

- Route: `GET /api/container_hello_world?name=YourName`
- Or: `POST /api/container_hello_world` with JSON `{ "name": "YourName" }`
- If no name is provided, returns a default greeting.

---

## 💻 Local Development with Docker

### 1. Build the Docker image

```bash
docker build -t container-hello-world .
```

### 2. Run the container

```bash
docker run -p 8080:80 -p 2222:2222 container-hello-world
```

### 3. Test HTTP function

```bash
curl "http://localhost:8080/api/container_hello_world?name=Yeongseon"
```

### 4. SSH Access (for debugging)

```bash
ssh root@localhost -p 2222
# password: Docker!
```

> ⚠️ Note: SSH is for local development use only. Do not expose in production.

---

## 📝 Source Code (function_app.py)

```python
import azure.functions as func
import logging

app = func.FunctionApp()

@app.route(route="container_hello_world", auth_level=func.AuthLevel.ANONYMOUS)
def container_hello_world(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing container_hello_world request.")

    name = req.params.get("name") or (req.get_json().get("name") if req.method == "POST" else None)
    message = f"Hello, {name}!" if name else (
        "This HTTP triggered function executed successfully. "
        "Pass a name in the query string or in the request body for a personalized response."
    )

    return func.HttpResponse(message)
```

---

## 📦 Deployment (Custom Container)

You can deploy this container to Azure Functions using the **Custom Container** method:

- Azure CLI:  
  ```bash
  az functionapp create --name <APP_NAME> --storage-account <STORAGE_NAME> \
      --resource-group <RESOURCE_GROUP> --plan <APP_SERVICE_PLAN> \
      --deployment-container-image-name <ACR_LOGIN_SERVER>/container-hello-world:latest
  ```

---

## 📚 Related

- Azure Functions Custom Containers: https://learn.microsoft.com/azure/azure-functions/functions-custom-containers
- Python Developer Guide: https://learn.microsoft.com/azure/azure-functions/functions-reference-python


---

## 🐳 Dockerfile Overview

This project uses the official Azure Functions Python 3.12 image:  
`mcr.microsoft.com/azure-functions/python:4-python3.12`

### Key Build Steps

| Step | Description |
|------|-------------|
| `ENV` | Sets up environment variables required by Azure Functions runtime (e.g., `FUNCTIONS_WORKER_RUNTIME=python`) |
| `apt-get install` | Installs OpenSSH server and sets root password (`Docker!`) for local SSH access |
| `COPY sshd_config` | Adds a custom SSH configuration file that enables root login and password authentication |
| `COPY entrypoint.sh` | Adds an entrypoint script that starts both the SSH server and the Azure Functions host |
| `EXPOSE` | Exposes port `80` for HTTP and `2222` for SSH access |
| `ENTRYPOINT` | Runs the `entrypoint.sh` script to start the SSH daemon and the Azure Functions runtime |

> ⚠️ **Warning**: SSH access is intended for local development only. Do not use this configuration in production environments without securing access.



---

## 🐳 Docker Support in This Project

This project packages an Azure Function inside a custom Docker image, enabling enhanced flexibility such as local SSH access, custom dependencies, and isolated runtime environments.

### 🔧 Dockerfile Breakdown

The `Dockerfile` performs the following steps:

| Step | Purpose |
|------|---------|
| `FROM mcr.microsoft.com/azure-functions/python:4-python3.12` | Base image provided by Microsoft for running Python 3.12 Azure Functions |
| `ENV ...` | Configures environment variables for Azure Functions runtime |
| `RUN apt-get install ...` | Installs `openssh-server` and sets root password for SSH access |
| `COPY sshd_config` | Provides custom SSH configuration to allow password login |
| `COPY entrypoint.sh` | Script that starts both SSH and Azure Functions host processes |
| `COPY . /home/site/wwwroot` | Copies function app files into the container’s expected directory |
| `EXPOSE 80 2222` | Exposes HTTP (80) and SSH (2222) ports |
| `ENTRYPOINT ["/entrypoint.sh"]` | Launches SSHD and the Azure Functions runtime together |

---

## 🏗️ Docker Build and Run

You can build and run the container locally using the following steps:

```bash
# Build the Docker image
docker build -t container-hello-world .

# Run the container, exposing necessary ports
docker run -p 8080:80 -p 2222:2222 container-hello-world
```

Once running:
- Function endpoint: `http://localhost:8080/api/container_hello_world`
- SSH access: `ssh root@localhost -p 2222` (password: `Docker!`)

> 🛑 SSH is enabled only for development. Do not expose port 2222 in production.

---

## 🚀 Deployment to Azure (with Custom Container)

To deploy this containerized function app to Azure:

1. Push your image to a container registry (e.g., Azure Container Registry):

```bash
# Tag your image
docker tag container-hello-world <ACR_LOGIN_SERVER>/container-hello-world:latest

# Log in and push
az acr login --name <ACR_NAME>
docker push <ACR_LOGIN_SERVER>/container-hello-world:latest
```

2. Create an Azure Function App with a custom container:

```bash
az functionapp create --name <APP_NAME> \
    --resource-group <RESOURCE_GROUP> \
    --plan <APP_SERVICE_PLAN> \
    --storage-account <STORAGE_ACCOUNT> \
    --deployment-container-image-name <ACR_LOGIN_SERVER>/container-hello-world:latest
```

> Ensure that your App Service Plan supports Linux and custom containers.

---

## 📖 Additional Tips

- You can customize startup behavior in `entrypoint.sh`
- For production, consider disabling SSH or using more secure mechanisms (e.g., certificate-based login)
- Monitor logs with `az functionapp log stream --name <APP_NAME> --resource-group <RESOURCE_GROUP>`

