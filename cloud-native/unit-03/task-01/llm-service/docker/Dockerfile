FROM ubuntu:22.04

WORKDIR /app
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install build-essential wget python3 python3-pip -y && wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q2_K.gguf

COPY ../dist/simplellm-1.0.0-py2.py3-none-any.whl ./simplellm-1.0.0-py2.py3-none-any.whl

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

RUN pip install --no-cache-dir simplellm-1.0.0-py2.py3-none-any.whl

CMD pip install llama-cpp-python && waitress-serve --call 'simplellm:create_app'