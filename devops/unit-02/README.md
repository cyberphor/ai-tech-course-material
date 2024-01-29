# Azure DevOps Pipelines: Continuous Deployment

## Topics
* Software Development Life Cycles (e.g., Agile)
* Continuous Deployment
* Test Driven Development
* Unit Tests
* Integration Tests
* Static Code Analysis

## Notes
**Velocity**  
Velocity refers to the speed of software releases.

**Quality**  
Quality refers to how well an artifact fulfills a business requirement.

**Continous Deployment**  
Continous Deployment is a software development process for automatically testing and releasing artifacts to the production environment. CD reduces administrative cost, allowing teams to focus more on making smaller changes and improving software quality. CD should only be adopted by organizations who (1) are confident in the testing and release of their software in production environments and (2) have real-time monitoring capabilities for detecting and responding to feedback.

**Test Driven Development**  
Test Driven Development (TDD) is when you convert software requirements into test cases before evaluating software against them.

**Unit**  
A unit is the smallest testable component of software. A function is an example.

**Unit Testing**  
Unit testing is a software development testing process used to ensure software components meet their individual design and behavior requirements.

**Integration Testing**  
Integration testing is a software development testing process used to ensure software components work together.

**Code Coverage**  
A code coverage report describes how much source code is executed during testing. Higher code coverage values suggest there will be a lower probability of bugs.

**Using the "Classic Interface" vs YAML to Define CI/CD Pipelines in Azure**  
* Classic Interface: CI/CD is defined and executed as two separate pipelines.
* YAML: CI/CD is defined and executed as one pipeline.

**Environments and Stages**  
Below is a list of environments and stages.  
* Development: build, test, audit, deploy
* Staging
* Production

**Public Projects**  
Public projects in Azure DevOps are repositories that can be viewed by anyone on the Internet.  

**Artifacts**  
An artifact is the compiled version of source code. They are the product of a CI (aka "build") pipeline. Artifacts must be published before they are passed to a CD (aka "deploy") pipeline.

**Azure Pipeline Deployment Jobs**  
Deployment jobs within an Azure pipeline are used to take artifacts published in one stage and pass them to another. By default, artifacts are placed in the following file-path: `$(Pipeline.Workspace)/{artifact}`

**SonarCloud**  
SonarCloud is a service used for detecting vulnerabilities and measuring code quality. It's available as an Azure DevOps extension.