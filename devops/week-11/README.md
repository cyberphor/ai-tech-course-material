# GitHub Actions

## Training Objectives
* Describe a CI/CD workflow
* Describe GitHub Actions
* Describe GitHub Actions benefits
* Describe GitHub Actions features
  * Runner
  * Job
  * Event
  * Workflow
  * Secret
* Implement different CI/CD workflows using GitHub Actions
  * Multi-trigger workflow
  * Conditional workflow
  * Multi-job workflow

## GitHub Actions
GitHub Actions is a platform for defining and executing CI/CD pipelines using YAML and virtual machines in the cloud.

**Runner**  
A GitHub Actions runner is a virtual machine used for executing jobs (i.e., building, testing, releasing, and deploying code). The runner includes the software needed for GitHub to communicate with it. It sits idle when there isn't a workflow to execute and is  rebuilt after every job. The runner's operating system can be customized, but the hardware cannot. If you want to specify the hardware to use, you have to host the runner yourself. 

**Job**  
A GitHub Actions job is a set of instructions executed by a runner. 

**Event**  
A GitHub Actions event is a trigger for job execution. 

**Workflow**  
A GitHub Actions workflow is one or more jobs defined in a YAML and executed by a runner after an event has occurred. The default file-name of a GitHub Actions workflow (`.github/workflows/main.yml`) has nothing to do with worflow execution. 