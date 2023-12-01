# Serverless Functions

## Setup
**Step 1.** Create a private GitHub repository called `cicd-functions`. 

**Step 2.** Clone it within Azure Cloud Shell. 
```bash
git clone git@github.com:cyberphor/cicd-functions.git
```

## Task 1
**Step 1.** From your home directory, generate an Azure Function (i.e., serverless function) template using the command below. 
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

**Step 4.** In the "pom.xml" file set the "region" to be `eastus`. 

**Step 5.** Package the Maven code. 
```bash
mvn clean package
```

**Step 6.** Deploy the serverless function using the Azure Functions plugin (it's installed by default in the Azure Cloud Shell environment). 
```bash
mvn azure-functions:run 
```

**Step 7.** Verify the serverless function is running locally. 
```bash
curl http://localhost:7071/api/HttpExample --data "Victor" -w "\n" 
```

**Step 8.** Stop the serverless function.

**Step 9.** Commit the changes you've made so far to your GitHub repository. 
```bash
git add .
git commit -m "Added a serverless function"
git push
```

## Task 2

## Task 3