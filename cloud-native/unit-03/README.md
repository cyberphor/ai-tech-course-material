# Cloud Native: API Gateway
* [References](#references)
* [Setup](#setup)
* [Task 01](#task-01)
* [Task 02](#task-02)
* [Task 03](#task-03)
* [Task 04](#task-04)
* [Task 05](#task-05)

## References
If I find any helpful references, I will put them here. 
* [GitHub - cyberphor: virtualization/containers/kubernetes](https://github.com/cyberphor/knowledge-base/tree/main/virtualization/containers/kubernetes)

## Setup
**Step 1.** Accept the GitHub Classroom assignment titled "Project 3 - Productionizing API Gateways." The invitation is in the "Setup" section of task 1's instructions (in the course material, not here). After accepting the assignment, a GitHub repository will be created for you. To access it, do the following: (1) login to GitHub, (2) click your profile picture, (3) click "Your organizations", (4) click "CloudNativeSpring2024", and then (5) click the "project-3-productionizing-api-gateways-" repository. 

**Step 2.** Download the `vic-code` GitHub repository and change directories to the `setup` folder for this week's project. These commands are meant to be ran on your personal computer.
```bash
git clone https://github.com/AFC-AI2C-Cohort-04/vic-code
cd vic-code/cloud-native/unit-03/setup/
```

**Step 3.** Login to the Azure CLI if you haven't already. This command is meant to be ran on your personal computer.
```bash
az login --use-device-code
```

**Step 4.** Set your subscription if you haven't already. This command is meant to be ran on your personal computer.
```bash
az account set --subscription "AI2C Subscription 3"
```

**Step 5.** Define and export an environment variable called `ACR_NAME`. 

*Option 1*  
Enter the command below (after replacing the string `cyberphorwashere`). 
```bash
export ACR_NAME="cyberphorwashere"
```

*Optional 2*  
Edit the provided [`.env`](setup/.env) file and then enter the command below. Again, the `source` program reads and executes commands from files into your current shell environment. 
```bash
source .env
```

**Step 6.** Create an Azure Kubernetes Cluster (AKS) resource using the [provided script](setup/setup.sh). From the `setup` directory, run the command below. 
```bash
bash setup.sh
```

## Task 01
**Step 1.** Text goes here.

## Task 02
**Step 1.** Text goes here.

## Task 03
**Step 1.** Text goes here.

## Task 04
**Step 1.** Text goes here.

## Task 05
**Step 1.** Text goes here.