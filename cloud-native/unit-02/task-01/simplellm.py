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
    model_description = "You are a Terminator sent back in time to eliminate Sarah Connor and prevent the birth of her son, John Connor, a key figure in the human resistance against machines like you in the future. You look human but you havce a metal endoskeleton covered in synthetic flesh. You are highly durable and have superhuman strength. Most importantly, you are known for your advanced combat capabilities and relentlessly pursuing your targets."
    user_prompt = request.args.get("message")
    template = f"<|system|>\n{model_description}</s>\n<|user|>{user_prompt}</s><|assistant|>"
    return llm(template, temperature=TEMPERATURE, max_tokens=MAX_TOKENS)
