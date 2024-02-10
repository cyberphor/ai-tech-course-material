"""A simple Large Language Model (LLM) module"""
import logging
from azure.functions import AuthLevel
from azure.functions import FunctionApp
from azure.functions import HttpRequest
from azure.functions import HttpResponse
from llama_cpp import Llama

MODEL_PATH = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
N_CTX = 512
N_BATCH = 1
TEMPERATURE = 0.0
MAX_TOKENS = None
MODEL_DESCRIPTION = "You are an assistant."

model = Llama(model_path=MODEL_PATH, n_ctx=N_CTX, n_batch=N_BATCH)
app = FunctionApp()

@app.route(route="healthcheck", auth_level=AuthLevel.ANONYMOUS)
def healthcheck(req: HttpRequest) -> HttpResponse:
    logging.info(f"[User] {req}")
    return HttpResponse("OK\n")

@app.route(route="llm", auth_level=AuthLevel.ANONYMOUS)
def llm(req: HttpRequest) -> HttpResponse:
    """"Function for LLM response"""
    user_prompt = req.params.get("message") 
    logging.info(f"[User] {user_prompt}")
    template = f"<|system|>\n{MODEL_DESCRIPTION}</s>\n<|user|>{user_prompt}</s><|assistant|>"
    model_response = str(model(template, temperature=TEMPERATURE, max_tokens=MAX_TOKENS))
    logging.info(f"[Model] {model_response}")
    return HttpResponse(model_response)