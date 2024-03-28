# Cloud Native: Inter-Service Communication
* [References](#references)
* [Notes](#notes)
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)
* [Task 03](#task-03)
* [Task 04](#task-04)

## References
If I find any helpful references, I will put them here. 
* [gRPC vs. REST: Key Similarities and Differences](https://blog.dreamfactory.com/grpc-vs-rest-how-does-grpc-compare-with-traditional-rest-apis/)
* [grpc.io: Python - Quick Start](https://grpc.io/docs/languages/python/quickstart/)
* [Protocol Buffers Documentation: JSON Mapping](https://protobuf.dev/programming-guides/proto3/#json)

## Notes
**Web Server Gateway Interfaces**  
Web Server Gateway Interfaces (WSGI) process requests one at a time. Flask is an example of a WSGI application.

**Asynchronous Server Gateway Interface**  
Asynchronous Server Gateway Interfaces (ASGI) can process multiple requests at the same time. FastAPI is an example of a ASGI application.

**pip**  
`pip` is a package manager for Python.

**pipx**  
`pipx` is also a package manager for Python. Yet, it can install Python packages in isolated environments (this is ideal for programs used by multiple users working on the same machine).

**venv**  
`venv` is used to create virtual environments. Virtual environments help avoid package version conflicts. 

**Poetry**  
Poetry is another package manager that can install Python packages in isolated environments. Yet, unlike `pipx`, Poetry can also handle dependency resolution, package version locking, or package publishing. Package managers like Poetry and Cargo (the package manager for the Rust programming language) create "source" and "test" folders because they assume your codebase will include unit tests. If you want to configure Poetry to create your virtual environment near your code, add a file called `poetry.toml` to your project folder (see below for what to add to this file). Once you've added Python packages to your project's `pyproject.toml` file (NOT the `poetry.toml` file), others can replicate your development setup by downloading your code and then running `poetry install`.

**gRPC**  
Google Remote Procedure Call (gRPC) is a protocol used for inter-service communication. gRPC uses *protocol buffers* for its messaging format (aka interface definition language) and HTTP 2 for transport. In contrast, REST APIs uses JSON and HTTP 1.1.

**Serialization**  
Serialization is the process of converting a language object (e.g., Python dict) into a series of bytes. Examples of technology that use serialization are Pickle and gRPC.

**Protocol Buffer**  
A protocol buffer is a method of serialization. Protocol buffers are defined using `.proto` files.

## Setup
The tasks prescribed within this README assume you're already working in a Linux environment (Windows Subsystem for Linux, Azure Shell, GitHub Codespaces, a VirtualBox-based Linux virtual machine, etc.). They also assume you already have the following software installed: Python, Azure CLI, Kubernetes, and Helm.

**Step 1.** Install `pipx`.  
```bash
python -m pip install pipx
```

**Step 2.** Install Poetry using `pipx`. 
```bash
pipx install poetry
``` 

**Step 3.** Create a Python project using Poetry. FYI, this command will also create a file called `pyproject.toml` among other things.
```bash
poetry new fastapi-p4
```

**Step 4.** Change directories to your project folder. 
```bash
cd fastapi-p4/
```

**Step 6.** Create and open a file called `poetry.toml`. 
```bash
vim poetry.toml
```

**Step 7.** Add the code below to the `poetry.toml` file. 
```yaml
[virtualenvs]
in-project = true
path = ".venv"
```

**Step 8.** Add the Python packages you need to the `pyproject.toml` file and then install them. 
```bash
poetry add fastapi gunicorn llama-cpp-python uvicorn[standard]
```

**Step 9.** Download the Machine Learning (ML) model mentioned throughout this README to your project folder. 
```bash
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q2_K.gguf
```

For example, your current working directory should look like this after you download the ML model.
```bash
total 471900
-rw-rw-rw-  1 codespace codespace         0 Mar 11 13:55 README.md
drwxrwxrwx+ 3 codespace codespace      4096 Mar 11 14:32 fastapi_p4
-rw-rw-rw-  1 codespace codespace     83429 Mar 11 14:04 poetry.lock
-rw-rw-rw-  1 codespace codespace        47 Mar 11 13:59 poetry.toml
-rw-rw-rw-  1 codespace codespace       428 Mar 11 14:04 pyproject.toml
drwxrwxrwx+ 2 codespace codespace      4096 Mar 11 13:55 tests
-rw-rw-rw-  1 codespace codespace 483116416 Dec 31 20:53 tinyllama-1.1b-chat-v1.0.Q2_K.gguf
```

## Task 01
### Subtask 01
**Step 1.** Create and open a file called `llmserver.py` in the `fastapi_p4` child folder (notice the `_` in the child folder's name versus the `-` in the parent folder's name). 
```bash
vim fastapi_p4/llmserver.py
```

**Step 2.** Add the code below to the `llmserver.py` file.
```python
"""
A module for an Large Language Model (LLM). 
"""
# import third-party modules
from fastapi import FastAPI
from llama_cpp import Llama

# declare and initialize a variable called "app" by assigning a FastAPI object to it
# to run this FastAPI application via "uvicorn" use:
#     poetry run uvicorn fastapi_p4.llmserver:app --reload
# if name the variable something else, make sure to update the "uvicorn" command you use
# for example, if you called this variable "foo" your "uvicorn" command would be:
#     poetry run uvicorn fastapi_p4.llmserver:foo --reload
app = FastAPI()

# declare and initialize a variable called "model" by assigning a Llama object to it
model = Llama(
    model_path="tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
    n_ctx=512,
    n_batch=1
)


# add a HTTP route, with an endpoint called "/healthcheck", to the FastAPI app 
@app.get("/healthcheck")
async def healthcheck():
    """
    Function to check if the FastAPI app is running
    """
    return "OK"

# add a HTTP route, with an endpoint called "/api", to the FastAPI FastAPI app
@app.get("/api")
async def api(message: str):
    """
    Function to implement the Large Language Model's (LLM) Application Programming Interface (API)
    """
    model_description = "You are an assistant."
    request = f"<|system|>\n{model_description}</s>\n<|user|>{message}</s><|assistant|>"
    response = model(request, temperature=0.0, max_tokens=128)
    return response
```

**Step 3.** Run your ML model using Poetry and the `uvicorn` ASGI web server. FYI, your ML model is now an ASGI application instead of WSGI application because we swapped out Flask for FastAPI. Using FastAPI makes your code an ASGI application (meaning it can handle multiple requests at the same time). Using the `--reload` option means `uvicorn` will reload itself whenever it detects changes to your code. This means you don't have to manually restart it after you make an update. 
```bash
poetry run uvicorn fastapi_p4.llmserver:app --reload
```

**Step 4.** Using a different terminal window, verify your FastAPI app is running.
```bash
curl http://localhost:8000/healthcheck
```

**Step 5.** Using a different terminal window, verify your ML model is working as intended.
```bash
curl http://localhost:8000/api?message=hi
```

### Subtask 02
**Step 1.** Open the file called `llmserver.py` in the `fastapi_p4` child folder. 
```bash
vim fastapi_p4/llmserver.py
```

**Step 2.** Replace the contents of the `llmserver.py` file with the updated code below.
```python
"""
A module for an Large Language Model (LLM). 
"""
# import third-party modules
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Query
from fastapi.exceptions import RequestValidationError
from llama_cpp import Llama
from pydantic import BaseModel
from pydantic import validator

# declare and initialize a variable called "app" by assigning a FastAPI object to it
# to run this FastAPI application via "uvicorn" use:
#     poetry run uvicorn fastapi_p4.llmserver:app --reload
# if name the variable something else, make sure to update the "uvicorn" command you use
# for example, if you called this variable "foo" your "uvicorn" command would be:
#     poetry run uvicorn fastapi_p4.llmserver:foo --reload
app = FastAPI()

# declare and initialize a variable called "model" by assigning a Llama object to it
model = Llama(
    model_path="tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
    n_ctx=512,
    n_batch=1
)

# set the max number of tokens allowed for each LLM prompt 
MAX_TOKENS = 512

# create a class called "LLMRequest" to represent each request sent to the LLM 
class LLMRequest(BaseModel):
    """
    Represents requests sent to the Large Language Model (LLM)
    """
    # declare a property called "message" for the "LLMRequest" class and initialize it using a Query object
    # the "message" property will be whatever is passed via the "message" field
    message: str = Query("message")

    # the "cls" parameter is the "LLMRequest" class
    # the "v" parameter is the "message" property
    @validator("message")
    def check_message(cls, v) -> str:
        """
        Checks if the request exceeds the maximum token count    
        """
        # if the number of "tokens" used exceeds what is allowed, throw an error 
        tokens = len(model.tokenize(v.encode("utf-8")))
        if tokens >= MAX_TOKENS:
            raise RequestValidationError(f"Token count exceeds the maximum allowed limit of 512.")
        # otherwise return what was passed via the "message" field
        return v

# add a HTTP route, with an endpoint called "/healthcheck", to the FastAPI app 
@app.get("/healthcheck")
async def healthcheck():
    """
    Function to check if the FastAPI app is running
    """
    return "OK"

# add a HTTP route, with an endpoint called "/api", to the FastAPI FastAPI app
@app.get("/api")
async def api(message: LLMRequest = Depends(LLMRequest)):
    """
    Function to implement the Large Language Model's (LLM) Application Programming Interface (API)
    """
    model_description = "You are an assistant."
    request = f"<|system|>\n{model_description}</s>\n<|user|>{message}</s><|assistant|>"
    response = model(request, temperature=0.0, max_tokens=MAX_TOKENS)
    return response
```

**Step 3.** Using a different terminal window, verify your ML model rejects prompts that are too long.
```bash
curl http://localhost:8000/api?message=BeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBeeBoBopBee
```

```json
{"detail":"Token count exceeds the maximum allowed limit of 512."}
```

### Subtask 3
**Step 1.** Open the file called `llmserver.py` in the `fastapi_p4` child folder.
```bash
vim fastapi_p4/llmserver.py
```

**Step 2.** Replace the contents of the `llmserver.py` file with the updated code below.
```python
"""
A module for an Large Language Model (LLM). 
"""
# import built-in modules
from typing import Optional
from typing import List

# import third-party modules
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Query
from fastapi.exceptions import RequestValidationError
from llama_cpp import Llama
from pydantic import BaseModel
from pydantic import validator

# declare and initialize a variable called "app" by assigning a FastAPI object to it
# to run this FastAPI application via "uvicorn" use:
#     poetry run uvicorn fastapi_p4.llmserver:app --reload
# if name the variable something else, make sure to update the "uvicorn" command you use
# for example, if you called this variable "foo" your "uvicorn" command would be:
#     poetry run uvicorn fastapi_p4.llmserver:foo --reload
app = FastAPI()

# declare and initialize a variable called "model" by assigning a Llama object to it
model = Llama(
    model_path="tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
    n_ctx=512,
    n_batch=1
)

# set the max number of tokens allowed for each LLM prompt 
MAX_TOKENS = 512

# create a class called "LLMRequest" to represent each request sent to the LLM 
class LLMRequest(BaseModel):
    """
    Represents requests sent to the Large Language Model (LLM)
    """
    # declare a property called "message" for the "LLMRequest" class and initialize it using a Query object
    # the "message" property will be whatever is passed via the "message" field
    message: str = Query("message")

    # the "cls" parameter is the "LLMRequest" class
    # the "v" parameter is the "message" property
    @validator("message")
    def check_message(cls, v) -> str:
        """
        Checks if the request exceeds the maximum token count    
        """
        # if the number of "tokens" used exceeds what is allowed, throw an error 
        tokens = len(model.tokenize(v.encode("utf-8")))
        if tokens >= MAX_TOKENS:
            raise RequestValidationError(f"Token count exceeds the maximum allowed limit of 512.")
        # otherwise return what was passed via the "message" field
        return v

# create a class called "LLMChoices" to describe LLM choices
class LLMChoices(BaseModel):
    """
    Represents Large Language Model (LLM) choices
    """
    text: str = "Beep boop"
    index: int = 0
    logprobs: Optional[str] = "null"
    finish_reason: str = "stop"

# create a class called "LLMUsage" to describe LLM token usage
class LLMUsage(BaseModel):
    """
    Represents Large Language Model (LLM) token usage
    """
    prompt_tokens: int = 198
    completion_tokens: int = 10
    total_tokens: int = 208

# create a class called "BaseLlamaResponse" to represent each response from the LLM 
class BaseLlamaResponse(BaseModel):
    """
    Represents responses from the Large Language Model (LLM)
    """
    id: str = "cmpl-7fc1be4c-8f5b-4b2f-805f-f8c5086a9fb4"
    object: str = "text_completion"
    created: int = 1708459650
    model: str = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
    choices: List[LLMChoices]
    usage: LLMUsage

# add a HTTP route, with an endpoint called "/healthcheck", to the FastAPI app 
@app.get("/healthcheck")
async def healthcheck():
    """
    Function to check if the FastAPI app is running
    """
    return "OK"

# add a HTTP route, with an endpoint called "/api", to the FastAPI FastAPI app
@app.get("/api", response_model=BaseLlamaResponse)
async def api(message: LLMRequest = Depends(LLMRequest)):
    """
    Function to implement the Large Language Model's (LLM) Application Programming Interface (API)
    """
    model_description = "You are an assistant."
    request = f"<|system|>\n{model_description}</s>\n<|user|>{message}</s><|assistant|>"
    response = model(request, temperature=0.0, max_tokens=MAX_TOKENS)
    return response
```

**Step 3.** Using a different terminal window, verify your ML model is still working as intended. 
```bash
curl http://localhost:8000/api?message=hi
```

### Subtask 04
**Step 1.** Add the `mypy` Python package to your project as a development dependency. Doing this allows you to use `mypy` while ensuring it's not added to your production-specific `pyproject.toml` when you publish your project later.  
```bash
poetry add -G dev mypy
```

**Step 2.** Run `mypy` using Poetry. It will identified a number of issues to fix. 
```bash
poetry run mypy -p fastapi_p4 --strict
```

**Step 3.** Open the file called `llmserver.py` in the `fastapi_p4` child folder. 
```bash
vim fastapi_p4/llmserver.py
```

**Step 4.** Replace the contents of the `llmserver.py` file with the updated code below. 
```python
"""
A module for an Large Language Model (LLM). 
"""
# import built-in modules
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union

# import third-party modules
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Query
from fastapi.exceptions import RequestValidationError
from llama_cpp import Llama
from llama_cpp import CreateCompletionResponse
from pydantic import BaseModel
from pydantic import validator

# declare and initialize a variable called "app" by assigning a FastAPI object to it
# to run this FastAPI application via "uvicorn" use:
#     poetry run uvicorn fastapi_p4.llmserver:app --reload
# if name the variable something else, make sure to update the "uvicorn" command you use
# for example, if you called this variable "foo" your "uvicorn" command would be:
#     poetry run uvicorn fastapi_p4.llmserver:foo --reload
app = FastAPI()

# declare and initialize a variable called "model" by assigning a Llama object to it
model = Llama(
    model_path="tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
    n_ctx=512,
    n_batch=1
)

# set the max number of tokens allowed for each LLM prompt 
MAX_TOKENS = 512

# create a class called "LLMRequest" to represent each request sent to the LLM 
class LLMRequest(BaseModel):
    """
    Represents requests sent to the Large Language Model (LLM)
    """
    # declare a property called "message" for the "LLMRequest" class and initialize it using a Query object
    # the "message" property will be whatever is passed via the "message" field
    message: str = Query("message")

    # the "cls" parameter is the "LLMRequest" class
    # the "v" parameter is the "message" property
    @validator("message")
    def check_message(cls: LLMRequest, v: str) -> str:
        """
        Checks if the request exceeds the maximum token count    
        """
        # if the number of "tokens" used exceeds what is allowed, throw an error 
        tokens = len(model.tokenize(v.encode("utf-8")))
        if tokens >= MAX_TOKENS:
            raise RequestValidationError(f"Token count exceeds the maximum allowed limit of 512.")
        # otherwise return what was passed via the "message" field
        return v

# create a class called "LLMChoices" to describe LLM choices
class LLMChoices(BaseModel):
    """
    Represents Large Language Model (LLM) choices
    """
    text: str = "Beep boop"
    index: int = 0
    logprobs: Optional[str] = "null"
    finish_reason: str = "stop"

# create a class called "LLMUsage" to describe LLM token usage
class LLMUsage(BaseModel):
    """
    Represents Large Language Model (LLM) token usage
    """
    prompt_tokens: int = 198
    completion_tokens: int = 10
    total_tokens: int = 208

# create a class called "BaseLlamaResponse" to represent each response from the LLM 
class BaseLlamaResponse(BaseModel):
    """
    Represents responses from the Large Language Model (LLM)
    """
    id: str = "cmpl-7fc1be4c-8f5b-4b2f-805f-f8c5086a9fb4"
    object: str = "text_completion"
    created: int = 1708459650
    model: str = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
    choices: List[LLMChoices]
    usage: LLMUsage

# add a HTTP route, with an endpoint called "/healthcheck", to the FastAPI app 
@app.get("/healthcheck")
async def healthcheck() -> str:
    """
    Function to check if the FastAPI app is running
    """
    return "OK"

# add a HTTP route, with an endpoint called "/api", to the FastAPI FastAPI app
@app.get("/api", response_model=BaseLlamaResponse)
async def api(message: LLMRequest = Depends(LLMRequest)) -> Union[CreateCompletionResponse, Iterator[CreateCompletionResponse]]:
    """
    Function to implement the Large Language Model's (LLM) Application Programming Interface (API)
    """
    model_description = "You are an assistant."
    request = f"<|system|>\n{model_description}</s>\n<|user|>{message}</s><|assistant|>"
    response = model(request, temperature=0.0, max_tokens=MAX_TOKENS)
    return response
```

**Step 5.** Run `mypy` using Poetry again to make sure the issues previously identified have been fixed.  
```bash
poetry run mypy -p fastapi_p4 --strict
```

### Subtask 05
The conditions needed to complete Subtask 05 are already done thanks to the way `llmserver.py` is currently written.

### Subtask 06
**Step 1.** Create a directory called `docker` in the parent folder of `fastapi-p4` (notice the `-` in folder's name versus the `_` in the child folder's name).
```bash
mkdir docker/
```

**Step 2.** Create and open a Dockerfile in the `docker` folder. 
```bash
vim docker/Dockerfile
```

**Step 3.** Add the code below to the Dockerfile.
```bash
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
```

**Step 4.** Build a container image using the Dockerfile. 
```bash
docker build -t llmservice:v1.0.0 -f docker/Dockerfile .
```

**Step 5.** Start a container using the container image you just built.
```bash
docker run --name llmservice -d -p80:80 llmservice:v1.0.0
```

**Step 6.** Verify your containerized ML model is still working as intended.
```bash
curl http://localhost/api?message=hi
```

**FYSA.** The submitter assumes you will run it where `fastapi-p4` is a child folder (not via Docker). 

## Task 02
### Subtask 01
**Step 1.** Use Poetry to create a new Python project called `grpc-p4`. FYI, this command will also create a file called `pyproject.toml` among other things.
```bash
poetry new grpc-p4
```

**Step 2.** Change directories to your project folder. 
```bash
cd grpc-p4/
```

**Step 3.** Create and open a file called `poetry.toml`. 
```bash
vim poetry.toml
```

**Step 4.** Add the code below to the `poetry.toml` file. 
```yaml
[virtualenvs]
in-project = true
path = ".venv"
```

**Step 5.** Add the Python packages you need to the `pyproject.toml` file and then install them. 
```bash
poetry add grpcio-tools llama-cpp-python
```

**Step 6.** Create a directory called `v1` under another directory called `llmproto`. 
```bash
mkdir -p llmproto/v1
```

**Step 7.** Create and open a file called `llm.proto` in the `llmproto/v1/` directory.
```bash
vim llmproto/v1/llm.proto
```

**Step 8.** Add the code below to it. 
```go
// set the syntax version
syntax = "proto3";

// define the package
package llmproto.v1;

// import the "Timestamp" type definition file from Google
import "google/protobuf/timestamp.proto";

// define a gRPC service called "LLMService"
service LLMService {
    // returns a CompletionResponse object when given a CompletionRequest object
    rpc Completion (CompletionRequest) returns (CompletionResponse) {}
}

// represents requests sent to the LLM 
message CompletionRequest {
    // message contains the LLM prompt
    string message = 1;
}

// represents responses from the the LLM 
message CompletionResponse {
    // id field
    string id = 1;

    // object field
    string object = 2;

    // timestamp field
    google.protobuf.Timestamp created = 3;

    // model name field
    string model = 4;

    // choices contains a list of fields
    message Choices {
        // text field
        string text = 1;

        // index field
        int32 index = 2;

        // logprobs field
        string logprobs = 3;

        // finish_reason field
        string finish_reason = 4;
    }

    // usage contains a dictionary of fields
    message Usage {
        // prompt_tokens field
        int32 prompt_tokens = 1;

        // completion_tokens field
        int32 completion_tokens = 2;

        // total_tokens field
        int32 total_tokens = 3;
    }

    // choices field
    Choices choices = 5;

    // usage field
    Usage usage = 6;
}
```

**Step 9.** Download and install Homebrew, another open-source package manager. 
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Step 10.** Run the commands necessary to add Homebrew to your `PATH` environment variable. For example, in GitHub Codespaces, I got the following output. 
```bash
==> Next steps:
- Run these two commands in your terminal to add Homebrew to your PATH:
    (echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> /home/codespace/.bashrc
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
``` 

So I ran these commands in my terminal session. Given the filepaths used (ex: `/home/codespace/`) you might have a slightly different command sentence to run. 
```bash
(echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> /home/codespace/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
```

**Step 11.** Download install Buf using Homebrew.
```bash
brew install bufbuild/buf/buf
```

**Step 12.** Create and open a file called `buf.yaml` within the `grpc-p4` folder (this folder is above the `grpc_p4` and `llmproto` folders). The file `buf.yaml` represents Buf's configuration settings. 
```bash
vim buf.yaml
```

**Step 13.** Add the code below to it. 
```yaml
version: v1
build:
  excludes:
    - .venv
lint:
  use:
    - DEFAULT
    - COMMENT_MESSAGE
    - COMMENT_RPC
    - COMMENT_SERVICE
    - COMMENT_FIELD
```

**Step 15.** Run Buf to confirm your `llm.proto` file meets code style and functionality changes. No output is good. It means Buf didn't find anything wrong with your protocol buffer definition.
```bash
./buf lint .
```

### Subtask 02
**Step 1.** Use the `grpc_tools.protoc` Python module to create gRPC stubs. The command sentence below will specifically create a `llmproto/v1` folder and add three files to it: 
* `llm_pb2_grpc.py`: contains client and server classes
* `llm_pb2.py`: contains request and response classes
* `llm_pb2.pyi`: contains protocol buffer message interfaces

```bash
poetry run python -m grpc_tools.protoc -Igrpc_p4=. --python_out=. --pyi_out=. --grpc_python_out=. llmproto/v1/llm.proto
```

**Step 2.** Create and open a file called `server.py` in the `grpc_p4` folder (notice the `_`).
```bash
vim grpc_p4/server.py
```

**Step 3.** Add the code below to it.
```python
"""
A module for an Large Language Model (LLM) gRPC server
"""
# import built-in modules
from concurrent import futures
from time import time

# import third-party modules
from google.protobuf.timestamp_pb2 import Timestamp
import grpc

# import local modules
from grpc_p4.llmproto.v1 import llm_pb2
from grpc_p4.llmproto.v1 import llm_pb2_grpc

port = "50051"

# text goes here
class LLMService(llm_pb2_grpc.LLMServiceServicer):
    """
    Text goes here
    """
    def Completion(self, request, context):
        print(f"LLM Prompt: {request.message}")
        seconds_since_epoch = int(time())
        timestamp = Timestamp()
        timestamp.FromSeconds(seconds=seconds_since_epoch)
        return llm_pb2.CompletionResponse(
            id="cmpl-7fc1be4c-8f5b-4b2f-805f-f8c5086a9fb4",
            object="text_completion",
            created=timestamp,
            model = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
            choices=llm_pb2.CompletionResponse.Choices(
                text="Beep boop",
                index=0,
                logprobs="null",
                finish_reason="stop"
            ),
            usage=llm_pb2.CompletionResponse.Usage(
                prompt_tokens=198,
                completion_tokens=10,
                total_tokens=208
            )
        )

# text goes here
def serve(port: str):
    """
    Text goes here
    """
    # declare and initialize a variable called "server" using 
    # a grpc.server() object
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # declare and initialize a variable called "llmservice" using 
    # a LLMService() object
    llmservice = LLMService()

    # bind the LLMService to the gRPC server
    llm_pb2_grpc.add_LLMServiceServicer_to_server(llmservice, server)

    # add a port to the gRPC server
    server.add_insecure_port("[::]:" + port)

    # start the gRPC server
    server.start()
    print(f"Server started, listening on {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve(port)
```

**Step 4.** Create and open a file called `client.py` in the `grpc_p4` folder (notice the `_`).
```bash
vim grpc_p4/client.py
```

**Step 5.** Add the code below to it.
```python
"""
A module for an Large Language Model (LLM) gRPC client
"""
# import built-n modules
from __future__ import print_function

# import third-party modules
import grpc

# import local modules
from grpc_p4.llmproto.v1 import llm_pb2
from grpc_p4.llmproto.v1 import llm_pb2_grpc

# text goes here
def run():
    """
    Text goes here
    """
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = llm_pb2_grpc.LLMServiceStub(channel)
        response = stub.Completion(llm_pb2.CompletionRequest(message="hello"))
    print(response)


if __name__ == "__main__":
    run()
```

**Step 6.** Start the gRPC server.
```bash
poetry run python -m grpc_p4.server
```

**Step 7.** In another terminal, run the gRPC client to make sure your code works. You should get a response back similar to the output of the LLM in Task 01. 
```bash
poetry run python -m grpc_p4.client
```

### Subtask 03
**Step 1.** Open the file called `llm.proto` (i.e., the protocol buffer definition file) in the `llmproto/v1/` directory.
```bash
vim llmproto/v1/llm.proto
```

**Step 2.** Replace its contents with the code below. 
```go
// set the syntax version
syntax = "proto3";

// define the package
package llmproto.v1;

// import the "Timestamp" type definition file from Google
import "google/protobuf/timestamp.proto";

// define a gRPC service called "LLMService"
service LLMService {
    // returns a CompletionResponse object when given a CompletionRequest object
    rpc Completion (CompletionRequest) returns (CompletionResponse) {}

    // returns a stream LLMStreamResponse object when given a LLMStreamResponse object
    rpc LLMStream (LLMStreamRequest) returns (stream LLMStreamResponse) {}
}

// represents requests sent to the LLM 
message CompletionRequest {
    // message contains the LLM prompt
    string message = 1;
}

// represents responses from the the LLM 
message CompletionResponse {
    // id field
    string id = 1;

    // object field
    string object = 2;

    // timestamp field
    google.protobuf.Timestamp created = 3;

    // model name field
    string model = 4;

    // choices contains a list of fields
    message Choices {
        // text field
        string text = 1;

        // index field
        int32 index = 2;

        // logprobs field
        string logprobs = 3;

        // finish_reason field
        string finish_reason = 4;
    }

    // usage contains a dictionary of fields
    message Usage {
        // prompt_tokens field
        int32 prompt_tokens = 1;

        // completion_tokens field
        int32 completion_tokens = 2;

        // total_tokens field
        int32 total_tokens = 3;
    }

    // choices field
    Choices choices = 5;

    // usage field
    Usage usage = 6;
}

// represents requests sent to the LLM 
message LLMStreamRequest {
    // message contains the LLM prompt
    string message = 1;
}

// represents responses from the the LLM 
message LLMStreamResponse {
    // id field
    string id = 1;

    // object field
    string object = 2;

    // timestamp field
    google.protobuf.Timestamp created = 3;

    // model name field
    string model = 4;

    // choices contains a list of fields
    message Choices {
        // text field
        string text = 1;

        // index field
        int32 index = 2;

        // logprobs field
        string logprobs = 3;

        // finish_reason field
        string finish_reason = 4;
    }

    // choices field
    Choices choices = 5;
}
```

**Step 3.** Run Buf again to make sure `llm.proto` still meets style and functionality expectations.
```bash
buf lint .
```

**Step 4.** Use the `grpc_tools.protoc` Python module again to recreate gRPC stubs. 
```bash
poetry run python -m grpc_tools.protoc -Igrpc_p4=. --python_out=. --pyi_out=. --grpc_python_out=. llmproto/v1/llm.proto
```

**Step 5.** Open the file called `server.py` in the `grpc_p4` folder (notice the `_`).
```bash
vim grpc_p4/server.py
```

**Step 6.** Add the code below to it.
```python
"""
A module for an Large Language Model (LLM) gRPC server
"""
# import built-in modules
from collections.abc import Iterator
from concurrent import futures
from time import time
from typing import Dict

# import third-party modules
from google.protobuf.timestamp_pb2 import Timestamp
import grpc
from llama_cpp import Llama

# import local modules
from grpc_p4.llmproto.v1 import llm_pb2
from grpc_p4.llmproto.v1 import llm_pb2_grpc

# set environment variable
port = "50051"

# declare and initialize a variable called "model" by assigning a Llama object to it
model = Llama(
    model_path="tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
    n_ctx=512,
    n_batch=1
)

# set the max number of tokens allowed for each LLM prompt 
MAX_TOKENS = 512

# text goes here
class LLMService(llm_pb2_grpc.LLMServiceServicer):
    """
    Text goes here
    """
    def Completion(self, request: llm_pb2.CompletionRequest, context: grpc.ServicerContext) -> llm_pb2.CompletionResponse:
        """
        Text goes here
        """
        print(f"Completion Request: {request.message}")
        seconds = int(time())
        timestamp = Timestamp()
        timestamp.FromSeconds(seconds)
        return llm_pb2.CompletionResponse(
            id="cmpl-7fc1be4c-8f5b-4b2f-805f-f8c5086a9fb4",
            object="text_completion",
            created=timestamp,
            model = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
            choices=llm_pb2.CompletionResponse.Choices(
                text="Beep boop",
                index=0,
                logprobs="null",
                finish_reason="stop"
            ),
            usage=llm_pb2.CompletionResponse.Usage(
                prompt_tokens=198,
                completion_tokens=10,
                total_tokens=208
            )
        )
    def LLMStream(self, request: llm_pb2.LLMStreamRequest, context: grpc.ServicerContext) -> Iterator[llm_pb2.LLMStreamResponse]:
        """
        Text goes here
        """
        print(f"LLM Stream Request: {request.message}")
        model_description = "You are an assistant."
        llmprompt = f"<|system|>\n{model_description}</s>\n<|user|>{request.message}</s><|assistant|>"
        for element in model(llmprompt, temperature=0.0, max_tokens=MAX_TOKENS, stream=True):
            assert isinstance(element, Dict)
            assert element["choices"][0]["logprobs"] is None
            seconds = int(element["created"])
            timestamp = Timestamp()
            timestamp.FromSeconds(seconds)
            yield llm_pb2.LLMStreamResponse(
                id=element["id"],
                object=element["object"],
                created=timestamp,
                model = element["model"],
                choices=llm_pb2.LLMStreamResponse.Choices(
                    text=element["choices"][0]["text"],
                    index=element["choices"][0]["index"],
                    logprobs=element["choices"][0]["logprobs"],
                    finish_reason=element["choices"][0]["finish_reason"]
                )
            )

# text goes here
def main(port: str) -> None:
    """
    Text goes here
    """
    # declare and initialize a variable called "server" using 
    # a grpc.server() object
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # declare and initialize a variable called "llmservice" using 
    # a LLMService() object
    llmservice = LLMService()

    # bind the LLMService to the gRPC server
    llm_pb2_grpc.add_LLMServiceServicer_to_server(llmservice, server)

    # add a port to the gRPC server
    server.add_insecure_port("[::]:" + port)

    # start the gRPC server
    server.start()
    print(f"Server started, listening on {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    main(port)
```

**Step 7.** Open the file called `client.py` in the `grpc_p4` folder (notice the `_`).
```bash
vim grpc_p4/client.py
```

**Step 8.** Add the code below to it.
```python
"""
A module for an Large Language Model (LLM) gRPC client
"""
# import third-party modules
import grpc

# import local modules
from grpc_p4.llmproto.v1 import llm_pb2
from grpc_p4.llmproto.v1 import llm_pb2_grpc

# text goes here
def main() -> None:
    """
    Text goes here
    """
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = llm_pb2_grpc.LLMServiceStub(channel)
        for element in stub.LLMStream(llm_pb2.LLMStreamRequest(message="hello")):
            print(element.choices.text, end="", flush=True)

if __name__ == "__main__":
    main()
```

**Step 9.** Download the `tinyllama-1.1b-chat-v1.0.Q2_K.gguf` model file to the `grpc-p4` directory.
```bash
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q2_K.gguf
```

**Step 10.** Start the gRPC server.
```bash
poetry run python -m grpc_p4.server
```

**Step 11.** In another terminal, run the gRPC client to make sure your code works. You should get a streaming response back similar to ChatGPT.
```bash
poetry run python -m grpc_p4.client
```

### Subtask 04
**Step 1.** Add the `grpc-stubs`, `mypy`, and `types-protobuf` Python packages to your project as development dependencies. Again, doing this allows you to use these packages while ensuring they are not added to your production-specific `pyproject.toml` when you publish your project later. 
```bash
poetry add -G dev grpc-stubs mypy types-protobuf 
```

**Step 2.** Open the file called `pyproject.toml`.
```bash
vim pyproject.toml
```
 
**Step 3.** Add the content below to it.
```yaml
[tool.mypy]
strict = true
untyped_calls_exclude = "grpc_p4.llmproto"

[[tool.mypy.overrides]]
module = "grpc_p4.llmproto.v1.*"
ignore_errors = true
```

**Step 4.** Run `mypy` using Poetry to lint `server.py`. `mypy` shouldn't find any issues.
```bash
poetry run mypy grpc_p4/server.py --strict
```

**Step 5.** Run `mypy` using Poetry to lint `client.py`. `mypy` shouldn't find any issues.
```bash
poetry run mypy grpc_p4/client.py --strict
```

**Step 6.** Add the `asyncio` Python package to the `pyproject.toml` file and then install them. 
```bash
poetry add asyncio
```

**Step 7.** Open the file called `server.py` in the `grpc_p4` folder (notice the `_`).
```bash
vim grpc_p4/server.py
```

**Step 8.** Replace its contents with the code below.
```python
"""
A module for an Large Language Model (LLM) gRPC server
"""
# import built-in modules
from time import time
from typing import AsyncGenerator
from typing import Dict
from typing import List

# import third-party modules
from google.protobuf.timestamp_pb2 import Timestamp
from llama_cpp import Llama
import asyncio
import grpc

# import local modules
from grpc_p4.llmproto.v1 import llm_pb2
from grpc_p4.llmproto.v1 import llm_pb2_grpc

# set environment variable
port = "50051"

# declare and initialize a variable called "model" by assigning a Llama object to it
model = Llama(
    model_path="tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
    n_ctx=512,
    n_batch=1
)

# set the max number of tokens allowed for each LLM prompt 
MAX_TOKENS = 512

# text goes here
class LLMService(llm_pb2_grpc.LLMServiceServicer):
    """
    Text goes here
    """
    async def Completion(self, request: llm_pb2.CompletionRequest, context: grpc.ServicerContext) -> llm_pb2.CompletionResponse:
        """
        Text goes here
        """
        print(f"Completion Request: {request.message}")
        seconds = int(time())
        timestamp = Timestamp()
        timestamp.FromSeconds(seconds)
        return llm_pb2.CompletionResponse(
            id="cmpl-7fc1be4c-8f5b-4b2f-805f-f8c5086a9fb4",
            object="text_completion",
            created=timestamp,
            model = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
            choices=[
                llm_pb2.Choice(
                    text="Beep boop",
                    index=0,
                    logprobs="null",
                    finish_reason="stop"
                )
            ],
            usage=llm_pb2.Usage(
                prompt_tokens=198,
                completion_tokens=10,
                total_tokens=208
            )
        )
    async def LLMStream(self, request: llm_pb2.LLMStreamRequest, context: grpc.ServicerContext) -> AsyncGenerator[llm_pb2.LLMStreamResponse, None]:
        """
        Text goes here
        """
        print(f"LLM Stream Request: {request.message}")
        model_description = "You are an assistant."
        llmprompt = f"<|system|>\n{model_description}</s>\n<|user|>{request.message}</s><|assistant|>"
        for element in model(llmprompt, temperature=0.0, max_tokens=MAX_TOKENS, stream=True):
            assert isinstance(element, Dict)
            assert isinstance(element["choices"], List)
            assert element["choices"][0]["logprobs"] is None
            seconds = int(element["created"])
            timestamp = Timestamp()
            timestamp.FromSeconds(seconds)
            yield llm_pb2.LLMStreamResponse(
                id=element["id"],
                object=element["object"],
                created=timestamp,
                model=element["model"],
                choices=element["choices"]
            )

# text goes here
async def main() -> None:
    """
    Text goes here
    """
    # declare and initialize a variable called "server" using 
    # a grpc.server() object
    server = grpc.aio.server()

    # declare and initialize a variable called "llmservice" using 
    # a LLMService() object
    llmservice = LLMService()

    # bind the LLMService to the gRPC server
    llm_pb2_grpc.add_LLMServiceServicer_to_server(llmservice, server)

    # add a port to the gRPC server
    server.add_insecure_port("[::]:" + port)

    # start the gRPC server
    await server.start()
    print(f"Server started, listening on {port}")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(main())
```

**Step 9.** Open the file called `client.py` in the `grpc_p4` folder (notice the `_`).
```bash
vim grpc_p4/server.py
```

**Step 10.** Replace its contents with the code below.
```python
"""
A module for an Large Language Model (LLM) gRPC client
"""
# import third-party modules
import asyncio
import grpc

# import local modules
from grpc_p4.llmproto.v1 import llm_pb2
from grpc_p4.llmproto.v1 import llm_pb2_grpc

# text goes here
async def main() -> None:
    """
    Text goes here
    """
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = llm_pb2_grpc.LLMServiceStub(channel)
        for element in stub.LLMStream(llm_pb2.LLMStreamRequest(message="hello")):
            print(element.choices[0].text, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
```

**Step 11.** Install `grpcurl` using Homebrew. It's needed for the submitter.
```bash
brew install grpcurl
```

## Task 03
**Purpose of Task 03**  
FastAPI does not provide a streaming interface for clients that can scale without violating REST. gRPC, on the other hand can scale, but its interface will not work with frontend applications that can't use gRPC. 

**Step 1.** 

## Task 04