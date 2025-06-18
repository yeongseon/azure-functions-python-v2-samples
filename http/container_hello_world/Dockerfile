# Use the official Azure Functions Python 3.12 base image
FROM mcr.microsoft.com/azure-functions/python:4-python3.12

# Set environment variables for Azure Functions
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true \
    FUNCTIONS_WORKER_RUNTIME=python \
    PYTHON_ISOLATE_WORKER_DEPENDENCIES=1

# Install SSH and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends dialog openssh-server && \
    echo "root:Docker!" | chpasswd && \
    mkdir /var/run/sshd

# Copy SSH config and entry script
COPY sshd_config /etc/ssh/sshd_config
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy function application code
COPY . /home/site/wwwroot

# Expose ports: 80 for HTTP, 2222 for SSH
EXPOSE 80 2222

# Start the SSH server and Azure Functions host
ENTRYPOINT ["/entrypoint.sh"]
