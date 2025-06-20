# 🚀 durable\_http\_orchestrator - Durable Function v2 (HTTP Trigger)

This is a minimal example of an **Azure Durable Function v2** written in Python using the **@app.route**, **@app.orchestration\_trigger**, and **@app.activity\_trigger** decorators. It runs locally and orchestrates a greeting message.

---

## 📂 Directory Structure

```
durable/
└── http_orchestrator/
    ├── function_app.py          # Main Durable Functions code
    ├── host.json                # Azure Functions host configuration
    ├── local.settings.json      # Local development settings (Azurite)
    ├── requirements.txt         # Python dependencies
    └── README.md                # This documentation
```

---

## ▶️ How It Works

* **Route:** `POST /api/orchestrators/hello_orchestrator`
* Starts a Durable orchestration instance that calls an activity named `hello`
* The `hello` activity returns a greeting like `Hello Seoul!`

---

## 💻 Local Development

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Azurite (storage emulator)

```bash
docker run -p 10000:10000 -p 10001:10001 -p 10002:10002 \
       mcr.microsoft.com/azure-storage/azurite
```

### 4. Start the function app locally

```bash
func start
```

You should see:

```
Functions:
    http_start: [POST] http://localhost:7071/api/orchestrators/hello_orchestrator
```

---

## 🧪 Test the Orchestration

### ✅ Start via HTTP POST

```bash
curl -X POST http://localhost:7071/api/orchestrators/hello_orchestrator
```

**Response:** JSON with instance ID and status URLs

### ✅ Check Orchestration Status

Use the `statusQueryGetUri` from the response, or:

```bash
curl http://localhost:7071/runtime/webhooks/durabletask/instances/<instanceId>?taskHub=TestHubName&connection=Storage
```

**Expected Output:**

```json
{
  "runtimeStatus": "Completed",
  "output": "Hello Seoul!"
}
```

---

## 📝 Source Code (function\_app.py)

```python
import azure.functions as func
import azure.durable_functions as df

app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="orchestrators/{functionName}", methods=["POST"])
@app.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    orchestrator_name = req.route_params.get('functionName')
    instance_id = await client.start_new(orchestrator_name)
    return client.create_check_status_response(req, instance_id)

@app.orchestration_trigger(context_name="context")
def hello_orchestrator(context: df.DurableOrchestrationContext):
    result = yield context.call_activity("hello", "Seoul")
    return result

@app.activity_trigger(input_name="name")
def hello(name: str) -> str:
    return f"Hello {name}!"
```

---

## 📦 Dependencies (requirements.txt)

```txt
azure-functions
azure-functions-durable
```

---

## 📚 References

* Azure Functions Durable (Python): [https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-python-v2](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-python-v2)
* Azurite Emulator: [https://github.com/Azure/Azurite](https://github.com/Azure/Azurite)
