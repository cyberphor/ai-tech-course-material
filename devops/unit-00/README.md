## DevOps
### Git, GitHub, and Azure DevOps
* [Task 01: Create a GitHub Personal Access Token](#task-01)
* [Task 02: Create an Azure DevOps Personal Access Token](#task-03)
* [Task 03: Create an Azure DevOps Project](#task-03)
* [Task 04: Purchase an Azure DevOps Parallel Job for an Organization](#task-04)
* [Task 05: Configure Git](#task-05)
* [Task 06: Clone a Repo Using SSH](#task-06)
* [Task 07: Create a Branch](#task-07)
* [Task 08: Add a GitHub Action](#task-08)
* [Task 09: Push a Commit](#task-09)

## Task 01
### Create a GitHub Personal Access Token
**Step 1.** Login to GitHub.  
**Step 2.** Click your profile (top-right icon) and click "Settings."  
**Step 3.** Click "Developer Settings" at the bottom of the pane on the left-hand side.  
**Step 4.** Click "Personal access tokens" > "Tokens (classic)."  
**Step 5.** Click "Generate new token" > "Generate new token (classic)."  
**Step 6.** Enter a "Note" (e.g., AI2C-DevOps-Week03).  
**Step 7.** Set the "Expiration" date (e.g., 60 days).  
**Step 8.** Select "repo" as the scope.  
**Step 9.** Click "Generate token."  

## Task 02
### Create an Azure DevOps Personal Access Token
**Step 1.** Browse to [http://dev.azure.com/](http://dev.azure.com/).  
**Step 2.** Click your Azure DevOps project.  
**Step 3.** Click your profile (the person-and-gear icon in the top-right corner).  
**Step 4.** Click "Personal access tokens."  
**Step 5.** Click "New Token."  
**Step 6.** Enter a "Name."  
**Step 7.** Set the "Scopes" field to "Custom defined."  
**Step 8.** Under the "Build" section, select "Read."  
**Step 9.** Click "Create."  
**Step 10.** Record your PAT and use it as necessary.

## Task 03
### Create an Azure DevOps Project
Azure DevOps projects and Azure DevOps pipelines are equivalent to GitHub repos and GitHub actions.  
**Step 1.** Browse to [http://dev.azure.com/](http://dev.azure.com/).  
**Step 2.** Click "New Project."  
**Step 3.** Enter a "Project name" (e.g., "ctfconsole").  
**Step 4.** Set the "Visibility" to "Private."  
**Step 5.** Click "Create."

## Task 04
### Purchase an Azure DevOps Parallel Job for an Organization
**Step 1.** Browse to [http://dev.azure.com/](http://dev.azure.com/).  
**Step 2.** Click "Organization settings" (bottom-left corner).  
**Step 3.** Click "Billing."  
**Step 4.** Click "Set up billing."  
**Step 5.** Select your Azure subscription.  
**Step 6.** Set the number of "Paid parallel jobs" for "MS Hosted CI/CD" pipeplines to 1.  
**Step 7.** Click "Save."

## Task 05
### Configure Git
**Step 1.** Enter your email address.

```bash
git config --global user.email "victor.fernandeziii@gmail.com"
```

**Step 2.** Enter your username.
```bash
git config --global user.name "cyberphor"
```

## Task 06
### Clone a Repo Using SSH
**Step 1.** Clone a repo and change your current working directory to it.
```bash
git clone git@github.com:SAIL-Classroom/getting-started-with-cloud-devops-cyberphor &&\
cd getting-started-with-cloud-devops-cyberphor
```

## Task 07
### Create a Branch
**Step 1.** Create a branch and switch to it.
```bash
# -b: creates the branch; if you don't include it, you will only switch branches
git checkout -b "add-test-cases"
```

**Step 2.** Set main as the upstream branch.
```bash
git push --set-upstream origin add-test-cases
```

## Task 08
### Add a GitHub Action
**Step 1.** Open the GitHub Action configuration file.
```bash
vim .github/workflows/main.yml
```

**Step 2.** Add your desired Action (below is an example of an updated configuration file).
```bash
# Name of Workflow
name: CI
# Controls when the workflow will run
on:
  # Triggers the workflow on push event but only for the "master" branch
  push:
    branches: [ "master" ]
  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:
# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "ci-greetings"
  ci-greetings:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest
    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v3
      # Runs a single command (i.e., Action) using the runners shell
      - name: Greetings
        run: echo "Welcome to the Cloud DevOps course!"
```

## Task 09
### Push a Commit
**Step 1.** Verify you're working on the right branch.  
```bash
git branch
```

**Step 2.** Stage all changes made (i.e., add all changes to the index).
```bash
git add .
```

**Step 3.** Create a commit with a message describing what changed.
```bash
git commit -m "update .github/workflows/main.yml"
```

**Step 4.** Upload the changes and commit made to the branch.
```bash
git push
```