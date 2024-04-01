# AI Practitioner: Feature Engineering for Logistic Regression
The purpose of this project is to explore (1) featurization schemes and (2) tools for preparing text-based data for numerical computations. Scenario: you're asked to build a dataset that describes the coronavirus and then, analyze it to determine a featurization scheme that will mitigate overfitting.

* [Notes](#notes)
* [References](#references)
* [Setup](#setup)

## Notes
If I learn anything new, I will put it here until I migrate the topic to my public [Knowledge Base](https://github.com/cyberphor/knowledge-base).

**Data Scientists**  
Data scientists are able to build their own dataset on a given topic by performing data collection and data processing tasks. 

## References
If I find any helpful references, I will put them here.

## Setup
FYSA, I used a Windows Subsystem for Linux environment for this project. This WSL environment already had VS Code, the Jupyter VS Code extension, Python 3.10, and Poetry installed. 

**Step 1.** Download the provided dataset and Jupyter Notebook.
```bash
wget https://aipractitioner.blob.core.windows.net/feature-engineering/sail2/v1/domain_data_preparation.tgz
```

**Step 2.** Unzip and extract the the provided dataset and Jupyter Notebook.
```bash
tar -xzvf domain_data_preparation.tgz
```

**Step 3.** Initialize your current working directory as a Poetry project. The purpose of this step is to add a `pyproject.toml` file to your existing and current working directory in preparation of using Poetry for package management and virtual environment management. This step is just one way of organizing your workspace. You are free to use other methods. 
```bash
poetry init --no-interaction
```

**Step 4.** Create and open a file called `poetry.toml` in your current working directory.
```bash
vim poetry.toml
```

**Step 5.** Add the content below to it. The purpose of this step and the previous one is to configure Poetry to create your virtual environment within your current working directory. 
```toml
[virtualenvs]
in-project = true
path = ".venv"
```

**Step 6.** Download the Python packages specified in requirements to your virtual environment. Again, Poetry creates, updates, activates, and deactivates your virtual environment for you.   
```bash
poetry add $(cat requirements.txt)
```

**Step 7.** Open the provided Jupyter Notebook in VS Code. 

**Step 8.** Click "View > Command Palette" and select "Python: Select Interpreter." Then, click "Enter interpreter path... > Find..." and select `.venv/bin/python`. 

**Step 9.** Click "Select kernel > Python Environments > .venv (Python 3.10.12)." FYI, your Python version might be different. Just pick the Python interpreter that's within your `.venv` folder (again this folder was created by Poetry).

**Step 10.** Give yourself permission to execute the provided `submitter` program.
```bash
chmod +x submitter
```