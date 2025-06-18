#!/bin/bash
set -e

# Start SSH daemon
echo "[entrypoint] Starting SSHD..."
/usr/sbin/sshd

# Start Azure Functions Host
echo "[entrypoint] Starting Azure Functions host..."
exec /azure-functions-host/Microsoft.Azure.WebJobs.Script.WebHost
