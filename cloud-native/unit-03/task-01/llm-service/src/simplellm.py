from flask import Flask, request
from llama_cpp import Llama


def get_llm_response(message, llm):
    system_message = "You are a helpful assistant."
    prompt = message
    template = f"""<|system|>
    {system_message}</s>
    <|user|>
    {prompt}</s>
    <|assistant|>"""
    return llm(template, temperature=0.0, max_tokens=128)



def create_app():

    app = Flask(__name__)
    print("Loading tinyllama model...")
    llm = Llama(model_path="tinyllama-1.1b-chat-v1.0.Q2_K.gguf", n_ctx=512, n_batch=1)

    @app.route('/api')
    def send_llm_response():
        message = request.args.get("message")
        return get_llm_response(message, llm)
    

    @app.route('/healthcheck')
    def healthcheck():
        return "OK"
    
    return app