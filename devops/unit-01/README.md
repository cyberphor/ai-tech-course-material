# Azure DevOps Pipelines: Continuous Integration

## Training Objectives
1. [Create an Azure DevOps Project](#task-1)
2. [Create a Pipeline](#task-2)
3. [Add Triggers to the Pipeline](#task-3)
4. [Add a Build Task to the Pipeline](#task-4)
5. [Add a Copy Task to the Pipeline](#task-5)
6. [Add a Publish Task to the Pipeline](#task-6)
7. [Add a Strategy Matrix to the Pipeline](#task-7)
8. [Review the Pipeline](#task-8)
9. [Create a Commit and Pull Request](#task-9)
10. [Verify the Artifact Was Published](#task-10)

**Purpose**  
Demonstrate knowledge and skill in creating and managing CI/CD pipelines using Azure.

**Conditions**  
You are hired by a startup as a DevOps Engineer. The startup is at the early stage that focuses on activities such as marketing research and product development. The web application is still under working in progress under internal testing. The developers are rapidly making frequent changes to the codebase. In order to ensure the code quality and the correctness of the functionality, the developers write unit tests and manually run the tests every time before they push their code.  

As you may expect, to manually build and test the application worked at the beginning but the increasing cost of this repetitive toil inevitably spins out of control. Such manual work eats up a huge chunk of the developer hours of the team that could otherwise be well spent on the functionality and quality of the product.  

The startup leader is aware of the existence of DevOps which could be the remedy. However, the startup leader does not have the technical experience nor cycles to execute the DevOps transformation.  

You, as the first DevOps Engineer of the startup, will initiate the DevOps adoption of the team. To take the very first step of DevOps transformation, your task is to build a CI pipeline that will build and test the application, and publish deployable artifacts that are ready for further internal testing by the QA team.

**References**  
[Azure Pipelines - Use predefined variables: Build.ArtifactStagingDirectory](https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&tabs=yaml#build-variables)

## Task 1
### Create an Azure DevOps Project
**Step 1.** Browse to [https://dev.azure.com/](https://dev.azure.com/).  
**Step 2.** Click "New Project."  
**Step 3.** Enter a value (e.g., the name of the GitHub repository containing your source code) in the "Project name" field.  
**Step 4.** Set the "Visibility" to "Private."  
**Step 5.** Click "Create."  

## Task 2
### Create a Pipeline      
**Step 1.** Browse to [https://dev.azure.com](https://dev.azure.com).  
**Step 2.** Click the Azure DevOps project you created.    
**Step 3.** Click "Pipelines" in left-hand pane.  
**Step 4.** Click "Create Pipeline."   
**Step 5.** In the "Where is your code?" section, click "GitHub." If prompted, login to GitHub and click "Authorize AzurePipelines."  
**Step 6.** Click the GitHub repository relevant to your project.   
**Step 7.** Click "Starter pipeline."  
**Step 8.** Delete the default "one-line" and "multi-line" steps.  
**Step 9.** Click "Save" (do NOT run the pipeline yet).

## Task 3
### Add Triggers to the Pipeline
**Step 1.** Browse to [https://dev.azure.com](https://dev.azure.com).  
**Step 2.** Click your Azure DevOps project.  
**Step 3.** Click "Pipelines" in the pane on the left.  
**Step 4.** Click "All."  
**Step 5.** Click the ellipsis ("...") next your pipeline and select "Edit."  
**Step 6.** Add your triggers the configuration file.  
**Step 7.** Click "Save" (do NOT run the pipeline yet).

## Task 4
### Add a Build Task the Pipeline
**Step 1.** Browse to [https://dev.azure.com](https://dev.azure.com).  
**Step 2.** Click the Azure DevOps project you created.  
**Step 3.** Click "Pipelines" in the left-hand pane.  
**Step 4.** Click "All."  
**Step 5.** Click the ellipsis ("...") next the pipeline you created and select "Edit."  
**Step 6.** Click "Show assistant" and select the "Maven" task.  
**Step 7.** Enter "verify" in the "Goals(s)" field and click "Add." NOTE: in a real-world scenario, you would set the goal to "package" if you wanted to compile your Java source code.  
**Step 9.** Click "Save" (do NOT run the pipeline yet).

## Task 5
### Add a Copy Task to the Pipeline
**Step 1.** Browse to [https://dev.azure.com](https://dev.azure.com).  
**Step 2.** Click the Azure DevOps project you created.  
**Step 3.** Click "Pipelines" in the left-hand pane.  
**Step 4.** Click "All."  
**Step 5.** Click "Show assistant" and select the "Copy files" task.    
**Step 6.** Enter the directory where your artifact is currently stored (e.g., `target`) as a value in the "Source Folder" field.  
**Step 7.** Enter the file path of your artifact as a value (e.g., `myshuttledev.war`) in the "Contents" field.  
**Step 8.** Enter the artifact staging directory (e.g., `$(Build.ArtifactStagingDirectory)`) in the "Target Folder" field and click "Add."   
**Step 9.** Click "Save" (do NOT run the pipeline yet).

## Task 6
### Add a Publish Task to the Pipeline
**Step 1.** Browse to [https://dev.azure.com](https://dev.azure.com).  
**Step 2.** Click your Azure DevOps project.  
**Step 3.** Click "Pipelines" in the pane on the left.  
**Step 4.** Click "All."  
**Step 5.** Click the ellipsis ("...") next your pipeline and select "Edit."  
**Step 6.** Click "Show assistant" and select "Publish build artifacts."  
**Step 7.** Enter the file path of your artifact staging directory (e.g., `$(Build.ArtifactStagingDirectory)`) in the "Path to publish" field.  
**Step 8.** Enter a value (e.g., `package`) in the "Artifact name" field and click "Add."  
**Step 9.** Click "Save" (do NOT run the pipeline yet).

## Task 7
### Add a Strategy Matrix to the Pipeline
**Step 1.** Browse to [https://dev.azure.com](https://dev.azure.com).  
**Step 2.** Click your Azure DevOps project.  
**Step 3.** Click "Pipelines" in the pane on the left.  
**Step 4.** Click "All."  
**Step 5.** Click the ellipsis ("...") next your pipeline and select "Edit."  
**Step 6.** Add a strategy matrix. The pipeline configuration shown at the end of this document includes an input option called `jdkVersionOption` and uses an environment variable as the value. The environment variable will during each job, facilitating the implementation of the strategy matrix.  
**Step 7.** Click "Save" (do NOT run the pipeline yet).  

## Task 8
### Review the Pipeline
**Step 1.** Browse to [https://dev.azure.com](https://dev.azure.com).  
**Step 2.** Click your Azure DevOps project.  
**Step 3.** Click "Pipelines" in the pane on the left.  
**Step 4.** Click "All."  
**Step 5.** Click the ellipsis ("...") next your pipeline and select "Edit."  
**Step 6.** Review the pipeline (below is an example of a pipeline configuration file). This configuration will produce multiple jobs (i.e., one per item in the strategy matrix).

```yaml
# ----------------------------------------------------------------------------
# TRIGGERS
# ----------------------------------------------------------------------------
# CI trigger: run pipeline when changes are made these branches
trigger:
- "master"
- "add-test-cases"

# PR trigger: run pipeline when PRs are submitted to these branches
pr:
- "master"

pool: # define agent properties
  vmImage: ubuntu-latest # define agent OS

# ----------------------------------------------------------------------------
# STRATEGY MATRIX
# ----------------------------------------------------------------------------
strategy:                 # run the pipeline once per env_var
  matrix:
    jdk10:                # job 1 name
      jdk_version: "1.8"  # env_var: value
    jdk11:                # job 2 name
      jdk_version: "1.11" # env_var: value
  maxParallel: 2

# ----------------------------------------------------------------------------
# TASKS
# ----------------------------------------------------------------------------
steps:

# build the artifact
- task: Maven@4
  inputs:
    mavenPomFile: 'pom.xml'
    goals: 'verify'
    publishJUnitResults: true
    testResultsFiles: '**/surefire-reports/TEST-*.xml'
    javaHomeOption: 'JDKVersion'
    mavenVersionOption: 'Default'
    mavenAuthenticateFeed: false
    effectivePomSkip: false
    sonarQubeRunAnalysis: false
    jdkVersionOption: '$(jdk_version)' # this env_var is defined above

# copy the artifact to the staging directory
- task: CopyFiles@2
  inputs:
    SourceFolder: 'target'
    Contents: 'myshuttledev.war'
    TargetFolder: '$(Build.ArtifactStagingDirectory)'

# publish the artifact
- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'
    ArtifactName: 'package'
    publishLocation: 'Container'
```

## Task 9
### Create a Commit and Pull Request
**Step 1.** Create a branch and switch to it.
```bash
# -b: creates the branch; if you don't include it, you will only switch branches
git checkout -b "add-test-cases"
```

**Step 2.** Define the upstream branch.
```bash
git push --set-upstream origin add-test-cases
```

**Step 3.** Add or modify a file.  
```bash
touch demo.txt
```

**Step 4.** Stage all changes made (i.e., add all changes to the index).
```bash
git add .
```

**Step 5.** Create a commit with a message describing what changed.
```bash
git commit -m "Add a file"
```

**Step 6.** Upload the changes and commit made to the branch.
```bash
git push
```

## Task 10
### Verify the Artifact Was Published
**Step 1.** Browse to [https://dev.azure.com](https://dev.azure.com).  
**Step 2.** Click your Azure DevOps project.  
**Step 3.** Click "Pipelines" in the pane on the left.  
**Step 4.** Click "All."  
**Step 5.** Click the pipeline you previously ran.  
**Step 6.** Click the most recent run.  
**Step 7.** In the "Summary" section, verify the number of artifacts published is at least 1.