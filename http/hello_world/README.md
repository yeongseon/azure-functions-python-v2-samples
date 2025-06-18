# 🚀 hello_world - HTTP Trigger Function

This is a simple Azure Functions HTTP Trigger written in Python using the `FunctionApp` SDK style (`@app.route`).  
It returns a personalized greeting if a `name` is provided via query string or JSON body.

---

## 📂 Directory Structure

```
hello_world/
├── __init__.py             # Main function code
├── function.json           # Azure Functions trigger configuration (auto-generated)
├── host.json               # Function host configuration
├── requirements.txt        # Python dependencies
└── local.settings.json     # Local development settings
```

---

## ▶️ How It Works

- Route: `GET /api/hello_world?name=YourName`
- Or: `POST /api/hello_world` with JSON `{ "name": "YourName" }`
- If no name is provided, returns a default greeting.

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

### 3. Start the function app locally

```bash
func start
```

---

## 🧪 Test Endpoints

### ✅ GET request

```bash
curl "http://localhost:7071/api/hello_world?name=Yeongseon"
```

**Response:**

```
Hello, Yeongseon!
```

---

### ✅ POST request

```bash
curl -X POST http://localhost:7071/api/hello_world \
     -H "Content-Type: application/json" \
     -d '{"name": "Yeongseon"}'
```

**Response:**

```
Hello, Yeongseon!
```

---

## 📝 Source Code (init.py)

```python
import azure.functions as func
import logging

app = func.FunctionApp()

@app.route(route="hello_world", auth_level=func.AuthLevel.ANONYMOUS)
def hello_world(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing hello_world request.")

    name = req.params.get("name") or (req.get_json().get("name") if req.method == "POST" else None)

    message = f"Hello, {name}!" if name else "Hello from Azure Functions!"
    return func.HttpResponse(message)
```

---

## 📦 Deployment (Azure CLI)

```bash
func azure functionapp publish <your-function-app-name>
```

---

## 📚 Related

- Azure Functions Python Docs: https://learn.microsoft.com/azure/azure-functions/functions-reference-python
