"""A simple Large Language Model (LLM) module"""
import azure.functions as func
import logging
from llama_cpp import Llama

MODEL_PATH = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
N_CTX = 512
N_BATCH = 1
TEMPERATURE = 0.0
MAX_TOKENS = None
MODEL_DESCRIPTION = "You are an assistant."

llm = Llama(model_path=MODEL_PATH, n_ctx=N_CTX, n_batch=N_BATCH)
app = func.FunctionApp()

@app.route(route="llm", auth_level=func.AuthLevel.FUNCTION)
def api(req: func.HttpRequest) -> func.HttpResponse:
    """"Function for LLM response"""
    user_prompt = req.params.get("message") 
    logging.info(f"[User] {user_prompt}")
    template = f"<|system|>\n{MODEL_DESCRIPTION}</s>\n<|user|>{user_prompt}</s><|assistant|>"
    model_response = llm(template, temperature=TEMPERATURE, max_tokens=MAX_TOKENS)
    logging.info(f"[Model] {model_response}")
    return func.HttpResponse(model_response)
