import azure.functions as func
import azure.durable_functions as df

# Create a Durable Functions app instance (HTTP trigger authentication: Anonymous)
app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# HTTP trigger function - Starts the orchestration via HTTP POST request
@app.route(route="orchestrators/{functionName}", methods=["POST"])
@app.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    # Get orchestrator function name from the route parameter
    orchestrator_name = req.route_params.get("functionName")
    # Start a new orchestration instance
    instance_id = await client.start_new(orchestrator_name)
    # Return a response with status query URLs (202 Accepted)
    return client.create_check_status_response(req, instance_id)


# Orchestrator function - Calls an activity function and collects result
@app.orchestration_trigger(context_name="context")
def hello_orchestrator(context: df.DurableOrchestrationContext):
    # Call the activity function 'hello' with input "Seoul"
    result = yield context.call_activity("hello", "Seoul")
    # Return the result from the activity function
    return result


# Activity function - Generates a greeting message
@app.activity_trigger(input_name="name")
def hello(name: str) -> str:
    return f"Hello {name}!"
