# AWS Code Examples

Within this repository are several examples of code written for the AWS Cloud. As a **Certified AWS Cloud Architect**, I have studied and worked with different services within the AWS Cloud. Each folder within this repository gives an example of an architecture in the cloud to solve a specific business goal. Below is a quick preview of the projects you will find in the repo. For more information on any of the projects, please refer to a more in depth ReadMe file in each of the subdirectories.

# AWS Example Projects

## Servelerss Cloud Inventory System

Many businesses both small and large rely on CRUD (**C**reate, **R**ead, **U**pdate and **D**elete) applications to run their business. Utilizing serveless technologies can allow these applications to scale as needed for these businesses. To reliably create this infrastructure, AWS has the SAM framework for writing infrastructure as code in a more conscise manner. Below is the description of AWS SAM from the AWS website.
>**SAM Framework:** The AWS Serverless Application Model (AWS SAM) is an open-source framework for building serverless applications. It provides shorthand syntax to express functions, APIs, databases, and event source mappings. With just a few lines per resource, you can define the application you want and model it using YAML. During deployment, AWS SAM transforms and expands the SAM syntax into AWS CloudFormation syntax, enabling you to save time and build, test, and deploy serverless applications faster.

In this case, I have made a serverless cloud infrastructure for a flower shop. The system is built around a RESTApi which can be built into any front facing client website or application. Each of the endpoints give different capabilities to either query the inventory, record a sale (customers buying from the shop) or record a purchase (the shop buying new inventory for the shop). 

