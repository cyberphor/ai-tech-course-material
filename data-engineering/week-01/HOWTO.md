# Data Engineering
## Task 01
**Step 1.** Deploy a virtual machine in Azure and login to it. 
```bash
terraform -chdir=terraform init
terraform -chdir=terraform plan
terraform -chdir=terraform apply -auto-approve
```

**Step 2.** Download, unzip, and change directories to the provided data set for Task 1. 
```bash
wget https://clouddataengineer.blob.core.windows.net/data-exploration/handout/project-data-exploration.zip
unzip project-data-exploration.zip
cd project-data-exploration/task1
```

**Step 3.** Update the `find_confidential.sh` script so it includes the command below. 
```bash
grep -i -r -l "confidential" emails
```

**Step 4.** Update the `count_confidential.sh` script so it includes the command below. 
```bash
grep -i -r -l "confidential" emails | wc -l
```

**Step 5.** Update the `find_phone_numbers.sh` script so it includes the command below. 
```bash
grep -i -r -l -P '\b\d{3}[\W]*\d{3}[\W]*\d{4}\b' emails
```

**Step 6.** Update the `count_phone_numbers.sh` script so it includes the command below. 
```bash
grep -i -r -l -P '\b\d{3}[\W]*\d{3}[\W]*\d{4}\b' emails | wc -l
```

**Step 7.** Update the `hide_phone_numbers.sh` script so it includes the command below. 
```bash
# -r tells sed to use extended regular expressions (so you don't have to escape everything)
# \b defines a boundary
# \W* zero or more non-word characters
# [0-9]{3} three numbers
sed -r 's/\b[0-9]{3}\W*[0-9]{3}\W*[0-9]{4}\b/<PHONE_REMOVED>/gI' anon_"$file_name"_ > anon_"$file_name"
```

**Step 8.** Update the `find_course.sh` script so it includes the command below. 
```bash
awk -F '\t' '$2 ~ /Python/ && $4 == "False" {print $2}' udemy_courses_v2.csv 
```