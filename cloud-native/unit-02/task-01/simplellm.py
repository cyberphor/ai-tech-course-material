"""A simple Large Language Model (LLM) module"""
from llama_cpp import Llama
from flask import Flask
from flask import request

MODEL_PATH = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
N_CTX = 512
N_BATCH = 1
TEMPERATURE = 0.0
MAX_TOKENS = None

llm = Llama(model_path=MODEL_PATH, n_ctx=N_CTX, n_batch=N_BATCH)
app = Flask(__name__)

@app.route("/healthcheck")
def healthcheck():
    return "OK"

@app.route("/api")
def api():
    """"API Function"""
    system_message = "You are a helpful assistant."
    prompt = request.args.get("message")
    template = f"<|system|>\n{system_message}</s>\n<|user|>{prompt}</s><|assistant|>"
    return llm(template, temperature=TEMPERATURE, max_tokens=MAX_TOKENS)
