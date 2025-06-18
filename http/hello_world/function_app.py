import azure.functions as func
import logging

app = func.FunctionApp()


@app.route(route="hello_world", auth_level=func.AuthLevel.ANONYMOUS)
def HelloWorld(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing HelloWorld request.")

    name = req.params.get("name") or (
        req.get_json().get("name") if req.method == "POST" else None
    )

    message = f"Hello, {name}!" if name else "Hello from Azure Functions!"
    return func.HttpResponse(message)
