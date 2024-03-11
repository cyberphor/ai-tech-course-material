# Dockerfile metadata
FROM python:3.10-alpine3.13 
LABEL Author="Victor Fernandez III, @cyberphor"

# set the working directory
WORKDIR /opt/simplellm/

# download Python dependencies and a Large Language Model (LLM) from HuggingFace
RUN wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q2_K.gguf

# install LLM (i.e., llama-cpp-python) dependencies and install poetry
RUN apk update &&\
    apk add g++ gcc libc-dev linux-headers musl-dev python3-dev &&\
    pip install poetry

# configure poetry to install dependencies globally
ENV POETRY_VIRTUALENVS_CREATE=false

# copy the project's files to the current working directory
COPY fastapi-p4/pyproject.toml pyproject.toml
COPY fastapi-p4/poetry.lock poetry.lock
COPY fastapi-p4/fastapi_p4/llmserver.py llmserver.py

# install the project's dependencies
RUN poetry install

# start the LLM (an ASGI application) via uvicorn (an ASGI server)
CMD ["uvicorn", "llmserver:app", "--host", "0.0.0.0", "--port", "80"]