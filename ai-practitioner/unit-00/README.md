# AI Practitioner: Recommendation Systems
* [Notes](#notes)
* [References](#references)
* [Setup](#setup)
* [Task 01](#task-01)

## Notes
If I learn anything new, I will put it here until I migrate the topic to my public [Knowledge Base](https://github.com/cyberphor/knowledge-base).

**Developing a ML System**  
**Step 1.** Identify and explore the data points between the user and their data science problem (e.g., picking a movie to watch). One example is the distribution of movie ratings per user.

**Step 2.** Identify how to assess the performance of your ML system (e.g., how do rating evolve over time?).

**Vectors**  
A *vector* is a list of numbers. The Pandas library represents vectors as Series objects. The NumPy library represents vectors as NumPy Array objects. 

**Outer Product**  
An *outer product* is the result of multiplying two lists of numbers together. The result look like a cross-walk of numbers. For example, imagine you have two lists: `[1,2,3]`, `[4,5]`. The outer product would be: `[[4,5],[8,10],[12,15]]`. 

**Calculating the Outer Product of Two Vectors**  
Below is an example of how calculate the outer product of two vectors in Python.
```python
import pandas as pd
import numpy as np

number_of_users = pd.DataFrame([1,2,3])
number_of_movies = pd.DataFrame([4,5])
outer_product = np.outer(number_of_users, number_of_movies)
print(outer_product)
```

## References
If I find any helpful references, I will put them here.

## Setup
FYSA, I used a Windows Subsystem for Linux environment for this project. This WSL environment already had VS Code, the Jupyter VS Code extension, and Poetry installed. 

**Step 1.** Initialize your current working directory as a Python project using Poetry. The `-n` parameter tells Poetry you don't want to interact with it and to just create a `pyproject.toml` on your behalf.
```bash
poetry init -n
```

**Step 2.** Create and open a file called `poetry.toml`. 
```bash
vim poetry.toml
```

**Step 3.** Add the code below to the `poetry.toml` file. 
```yaml
[virtualenvs]
in-project = true
path = ".venv"
```

**Step 4.** Download the handout. 
```bash
wget https://aipractitioner.blob.core.windows.net/collaborative-filtering/sail2/v1/collaborative_filtering.tgz
```

**Step 5.** Decompress the handout and extract the files it contains. If you didn't know, `z` says "decompress the archive," `x` says "extract the files from the archive," `v` says "be verbose in what you do," and `f` says "the following argument will be the archive to do everything against."
```bash
tar -zxvf collaborative_filtering.tgz
```

**Step 6.** Download the Python modules needed to complete this project. In the command sentence below, I'm using what is called "command substitution" to pass what `cat` will return to `poetry`. Since `requirements.txt` has a list of Python modules, I am passing a list of modules for Poetry to (1) add to the `pyproject.toml` file we just created and (2) download. Be cautious of situations where your `requirements.txt` file has comments. Poetry might throw an error if it's given a string that starts with `#` when it expected the name of a Python module.
```bash
poetry add $(cat requirements.txt)
```

**Step 7.** Open the provided `collaborative_filtering.ipynb` file in VS Code. 

**Step 8.** Click "View > Command Palette" and select "Python: Select Interpreter." Then, click "Enter interpreter path... > Find..." and select `.venv/bin/python`. 

**Step 9.** Click "Select kernel > Python Environments > .venv (Python 3.10.12)." FYI, your Python version might be different. Just pick the Python interpreter that's within your `.venv` folder (again this folder was created in your current working directory by Poetry).

**Step 10.** Give yourself permission to execute the `submitter` file.
```bash
chmod +x submitter
```

## Task 
The purpose of this task is to develop a movie recommendation system that uses collaborative filtering. See [the provided Jupyter Notebook](collaborative_filtering.ipynb) for the walkthrough.