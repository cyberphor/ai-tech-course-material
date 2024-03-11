# Cloud Native: Inter-Service Communication
* [Notes](#notes)
* [References](#references)
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)
* [Task 03](#task-03)
* [Task 04](#task-04)

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

## References
If I find any helpful references, I will put them here. 

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
```bash
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

## Task 03

## Task 04