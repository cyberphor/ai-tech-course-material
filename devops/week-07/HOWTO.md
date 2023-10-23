# Azure DevOps Pipelines: Continuous Deployment

## Training Objectives
1. Create an Azure DevOps Project for an Existing GitHub Repo
2. Create and Run a CI Pipeline for the Azure DevOps Project (ensure it deploys artifacts between multiple stages)
3. Add a Unit Test and Commit the Changes
4. Add a Publish Task to the CI Pipeline

## Create an Azure DevOps Project for an Existing GitHub Repo
**Step 1.** Create a Personal Access Token (PAT) in GitHub if you don't already have one.

**Step 2.** Purchase and/or add a subscription to your Azure DevOps organization's billing information if you haven't already.

**Step 3.** Add one "MS Hosted CI/CD" parallel job to your Azure DevOps organization's billing information if you haven't already.

**Step 4.** Change your Azure DevOps organization's security policies to "Allow public projects."

**Step 5.** Create a Azure DevOps project and make it public.

**Step 6.** Click "Pipelines."

**Step 7.** Click "Create Pipeline."

## Create and Run a CI Pipeline for the Azure DevOps Project
**Step 1.** Add a CI (aka "build") pipeline to the Azure DevOps project. Below is a template.
```yaml
trigger:
  - master # trigger the pipeline whenever you push an update to the master branch.

stages: # To organize your pipeline into multiple stages, you use the "stages" keyword.
  - stage: Build # name of the stage.
    # Your pipeline may have multiple jobs.
    # In the simplest case, a pipeline has a single job. In that case, you do not have to explicitly use the job keyword.
    # However, you can use the job keyword to specify additional properties on that job.
    jobs:
    - job: Build # name of the job.
      # When your build or deployment runs, the system begins one or more jobs.
      # An agent is an installable software that runs one job at a time.
      # The pool keyword specifies which pool to use for a job of the pipeline.
      # There can be different type of pools.
      # You can specify it at the pipeline, stage, or job level. However, the pool specified at the lowest level of the hierarchy will be used to run the job.
      pool:
        vmImage: 'ubuntu-latest'
      continueOnError: false # The job will not continue on error.
      steps: # Steps consist of tasks that execute in a linear sequence.
        - task: Maven@3 # the name of the task
          inputs: # the inputs of the task
            mavenOptions: '-Xmx3072m' # default maven option
            jdkVersionOption: '1.8' # Java JDK version
            jdkArchitectureOption: 'x64' # Java architecture option. This parameter is optional.
            goals: 'package -Dbuild.version=$(Build.BuildNumber)' # similar to run "mvn package" locally
            mavenPomFile: 'pom.xml' # location of POM file
            publishJUnitResults: true # publish results of JUnit
            testResultsFiles: '**/surefire-reports/TEST-*.xml' # which test files needs to consider for code coverage
            javaHomeOption: 'JDKVersion' # java home path
            mavenVersionOption: 'Default' # maven version
            sonarQubeRunAnalysis: false
        - task: PublishCodeCoverageResults@1 # This task publishes the code coverage so that you can view the result on Azure DevOps GUI
          inputs:
            codeCoverageTool: "JaCoCo" # the tool used for calculating coverage
            summaryFileLocation: "$(System.DefaultWorkingDirectory)/target/site/jacoco/jacoco.xml" # location of the summary file
            reportDirectory: "$(System.DefaultWorkingDirectory)/target/site/jacoco" # location of the report
            failIfCoverageEmpty: true
```

**Step 2.** Run the provided CI pipeline using Azure DevOps (it'll fail given the current state of the source code).

## Add a Unit Test
**Step 1.** Generate and add your SSH public key to your GitHub profile.

**Step 2.** Clone the existing GitHub repo using SSH.
```
git clone git@github.com:SAIL-Classroom/continuous-deployment-cyberphor.git &&\
cd continuous-deployment-cyberphor
```

**Step 2.** Add a unit tests.
```
vim src/test/java/edu/cmu/cc/project2/service/CalculatorServiceTest.java
```
```java
package edu.cmu.cc.project2.service;

import edu.cmu.cc.project2.config.MvcConfig;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ContextConfiguration;

/**
 * Test class for Calculator Service
 */
@SpringBootTest
@ContextConfiguration(classes = MvcConfig.class)
public class CalculatorServiceTest {
    // NEW UNIT TEST
    @Test
    public void fibonacciTest() {
      long num = 4;
      double result = calculatorService.fibonacci(num);
      // Assert that expected and actual are equal within the given non-negative delta.
      Assertions.assertEquals(3.0, result, 0.0);
    }
}
```

**Step 3.** Commit the changes.
```
git add .
git commit -m "Added a unit test for the fibonacci function"
git push
```

## Add a Publish Task to the CI Pipeline
**Step 1.** Add a "publish" task to the CI pipeline. Below is an example.
```
        - task: PublishPipelineArtifact@1
          inputs:
            artifactName: buildCode
            targetPath: "$(Build.SourcesDirectory)"
```

**Step 2.** Verify the CI pipeline ran again.

## Add an Intergration Test
**Step 1.** Add an integration test.
```
vim src/test/java/edu/cmu/cc/project2/controller/MainControllerTest.java
```
```java
# src/main/java/edu/cmu/cc/project2/controller/MainController.java
package edu.cmu.cc.project2.controller;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultHandlers;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

/**
 * Test class for MainController Class
 */
@RunWith(SpringRunner.class)
@WebMvcTest(MainController.class)
public class MainControllerTest {

    @Autowired
    private MockMvc mockMvc; // We will utilize Spring’s MockMvc to test the controller.

  // INTEGRATION TEST EXAMPLE
  public void testCreateRetrieveWithMockMVCFibonacci() throws Exception {
      this.mockMvc.perform(MockMvcRequestBuilders.get("/calculate?operation=5&firstNumber=3"))
      .andDo(MockMvcResultHandlers.print()).andExpect(MockMvcResultMatchers.status().isOk())
      .andExpect(MockMvcResultMatchers.view().name("index"))
      .andExpect(MockMvcResultMatchers.model().attribute("result", 2.0));
  }
}
```

**Step 2.** Commit the changes.
```
git add .
git commit -m "Added integration test for createRetrieve and fibonacciTest functions"
git push
```

## Add a Deployment Job to the CI Pipeline
**Step 1.** Add deployment job to the CI pipeline. Below is an example.
```yaml
  # Description: This is a new Stage that you will add to the pipeline
  # TODO: replace <string> with the new staging name, i.e., Testing
  - stage: Testing
    # Description: what stage(s) this stage dependsOn
    # TODO: this stage depends on the Build stage
    dependsOn: Build
    # Description: list of jobs, no edits needed
    jobs:
    # Description: instead of the `job` keyword that represents a traditional job
    # we use the `deployment` keyword to define a deployment job
    # TODO: replace <deployment_name> with the name of deployment, i.e., testing
    - deployment: testing
    # Description: the pool for this stage
      pool:
        # Description: the VM image we are using to run this deployment
        # TODO: replace <vm_image> with the image you are using for this stage
        # you will use the latest Ubuntu OS, i.e., ubuntu-latest
        vmImage: ubuntu-latest
      # Description: The name of environment for which this stage will run.
      # TODO: replace <environment_name> with the name of environment, i.e., Development
      environment: Development
      # Description: Strategy for deployment
      strategy:
        # Description: name of strategy for deployment
        # TODO: replace <strategy_name> with the name of strategy we are using, i.e., runOnce
        runOnce:
          # Description: used to run steps that deploy app/code. Download artifact task will be auto injected only in the deploy hook for deployment jobs. To stop downloading artifacts, use - download: none or choose specific artifacts to download by specifying Download Pipeline Artifact task.
          deploy:
            # Description: The list of steps need to completed
            steps:
              - task: Maven@3
                inputs:
                  # TODO: replace <pom_location_path> with the location of pom.xml file of the artifact downloaded.
                  mavenPomFile: "$(Pipeline.Workspace)/buildCode/pom.xml"
                  mavenOptions: '-Xmx3072m'
                  javaHomeOption: 'JDKVersion'
                  jdkVersionOption: '1.8'
                  jdkArchitectureOption: 'x64'
                  # TODO: set it to true so that it will generate summary files for code coverage task
                  publishJUnitResults: true
                  # TODO: replace <test_result_files_location> with the location of the XML test files generated
                  testResultsFiles: "$(Pipeline.Workspace)/buildCode/target/failsafe-reports/TEST-*.xml"
                  # TODO: set the goals to verify to run unit and integration tests.
                  goals: verify
              - task: PublishCodeCoverageResults@1
                inputs:
                  # TODO: replace <tool_name> with the name of tool you are using for code coverage
                  codeCoverageTool: JaCoCo
                  # TODO: replace <summary_file_location> with the location of the summary file i.e. the location of `jacoco.xml`
                  summaryFileLocation: "$(Pipeline.Workspace)/buildCode/target/site/jacoco/jacoco.xml"
                  # TODO: replace <report_directory> with the location of the report directory i.e. the folder contains `jacoco.xml`
                  reportDirectory: "$(Pipeline.Workspace)/buildCode/target/site/jacoco"
                  # TODO: Set it to true in order to fail the task if code coverage did not produce any results to publish.
                  failIfCoverageEmpty: true
              - task: PublishPipelineArtifact@1
                inputs:
                  # TODO: replace <artifact_name> with the name for the artifact
                  artifactName: qaCode
                  # TODO: replace <target_location> with the location of file/folder i.e., the location of the source directory
                  targetPath: "$(Pipeline.Workspace)/buildCode"
```

**Step 2.** Commit the changes.
```
git add .
git commit -m "Added a deployment job to the CI pipeline"
git push
```

## Create a SonarCloud Security Token
**Step 1.** Login to [SonarCloud](https://sonarcloud.io/sessions/new).

**Step 1.** Navigate to your account settings and generate a security token. Give the token a name relating to your Azure DevOps project.

## Configure SonarCloud in Azure DevOps
**Step 1.** Add the [SonarCloud extension](https://marketplace.visualstudio.com/) to your Azure DevOps organization.

**Step 2.** Add a service connection for SonarCloud in your Azure DevOps project.

## Create an Azure Personal Access Token
**Step 1.** Browse to [http://dev.azure.com/](http://dev.azure.com/).  
**Step 2.** Click your Azure DevOps project.  
**Step 3.** Click your profile (the person-and-gear icon in the top-right corner).  
**Step 4.** Click "Personal access tokens."  
**Step 5.** Click "New Token."  
**Step 6.** Enter a "Name" (e.g., "SonarCloud").
**Step 7.** Set the "Scopes" field to "Custom defined."  
**Step 8.** Under the "Build" section, select "Code: Read & Write."  
**Step 9.** Click "Create."  
**Step 10.** Record your PAT.

## Create an Organization in SonarCloud
**Step 1.** Login to [SonarCloud](https://sonarcloud.io/sessions/new).

**Step 2.** Navigate to your account settings and create an organization. Use PAT created in the previous task and set the SonarCloud organization to be the same as your Azure DevOps organization's name.

**Step 3.** Choose "Free plan."

**Step 4.** Click "Create Organization."

**Step 4.** Click "My Projects."

**Step 5.** Click "Analyze a new project."

**Step 6.** Select your current Azure DevOps project when prompted and click "Setup."

**Step 7.** Click "Previous version" to specify new code is whatever changed since the previous version.

**Step 8.** Click "Create project."

## Add an Audit Stage to the CI Pipeline
**Step 1.** Add an audit stage to the CI pipeline. Below is an example.
```yaml
	  - stage: Code_Auditing   
      dependsOn: Testing
      jobs:
      - deployment: auditing
        pool:
          vmImage: ubuntu-latest
        environment: Development
        strategy:
          runOnce:
            deploy:
              steps:
                - task: SonarCloudPrepare@1
                  inputs:
                    SonarCloud: "SonarCloud" # service connection name
                    organization: "victorfernandeziii" # name of sonarcloud org
                    scannermode: 'Other'
                - task: Maven@3
                  inputs:
                    mavenPomFile: "$(Pipeline.Workspace)/qaCode/pom.xml"
                    mavenOptions: '-Xmx3072m'
                    javaHomeOption: 'JDKVersion'
                    jdkVersionOption: '1.11'
                    jdkArchitectureOption: 'x64'
                    sonarQubeRunAnalysis: true
                    sqMavenPluginVersionChoice: 'pom'
                    goals: package
                - task: CopyFiles@2
                  inputs:
                    SourceFolder: "$(Pipeline.Workspace)/qaCode/target"
                    Contents: "**/*.war"
                    TargetFolder: "$(Build.ArtifactStagingDirectory)"
                    cleanTargetFolder: true
                - task: PublishPipelineArtifact@1
                  inputs:
                    artifactName: war
                    targetPath: "$(Build.ArtifactStagingDirectory)/project2-cyberphor-0.0.1-SNAPSHOT.war"
```

**Step 2.** Commit the changes.
```
git add .
git commit -m "Added a deployment job to the CI pipeline"
git push
```

## Create an Azure Web App Using the Azure App Service
**Step 1.** Browse to the [Azure App Service](https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.Web%2Fsites).

**Step 2.** Click "Create" and select "Web App."

**Step 3.** Specify the following settings before clicking "Review + create."
* Subscription
* Resource Group: "cdpipeline_app"
* Name: "cyberphorweek07webapp"
* Publish: "code"
* Runtime stack: "Java 8"
  * Java web server stack: "Apache Tomcat 9.0"
* Operating System: "Windows"
* Region: "East US"
* App Service Plan: "Free F1"

## Add a Azure Resource Manager Service Connection Endpoint to the Azure DevOps Project
**Step 1.** Click "Settings."  

**Step 2.** Click "Service connections."  

**Step 3.** Click "New service connections."  

**Step 4**. Select "Azure Resource Manager" and click "Next."  

**Step 5.** Select "Service principal (automatic)" and click "Next."

**Step 6** Login when prompted.  

**Step 7.** Specify the following settings before clicking "Save."  
* Scope level: "Subscription"
* Subscription:
* Service connection name: "Azure Resource Manager"

## Add a Deployment Stage to the CI Pipeline

```yaml
  - stage: Deployment
		dependsOn: Code-auditing
		jobs:
		- deployment: production
		  pool:
			vmImage: ubuntu-latest
		  environment: <environment_name>
		  strategy:
			  runOnce:
			    deploy:
				  steps:
				    - task: AzureWebApp@1
              inputs:
                azureSubscription: "Azure Resource Manager"
                appName: "cyberphorweek07webapp"
                package:  "$(Pipeline.Workspace)/war/project2-cyberphor-0.0.1-SNAPSHOT.war"
                customDeployFolder: ROOT
                # If the field is empty, package is deployed to <appname>.azurewebsites.net/<packagename>
                # If ROOT is used, package is deployed to <appname>.azurewebsited.net.
                appType: webApp
```

**Step 2.** Commit the changes.
```
git add .
git commit -m "Added a deployment stage to the pipeline"
git push
```