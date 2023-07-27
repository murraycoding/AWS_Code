# Serverless Cloud Inventory System
This project showcases the use of AWS SAM to build and deploy AWS Lambda, API Gateway and DynamoDB for inventory and transaction data storage. Below is the walk through and explaination of the AWS SAM Template and the RestAPI diagram.

![Alt serverless cloud inventory system diagram] (https://github.com/murraycoding/AWS_Code/blob/main/flower-shop/Serverless%20Function.drawio.png)

## AWS SAM Template Walkthrough

### Flower Function (AWS Lambda written in Python)
```yaml
flowerFunction:
    Type: AWS::Serverless::Function
    Properties:
        Handler: src/handlers/flowers.get_flower_information
        Runtime: python3.8
        MemorySize: 128
        Timeout: 100
        Description: A function to get the flower information for one or all of the flowers
        Environment:
            Variables:
                # Make table name accessible as environment variable from function code during execution
                INVENTORY_TABLE: !Ref inventoryTable
        Events:
            singleFlowerInfo:
            Type: Api
            Properties:
                Path: /flower/{id}
                Method: GET
                RestApiId:
                    Ref: flowerShopApi
            allFlowerInfo:
                Type: Api
                Properties:
                    Path: /flowers
                    Method: GET
                    RestApiId:
                        Ref: flowerShopApi
```

In AWS SAM, you can define different types of resources, each having their own specific properties. In this case, we have a serverless function. While I will not list out every single property, I will describe the ones I think need at least some explanation. For example, the `MemorySize` property just gives the amount of memory allocated to the Lambda function. The `Handler` lists where the code for the Lambda function is within the source files. The Environment property, in this case, lists variables which can be passed to the Lambda function for use there. In the cases of this function (and others in the project), it gives the reference to the DyanmoDB tables needed for the function. By the least privaledge principle, I have only allowed access to the tables needed by the function and no more. Lastly, the `Events` are what triggers the Lambda function to run. In this case, a RESTApi is being built so the events which trigger the lambda function are end users hitting the API end points listed under `Events`. The two API end points here are:
- `/flower`: Gets the information on a particular flower given the ID of the flower in the DynamoDB table
- `/flowers`: Gets the information on all flowers in the DyanmoDB table

The remainder of the functions will have a less descriptive explaination since most information repeats.

### Health Function (AWS Lambda written in Python)
```yaml
healthFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/health/health_check
      Runtime: python3.8
      MemorySize: 128
      Timeout: 100
      Description: A function to check the status of the API - nothing should be returned exceot for a success message
      Events:
        healthCheck:
          Type: Api
          Properties:
            Path: /health
            Method: GET
            RestApiId:
              Ref: flowerShopApi
```
This function is just to test the status of the API. For debugging purposes, you can hit this API endpoint to rule out an overall API failure in the case that a particular endpoint is not sending the correct response (or any response at all). Below are the endpoints attached to this Lambda function:
- `/health`: An endpoint just to test the 'health' of the API

### Update Inventory Function (AWS Lambda written in Python)
```yaml
updateInventoryFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/update_inventory/update_inventory_func
      Runtime: python3.8
      MemorySize: 128
      Timeout: 100
      Description: A function to update the flower inventory in the DynamoDB table
      Environment:
        Variables:
          # Make table name accessible as environment variable from function code during execution
          INVENTORY_TABLE: !Ref inventoryTable
          TRANSACTION_TABLE: !Ref transactionTable
      Events:
        purchaseRequest:
          Type: Api
          Properties:
            Path: /purchase
            Method: PUT
            RestApiId:
              flowerShopApi
        saleRequest:
          Type: Api
          Properties:
            Path: /sale
            Method: PATCH
            RestApiId:
              flowerShopApi
```
This function is very similar to the flower function in the sole fact that it reaches out to DynamoDB tables. Past this, it goes a lot more. There are two general purposes to this one Lambda function. To record a purchase and to record a sale. For the purposes of this function (and API), a "purchase" is when the shop owner will buy more inventory to hold in the shop for future customers to buy and a "sale" is when a customer makes a purchase from the inventory the shop owner has in stock at the time.

Both of these actions require read and write permissions to the inventory table as well as at least write permissions to the transaction table. This is why they have been written as one AWS Lambda function instead of two separate ones. Another main difference is the HTTP methods which will be used to interact with the databases. The purchase endpoint will either need to make a new record for a new item which needs to be added to the inventory or it will need to modify the inventory of an existing item already in the inventory. The `sale` endpoint should only need to modify the existing database. The `purchase` endpoint can either update an existing product in the inventory or add a completely new product to the inventory databse.

### DynamoDB Tables
```yaml
# dyanmodb tables
  inventoryTable:
    Type: AWS::Serverless::SimpleTable
    Properties:
      PrimaryKey:
        Name: id
        Type: String

  transactionTable:
    Type: AWS::Serverless::SimpleTable
    Properites:
      PrimaryKey:
        Name: transactionId
        Type: String
```
Nothing special here, just the listing in the SAM template for the two DyanmoDB tables. There are many other properties you can add here to customize the tables, but these are the basics.

### API Gateway
```yaml
# API information
  flowerShopApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
```
Simple again, just the minimum properties to get an RESTApi going. The important thing here is the name of the API in the template (`flowerShopApi`) is referenced in the template code for the Lambda function. This allows the Lambda functions to all be connected to the singular API.

### Connectors
```yaml
# Connectors
  flowerFunctionToInventoryTableConnector:
    Type: AWS::Serverless::Connector
    Properties:
      Source:
        Id: flowerFunction
      Destination:
        Id: inventoryTable
      Permissions:
        - Read

  updateInventoryFunctionToInventoryTableConnector:
    Type: AWS::Serverless::Connector
    Properties:
      Source:
        Id: updateInventoryFunction
      Destination:
        Id: inventoryTable
      Permissions:
        - Read
        - Write

  updateInventoryFunctionToTransactionTableConnector:
    Type: AWS::Serverless::Connector
    Properties:
      Source:
        Id: updateInventoryFunction
      Destination:
        Id: transactionTable
      Permissions:
        - Write
```

Connectors are what allow  the programatic permissions between different AWS resources. For example, the `flowerFunctionToInventroyTableConnector` simply allows the `FlowerFunction` to *connect* to the `InventoryTable`. In the same template, you also define the permissions. Keep in mind it is always considered a best practice to define permissions with the least privaledge principle in mind. Here I have made the connects with only the needed permissions (and nothing more). 







