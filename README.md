# Content
* [Setup Guides](#setup-guides)
* [Cloud Administrator](#cloud-administrator)
* [Python](#python)
* [DevOps](#devops)
* [Data Engineering](#data-engineering)
* [Cloud-Native](#cloud-native)

## Setup Guides
* [Create SSH Keys](/SETUP.md#how-to-create-ssh-keys)
* [Setup Single Sign-On (SSO) Using SSH](/SETUP.md#how-to-setup-single-sign-on-using-ssh)
* [Add Your SSH Public Key to GitHub](/SETUP.md#how-to-add-your-ssh-public-key-to-github)
* [Create a GitHub Personal Access Token](/SETUP.md#how-to-create-a-github-personal-access-token)
* [Create an Azure DevOps Personal Access Token](/SETUP.md#how-to-create-an-azure-devops-personal-access-token)
* [Install the Azure CLI](/SETUP.md#how-to-install-the-azure-cli)
* [Install Terraform](/SETUP.md#how-to-install-terraform)
* [Install Ansible](/SETUP.md#how-to-install-ansible)
* [Install sqlcmd](/SETUP.md#how-to-install-sqlcmd)

## Cloud Administrator
| Topic                                                              | Training Objectives |
| ------------------------------------------------------------------ | ------------------- |
| [Getting Started with Azure](/cloud-admin/unit-01/README.md)       | <ul><li>Set up an Azure account and an Azure subscription.</li><li>Practice using the Azure Cloud Shell and Azure CLI.</li><li>Examine the details of Azure account and subscription.</li><li>Explore the Azure quickstart to create a static HTML web app.</li><li>Experiment using the Azure portal to create a virtual machine.</li><li>Experiment hosting a web service on a virtual machine.</li></ul>
| [Resource Management](/cloud-admin/unit-02/README.md)            | <ul><li>Explain the definition and purposes of an Azure subscription.</li><li>Describe the relationship between Azure subscriptions and resource groups.</li><li>Interpret how Azure subscriptions are used in real-world scenarios.</li><li>Practice to provision virtual machines with the Azure CLI.</li><li>Practice moving resources between subscriptions with the Azure CLI.</li></ul>
| [Access Control](/cloud-admin/unit-03/README.md)           | <ul><li>Explain the definition and purpose of Azure Active Directory (aka Azure AD or AAD).</li><li>Explain the definition of a domain name in the Azure Active Directory.</li><li>Manipulate the association between directories and subscriptions.</li><li>Practice managing Azure Active Directories users.</li><li>Explore the characteristics and use cases of Role-Based-Access-Control (RBAC).</li><li>Demonstrate how to create groups, and manage group members and group owners.</li><li>Operate on a hierarchical Azure Active Directory to match the organizational structure.</li><li>Practice managing access to resources and applications in Azure Active Directory.</li><li>Demonstrate how to configure an Azure AD directory to match a real-world.
| [Resource Provisioning](/cloud-admin/unit-04/README.md)           | <ul><li>Provision and configure a virtual network, subnet, and network security group on Azure.</li><li>Provision Azure virtual machines to host public web server and private database server.</li><li>Automate post-deployment configuration of Azure virtual machines using bash scripts stored on Azure Storage.</li><li>Experiment with network diagnostic tools to test the external connectivity between the Internet and virtual machines and the internal connectivity between virtual machines.</li><li>Update security rules of network security groups to meet the changes of network traffic requirements.</li></ul>
| [Scalability](/cloud-admin/unit-05/README.md) | <ul><li>Explain the definition and purpose of scaling.</li><li>Practice vertical scaling by changing the size of the virtual machines on Azure.</li><li>Practice horizontal scaling by changing the number of virtual machines on Azure.</li><li>Experiment with tools of system benchmarking and load testing.</li><li>Practice provisioning a scale set to host a web service and tune the size and number of instances to meet the requirements for performance and cost.</li></ul>
| [Infrastructure-as-Code](/cloud-admin/unit-06/README.md)           | <ul><li>Illustrate how the infrastructure evolves over time with growing complexity and scale.</li><li>Describe the advantages of Infrastructure as Code with real-world scenarios.</li><li>Explain the difference between declarative and imperative approaches to manage infrastructure.</li><li>Practice using basic Terraform CLI commands with a prepared example to create a web app in Azure.</li><li>Experiment with provisioners in Terraform to install and start a web service on a virtual machine.</li><li>Explain and practice input variables and output values of Terraform.</li><li>Explain how Terraform stores infrastructure as states and makes incremental changes leveraging the desired state.</li><li>Modify prepared Terraform scripts and apply incremental infrastructure changes.</li><li>Explain resource dependencies in Terraform with examples and visualize the dependencies with graphs.</li></ul>
| [Monitoring Cloud Services](/cloud-admin/unit-07/README.md)         | <ul><li>Explain the concept and benefits of cloud monitoring.</li><li>Practice configuring autoscale settings of Azure Web App plan using both the Azure portal and Terraform.</li><li>Configure autoscale settings to collect resource metrics and trigger scale actions.</li><li>Explain the workflow of an alert to trigger an action group.</li><li>Practice configuring an availability test of a web app on Azure and set up an alert for test failures using both the Azure portal and Terraform.</li></ul>
| [Cloud Security](/cloud-admin/unit-08/README.md)        | <ul><li>Discuss the security requirements for deploying applications on the cloud.</li><li>Explain how a multi-layered security strategy provides protection against different and potentially unrelated attack vectors.</li><li>Explain the three ways in which access can be allowed, and denied, for an Azure SQL database.</li><li>Configure firewall rules for an Azure SQL database to implement the Network layer of a multi-layered security strategy.</li><li>Enable server-level auditing on an Azure SQL database to implement the Auditing and Threat Protection layer of a multi-layered security strategy.</li></ul>
| [Backup and Disaster Recovery](/cloud-admin/unit-09/README.md)                     | <ul><li>Describe the importance of business continuity and disaster recovery (BCDR)</li><li>Describe the two solutions provided by Azure Backup service and Azure Site Recovery service to enable the BCDR strategy</li><li>Set up backup on a VM, configure a backup policy, restore from backup with Azure Backup</li><li>Explain, compare, and apply failover and failback operations</li><li>Configure, test, and trigger the failover to the secondary region with Azure Site Recovery</li><li>Experiment with Azure Traffic Manager to deploy a geo-replicated web service</li></ul>
| [Docker and Kubernetes](/cloud-admin/unit-10/README.md)            | <ul><li>Describe Docker and Kubernetes and how a developer uses them to implement a microservices architecture (MSA).</li><li>Build docker images to containerize microservices and push the images into Azure Container Registry.</li><li>Provision, configure, and manage Kubernetes clusters.</li><li>Deploy containerised microservices on the cloud using Kubernetes.</li></ul>

## Python
| Topic                                                              | Training Objectives |
| ------------------------------------------------------------------ | ------------------- |
| [Types, Variables, and Functions](/python/unit-01/README.md)       |
| [Strings](/python/unit-02/README.md)                               |
| [Data Structures](/python/unit-04/README.md)                       | 
| [Files](/python/unit-06/README.md)                                 |
| [Object-Oriented Programming](/python/unit-08/README.md)           |
| [Debugging, Refactoring, Testing, and Packaging](/python/unit-10/) |
| [Data Stores](/python/unit-12/README.md)                           | 
| [Web Scraping](/python/unit-13/README.md)                          |
| [Data Analysis](/python/unit-14/README.md)                         |

## DevOps
| Topic                                                    | Training Objectives |
| -------------------------------------------------------- | ------------------- |
| [Git, GitHub, and Azure DevOps](/devops/unit-00/README.md) | <ul><li>Create a GitHub Personal Access Token</li><li>Create an Azure DevOps Personal Access Token</li><li>Create an Azure DevOps Project</li><li>Purchase an Azure DevOps Parallel Job for an Organization</li><li>Configure Git</li><li>Clone a Repo Using SSH</li><li>Create a Branch</li><li>Add a GitHub Action</li><li>Push a Commit</li></ul>
| [Continuous Integration (CI)](/devops/unit-01/README.md) |
| [Continuous Deployment (CD)](/devops/unit-02/README.md)  |
| [Azure DevOps Pipelines](/devops/unit-03/README.md)      |
| [GitHub Actions](/devops/unit-04/README.md)              |
| [Containers](/devops/unit-05/README.md)                  |
| [Serverless Functions](/devops/unit-06/README.md)        | <ul><li>Create a serverless function</li><li>Create a CI/CD pipeline for a serverless function</li><li>Implement a Blue/Green deployment strategy for a serverless function</li></ul>
| [Infrastructure as Code](/devops/unit-07/README.md)      |
| [Incident Response](/devops//unit-08/README.md)          |

## Cloud-Native
| Topic                                                        | Training Objectives |
| ------------------------------------------------------------ | ------------------- |
| [Monolith to Microservices](/cloud-native/unit-01/README.md) | <ul><li>Deploy a virtual machine and monolithic application using Packer</li><li>Deploy a Java application using Docker</li><li>Create a container registry and push images to it</li><li>Deploy containers using the Azure Kubernetes Service</li><li>Deploy Helm charts to manage a Kubernetes cluster</li></ul>
| [Serverless Deployment and Autoscaling](/cloud-native/unit-02/README.md) | <ul><li>Develop simple Python-based REST APIs</li><li>Utilize best practices to package and containerize a Python microservice application</li><li>Configure and deploy containers on Azure Container Instances</li><li>Orchestrate Kubernetes Pod resource limits of a developed microservice</li><li>Configure and deploy function triggers with Terraform given a stream of events</li><li>Utilize Goldilocks and vertical pod autoscaling to minimize resource costs</li><li>Develop simple scaling policies to ensure high uptime</li></ul>
| [API Gateway](/cloud-native/unit-03/README.md) | <ul><li>Differentiate between the kinds of service discovery systems that Kubernetes provides, and the kinds of systems that it does not.</li><li>Develop Gateway API-tolerant Reverse Proxies with Nginx Gateway Fabric.</li><li>Obtain SSL Certificates using Let's Encrypt and enable HTTPS traffic with a domain name.</li><li>Configure KrakenD to make use of its capabilities as an API Gateway, providing rate limiting and route redirection.</li><li>Connect an application gateway in the middle of an external and internal load balancer, understanding the benefits and tradeoffs.</li><li>Develop a simple query service using Django-REST-Framework.</li><li>Develop a simple JWT-based authentication system using the simplejwt library.</li><li>Connect the authentication system with KrakenD and enable API-specific authentication.</li><li>Configure and update a changing networking landscape when using two independent services.</li></ul>

## Data Engineering
| Topic                                                                   | Training Objectives |
| ----------------------------------------------------------------------- | ------------------- |
| [Introduction to Data Engineering](/data-engineering/unit-01/README.md) | <ul><li>Use `grep`, `sed`, and `awk` to clean data</li><li>Use `pandas` to extract data</li><li>Use `pandas` to analyze data</li><li>Use `pandas` to transform data</li></ul>
| [Relational Databases](/data-engineering/unit-02/README.md) | <ul> <li>Use `pandas` to clean, transform, and prepare data</li></li><li>Load data into a MySQL database</li><li>Perform SQL queries</li><li>Create and loads records into a SQL database table</li><li>Modify a SQL database tables (e.g., add and remove columns)</li><li>Query and filter records from SQL database tables</li><li>Merge multiple SQL database tables</li></ul>
| [NoSQL Databases](/data-engineering/unit-03/README.md) | <ul><li>Compare NoSQL databases to the relational databases based on SQL.</li><li>Deploy and configure a fully managed multi-model database on Azure with MongoDB API.</li><li>Ingest data from a local JSON file into the managed database on Azure.</li><li>Perform extraction, transformation, and loading (ETL) process on a raw dataset.</li><li>Practice writing efficient MongoDB queries using the Azure Cosmos DB's API for MongoDB.</li><li>Gather insights from a dataset residing in Azure Cosmos DB.</li><li>Implement and evaluate MongoDB indexing to improve the performance of MongoDB queries.</li></ul>
| [Data Processing with Spark](/data-engineering/unit-04/README.md) | <ul><li>Explore big data processing with Spark and MapReduce.</li><li>Compare non-iterative batch processing (Hadoop) vs. iterative batch processing (Spark).</li><li>Explain RDDs, transformations, actions in Spark job execution.</li><li>Develop Spark apps with interactive programming in Azure Databricks Notebooks.</li><li>Use cloud managed services for Spark apps, like Azure Databricks.</li><li>Write Spark applications using RDD and DataFrame APIs.</li></ul>
