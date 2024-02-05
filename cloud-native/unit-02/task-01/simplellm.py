"""A simple Large Language Model (LLM) module"""
from llama_cpp import Llama
from flask import Flask

MODEL_PATH = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
N_CTX = 512
N_BATCH = 1
TEMPERATURE = 0.0
MAX_TOKENS = None

app = Flask(__name__)

@app.route("/healthcheck")
def healthcheck():
    return "OK"

@app.route("/api")
def api():
    """"API Function"""
    llm = Llama(MODEL_PATH, N_CTX, N_BATCH)
    system_message = "You are a helpful assistant."
    prompt = "What is love?"
    template = f"<|system|>\n{system_message}</s>\n<|user|>{prompt}</s><|assistant|>"
    return llm(template, TEMPERATURE, MAX_TOKENS)
