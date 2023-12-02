# Serverless Functions

## Setup
**Step 1.** Create a private GitHub repository called `cicd-functions`. 

**Step 2.** Clone it within Azure Cloud Shell. 
```bash
git clone git@github.com:cyberphor/cicd-functions.git
```

## Task 1
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

**Step 6.** Replace the "Function.java" file with [the one provided](/devops/week-13/Function.java).
```bash
cp Function.java ~/cicd-functions/src/main/java/edu/cmu/cs/devops/Function.java
```

**Step 7.** Copy [the provided test file](/devops/week-13/FunctionTest.java) to the correct folder within your Maven project. 
```bash
cp FunctionTest.java ~/cicd-functions/src/test/java/edu/cmu/cs/devops/FunctionTest.java
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
```

**Step 10.** Commit the changes you've made so far to your GitHub repository. 
```bash
git add .
git commit -m "Added a serverless function"
git push
```

## Task 2

## Task 3