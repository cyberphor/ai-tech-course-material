# GitHub Actions

## Setup
### Setup an SSH Key  
**Step 1.** Create an SSH key pair. 
```bash
# -t: key type
# -b: key bit-length
# -C: comment
ssh-keygen -t rsa -b 4096 -C "for DevOps"
```

**Step 2.** Press "Enter" to save your private key to the default location (i.e., under `.ssh/id_rsa` within your home directory).  
  
**Step 3.** Enter a passphrase to encrypt the private key.  

**Step 4.** Open your BASH configuration file using your favorite text-editor
```bash
vim .bashrc
```

**Step 5.** Append the commands below to your BASH configuration file (they will be executed every time you login). 
```bash
eval "$(ssh-agent -s)" # start the SSH authentication agent
ssh-add ~/.ssh/id_rsa  # add my SSH private key to the SSH authentication agent
```

**Step 6.** Reload your environment (this will run the commands added to your BASH configuration file). 
```bash
source .bashrc
```

**Step 7.** Print your SSH public key to the console and copy it into memory.
```bash
cat ~/.ssh/id_rsa.pub
```

**Step 8.** Open a browser and login to GitHub.  

**Step 9.** Click your profile (top-right icon) and click "Settings."  

**Step 10.** Click "SSH and GPG keys" in the pane on the left-hand side.  

**Step 11.** Click "New SSH key."  

**Step 12.** Enter a "Title" (e.g., "for DevOps").  

**Step 13.** Click "Add SSH key" and go back to the CLI. 

### Clone a GitHub Repo Using SSH
**Step 1.** Define your environment variables. 
```bash
export GITUB_ORG="SAIL-Classroom"
export GITUB_REPO="intro-to-github-actions-cyberphor"
```

**Step 2.** Clone the GitHub repo using SSH. 
```bash
git clone git@github.com:${GITHUB_ORG}/${GITHUB_REPO}
```

### Create a GitHub Personal Access Token for the Submitter Program
**Step 1.** Login to GitHub.  
**Step 2.** Click your profile (top-right icon) and click "Settings."  
**Step 3.** Click "Developer Settings" at the bottom of the pane on the left-hand side.  
**Step 4.** Click "Personal access tokens" > "Tokens (classic)."  
**Step 5.** Click "Generate new token" > "Generate new token (classic)."  
**Step 6.** Enter a "Note" (e.g., "Submitter program").  
**Step 7.** Set the "Expiration" date (e.g., 60 days).  
**Step 8.** Select "repo" as the scope.  
**Step 9.** Click "Generate token."  