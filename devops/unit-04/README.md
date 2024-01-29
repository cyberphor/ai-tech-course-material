# GitHub Actions

## Training Objectives
* Describe a CI/CD workflow
* Describe GitHub Actions
  * Benefits
  * Features
    * Runners
    * Jobs
    * Events
    * Workflows
    * Secrets
* Implement different CI/CD workflows using GitHub Actions
  * CI workflow
  * CD workflow 
  * CD workflow with a matrix strategy
  * CD workflow with conditional statements (e.g., if a new tag has been pushed)

## GitHub Releases
A GitHub release is software you have packaged and made available for download within your GitHub repository. GitHub releases are based on tags. 

### Tags
Tags are used to identify important moments in the history of your source code. For example, the tag `v1.0.0` may indicate all commits up until this point represent version one of an app. 

**Lightweight Tags**  
A lightweight tag points to a commit. 

**Annotated Tags**  
An annotated tag points to a commit and includes the following: 
* Tagger name
* Tagger email
* Tag date
* Tag message 
* Support for digital signatures that can be verified using GNU Privacy Guard (GPG")

## GitHub Actions
GitHub Actions is a platform for defining and executing CI/CD pipelines using YAML and virtual machines in the cloud.

**Runner**  
A GitHub Actions runner is a virtual machine used for executing jobs (i.e., building, testing, releasing, and deploying code). The runner includes the software needed for GitHub to communicate with it. It sits idle when there isn't a workflow to execute and is  rebuilt after every job. The runner's operating system can be customized, but the hardware cannot. If you want to specify the hardware to use, you have to host the runner yourself. 

**Job**  
A GitHub Actions job is a set of instructions executed by a runner. 

*Matrix Strategy*    
A matrix strategy allows you to loop through different combinations of job variables (e.g., runner operating systems, Java versions, etc.). Below is an example of how you would define one. 

```yaml
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        version: [10, 12, 14]
```

In practice, you would use the variables you define within the matrix strategy elsewhere in your workflow like this:
* OS: `${{ matrix.os }}`
* Version: `${{ matrix.version }}`

**Event**  
A GitHub Actions event is a trigger for job execution. For example, a new tag being added to a repository is an event. 

**Workflow**  
A GitHub Actions workflow is one or more jobs defined in a YAML and executed by a runner after an event has occurred. The default file-name of a GitHub Actions workflow (`.github/workflows/main.yml`) has nothing to do with worflow execution. 

*Webhook*  
A webhook is an alert. They can be used as events (i.e., triggers) in your GitHub Actions workflows. 

*Webhook Payloads*  
A webhook payload contains fields and values relating to the webhook. For example, the payload in a `push` webhook contains the field `ref`. The value stored in the `ref` field can be used to implement conditions for executing different workflows. 
* If the commit pushed to a repository called `main`, the value in the `ref` field would be: `refs/heads/main`
* If the commit pushed a new tag called `v1.0.0`, the value in the `ref` field would be: `refs/tags/v1.0.0`

*How to Reference a Webhook Payload Within a GitHub Actions Workflow*  
A webhook payload can be referenced using the following syntax: `${{ github.event.ref }}`.

*Workflow Functions*  
Below is a list of functions that can be used within an GitHub Actions workflow `if` statement.   
* `startsWith`
* `endsWith`
* `format`
* `toJson`

## Solutions
* [Setup](/devops/week-11/HOWTO.md#setup)
  * [Setup an SSH Key](/devops/week-11/HOWTO.md#setup-an-ssh-key)
  * [Clone a GitHub Repo Using SSH](/devops/week-11/HOWTO.md#clone-a-github-repo-using-ssh)
  * [Create a GitHub Personal Access Token for the Submitter Program](/devops/week-11/HOWTO.md#create-a-github-personal-access-token-for-the-submitter-program)
* [Task 1: Create a CI Pipeline Using a GitHub Actions Workflow](/devops/week-11/HOWTO.md#create-a-ci-pipeline-using-a-github-actions-workflow)
* [Task 2: Create a CD Pipeline Using a GitHub Actions Workflow](/devops/week-11/HOWTO.md#create-a-cd-pipeline-using-a-github-actions-workflow)
* [Task 3: Create a CD Pipeline Using a GitHub Actions Workflow With a Matrix Strategy](/devops/week-11/HOWTO.md#create-a-cd-pipeline-using-a-github-actions-workflow-with-a-matrix-strategy)
* [Task 4: Create a CD Pipeline Using a Github Actions Workflow With Conditional Statements](/devops/week-11/HOWTO.md#create-a-cd-pipeline-using-a-github-actions-workflow-with-conditional-statements)