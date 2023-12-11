# Incident Response

## Training Objectives
* Using Terraform, deploy the infrastructure needed for a given web app
* Using Azure Application Insights, deploy the resources needed to monitor the health of a given web app
* Using Azure Application Insights, identify and mitigate a flaw within a given web app

## Concepts
**Azure App Service**  
The Azure App Service is a Platform-as-a-Service (PaaS) offering to host web apps, mobile backends, and RESTful APIs. 

**Azure App Service Plan**  
An Azure App Service Plan is a resource used to define the app attributes listed below. It represents what you need to rent from Azure to deploy your app.  
* Operating system
* Region
* Number of instances
* Size of instances (e.g., small, medium, or large)
* Pricing tier (Free, Shared, Basic, Standard, Premium, etc.)

**Azure Application Insights**  
Azure Application Insights (AAI) is a feature included with Azure Monitor, a PaaS offering for monitoring apps. An AAI instance is necessary to monitor your app. 

**Azure Application Insight Software Development Kits**
Use the Software Development Kits (SDK) below to get telemetry data from your app into an AAI instance. 
* JavaScript
* Python
* Go (not officially supported)

Below is an example of how you would use the JavaScript SDK to wire your app and AAI instance together. 
```javascript
// APPLICATIONINSIGHTS_CONNECTION_STRING is an environment variable
let appInsights = require("applicationinsights");
appInsights.setup(process.env.APPLICATIONINSIGHTS_CONNECTION_STRING).start();
```

### Continuous Monitoring
**Telemetry**  
Telemetry is the remote measurement of variables.

**Continuous Monitoring**  
Continuous monitoring is the process of observing and *analyzing* the performance and health of apps throughout their lifecycle. It involves the activities listed below.
* Collecting telemetry data from metrics, logs, and traces
* Analyzing telemetry data
* Visualizing telemetry data

**Motivation**  
Organizations perform continuous monitoring to *proactively* (1) identify issues/patterns and (2) make decisions to improve performance and health (e.g., sustainability and security). If we're not monitoring our apps, how do we know when there's an issue before it's too late?

**Benefits**  
DevOps benefits from continuous monitoring for the reasons listed below. 
* It improves the speed of detecting & responding to performance and security issues
* It facilitates continuous improvement

## Solutions
* [Setup](/devops/week-14/HOWTO.md)
* [Task 1](/devops/week-14/HOWTO.md#task-1)
* [Task 2](/devops/week-14/HOWTO.md#task-2)
* [Task 3](/devops/week-14/HOWTO.md#task-3)