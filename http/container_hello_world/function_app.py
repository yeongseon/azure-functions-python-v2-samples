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
