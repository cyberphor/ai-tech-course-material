# Dockerfile metadata
FROM python:3.9-alpine3.13 
LABEL Author="Victor Fernandez III, @cyberphor"

# Set the working directory
WORKDIR /opt/simplellm/

# Install llama-cpp-python requirements and update pip
RUN apk update &&\
    apk add g++ gcc libc-dev linux-headers musl-dev python3-dev &&\
    python -m pip install --upgrade pip 

# Download Python dependencies and the Rocket-3B Machine Learning model from HuggingFace
RUN python -m pip install flask llama-cpp-python locust waitress wonderwords &&\
    wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q2_K.gguf

# Copy the application's Python project file and source code
COPY src/pyproject.toml src/pyproject.toml
COPY src/simplellm.py src/simplellm.py

# Run the application
CMD [ "waitress-serve", "src.simplellm:app" ]