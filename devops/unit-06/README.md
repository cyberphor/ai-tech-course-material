## DevOps: Serverless Functions
* [Setup](#setup)
* [Concepts](#concepts)
* [Task 01](#task-1)
* [Task 02](#task-2)
* [Task 03](#task-3)

## Concepts
**Rate-Limiting**  
Rate-limiting is when you define and enforce the number of requests your app will respond to within a time interval. It is used to mitigate Denial-of-Service attacks (i.e., app exhaustion). It can also be used for the reasons listed below. 
* Enforce quotas
* Control the flow of data between endpoints
* Reduce cost

**Base64**  
Base64 is an encoding scheme for representing binary data in ASCII. It was developed to help transmit binary data between endpoints that can only handle text-based data. It is associated with encryption or compression. 

**Azure Function Archectype: Maven**  
The Maven Azure Function archectype includes the software needed to develop, build, and deploy a Java-based serverless function. NOTE: every Azure Function app must have a globally unique name (i.e., the "functionAppName" field within the app's "pom.xml" file). 

**Cold Start**  
A cold start is when your serverless function takes longer than usual because it has not been executed for an extended amount of time. It takes longer because the hardware allocated for it has to be powered back on. At some point, it was turned off due to inactivity. 

**Deployment Strategies**  
* Canary: deploying your app for a small set of people before everyone else
* Rolling: individually replacing old instances of your app with the new version
* Blue/Green: load balancing traffic to the old (Blue, production) and new (Green, staging) version of your app 

**GitFlow**  
GitFlow is a Git branching strategy. Below describes how you would implement it. 
* Create and maintain two branches
  * main
    * All commits are tagged with a version number (e.g., v0.1.0)
    * This branch stores all the official release history of the app
  * develop
    * This branch serves as the parent branch of all features 
    * Feature branches never interact with the main branch

![gitflow.png](gitflow.png)

**Deployment Slots**  
Deployment slots are instances of your Azure Function with a unique hostname. App content and configurations elements can be swapped between two deployment slots, including the production slot.

**Serverless Functions**  
![serverless-function.png](serverless-function.png)


## Setup
**Step 1.** Create a private GitHub repository called `cicd-functions`. 

**Step 2.** Clone it within Azure Cloud Shell. 
```bash
git clone git@github.com:cyberphor/cicd-functions.git
```

## Task 01
**Step 1.** From your home directory, generate an Maven project using the command below. 
```bash
mvn archetype:generate \
    -DarchetypeGroupId=com.microsoft.azure \
    -DarchetypeArtifactId=azure-functions-archetype
```

Use the values below when you are prompted for input. 
| Variable   | Value               |
| ---------- | ------------------- |
| groupId    | `edu.cmu.cs.devops` |
| artifactId | `my-first-function` |
| version    | Default             |
| package    | Default             |

**Step 2.** Copy everything from your "my-first-function" folder (it's automatically created in the previous step) to your GitHub repository. 
```bash
cp -r my-first-function/* cicd-functions/
```

**Step 3.** Change your current working directory to your GitHub repository. 
```bash
cd cicd-functions/
```

**Step 4.** In the "pom.xml" file, set the "region" field to `eastus`. Then, add the code below under the "<dependencies>" section.
```xml
<dependency>
    <groupId>commons-codec</groupId>
    <artifactId>commons-codec</artifactId>
    <version>1.14</version>
</dependency>
```

**Step 5.** Replace the code in the "host.json" file with the code below to implement rate limiting. 
```json
{
  "version": "2.0",
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[3.*, 4.0.0)"
  },
  "extensions": {
    "http": {
      "routePrefix": "api",
      "maxOutstandingRequests": 200
    }
  }
}
```

**Step 6.** Replace the "Function.java" file with [the one provided](/devops/week-13/task-1-Function.java).
```bash
cp task-1-Function.java ~/cicd-functions/src/main/java/edu/cmu/cs/devops/Function.java
```

**Step 7.** Copy [the provided test file](/devops/week-13/task-1-FunctionTest.java) to the correct folder within your Maven project. 
```bash
cp task-1-FunctionTest.java ~/cicd-functions/src/test/java/edu/cmu/cs/devops/FunctionTest.java
```

**Step 8.** Package your Maven project.  
```bash
mvn clean package
```

**Step 8.** Deploy the serverless function. Part of the Azure Functions template are the instructions to create a resource group in Azure. Take note of the serverless function URL in the resulting output. 
```bash
mvn azure-functions:deploy
```

**Step 9.** Verify the serverless function is working. 
```bash
export SERVERLESS_FUNCTION_URL="https://my-first-function-20231201120945143.azurewebsites.net/api/HttpExample"
export REQUEST=$(echo -n "Sort these words for me" | base64)
curl "${SERVERLESS_FUNCTION_URL}" --data "${REQUEST}" -s | base64 -d
# for me Sort these words
```

**Step 10.** Commit the changes you've made so far to your GitHub repository. 
```bash
git add .
git commit -m "Added a serverless function"
git push
```

## Task 02
**Step 1.** Login to Azure and download the "Publish Profile" for your Azure Function (click the "Get publish profile" button on the "Overview" page). 

**Step 2.** Create a service account for GitHub Actions to use when accessing Azure. Copy the output to your clipboard. 
```bash
export SUBSCRIPTION_ID="17408d59-f3b6-43a5-a48c-c3667527f330"
export RESOURCE_GROUP="java-functions-group"
export FUNCTION_APP_NAME="my-first-function-20231201120945143"
export SCOPES="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.Web/sites/${FUNCTION_APP_NAME}"
az ad sp create-for-rbac \
  --name "${FUNCTION_APP_NAME}" \
  --role contributor \
  --scopes "${SCOPES}" \
  --sdk-auth
```

Below is an example of the output to expect.
```json
{
  "clientId": "be0fedc0-ecc7-47ce-ad8a-309658c3bb8f",
  "clientSecret": "nI38Q~6ApA0suh_ace.lcAh3ra2HrxD0ts6siavK",
  "subscriptionId": "17408d59-f3b6-43a5-a48c-c3667527f330",
  "tenantId": "da3cb2a3-95dd-4a37-b857-c1264e363deb",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

**Step 3.** Add the output from the previous step as a secret to your GitHub repository. Call it `AZURE_CREDENTIALS`.

**Step 4.** Add a Github Actions workflow configuration file to your repository using inspiration from [the provided example](/devops/week-13/task-2-function-deploy.yml).

## Task 03
In this task, you're going to do the following:
* Create a *staging* environment in Azure for your serverless function
* Update the CI/CD pipeline for your *production* environment
* Add a secondary CI/CD pipeline albeit for your *staging* environment
* Update the code in your serverless function
* Create a "develop" branch

**Step 1.** Using the Azure Portal, add a "Deployment Slot" to your Azure Function. Call it "staging."

**Step 2.** Download the "Publish Profile" for the "staging" deployment slot.

**Step 3.** Add another secret to your GitHub repository. Call it `AZURE_FUNCTIONAPP_STAGING_PUBLISH_PROFILE` and use the contents of the "staging" publish profile as its value.

**Step 4.** Update your GitHub Actions workflow configuration file using inspiration from [the updated version of the first example](/devops/week-13/task-3-function-deploy.yml). 

**Step 5.** Create an second GitHub Actions workflow configuration file using inspiration from [the second provided example](/devops/week-13/task-3-function-swap.yml).

**Step 6.** Sync your local repository and GitHub repository.
```bash
git pull origin main
```

**Step 7.** Update the "Function.java" file with [a newer version](/devops/week-13/task-3-Function.java).
```bash
cp task-3-Function.java ~/cicd-functions/src/main/java/edu/cmu/cs/devops/Function.java
```

**Step 8.** Update the "FunctionTest.java" file with [a newer version](/devops/week-13/task-3-FunctionTest.java). 
```bash
cp task-3-FunctionTest.java ~/cicd-functions/src/test/java/edu/cmu/cs/devops/FunctionTest.java
```

**Step 9.** Create and checkout a "develop" branch. 
```bash
git checkout -b develop
```

**Step 10.** Push the "develop" branch to your GitHub repository.
```bash
git push origin develop
```
**Step 11.** Create and checkout a "feature/blue-green-gitflow" branch.
```bash
git checkout -b feature/blue-green-gitflow
```

**Step 12.** Add all the changes you've made so far to the "feature/blue-green-gitflow" branch. The command below adds all modified and untracked files in your entire repository. `git add .` only adds modified/untracked files in your current working directory and subdirectories. 
```bash
git add -A 
```

**Step 13.** Commit all the changes you've made so far to your local branch. 
```bash
git commit -m "Added a new feature"
```

**Step 14.** Push all changes committed to the local branch to your GitHub repository. 
```bash
git push origin feature/blue-green-gitflow
```

**Step 15.** Login to GitHub. Create a pull request and merge the "feature/blue-green-gitflow" branch into the "develop" branch. This will trigger the updated "Build and Deploy Job" pipeline and deploy your serverless function to your *staging* environment. 
* Click "Pull requests"
* Click "New pull request"
* Set the "base" to "develop" and "compare" to "feature/blue-green-gitflow"
* Click "Create pull request"
* Click "Merge pull request"
* Click "Confirm merge"

**Step 16.** Test your serverless function in the "staging" environment. 
```bash
export SERVERLESS_FUNCTION_URL="https://my-first-function-20231201120945143-staging.azurewebsites.net/api/HttpExample"
export REQUEST=$(echo -n "Sort these words for me" | base64)
curl "${SERVERLESS_FUNCTION_URL}" --data "${REQUEST}" -s | base64 -d
# words these Sort me for
```

**Step 17.** Login to GitHub. Create a pull request and merge the "develop" branch into the "main" branch. This will trigger the "Swap Job" pipeline and swap your updated serverless function to the "production" environment (specifically, the original version of your serverless function will no longer be considered "production" because the updated version will).
* Click "Pull requests"
* Click "New pull request"
* Set the "base" to "main" and "compare" to "develop"
* Click "Create pull request"
* Click "Merge pull request"
* Click "Confirm merge"