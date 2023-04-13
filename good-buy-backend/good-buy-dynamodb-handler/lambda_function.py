'''
This module defines the lambda function that will return interact with
the DynamoDB database. When invoked, it will take an event as input
and take query string parameters or body data from it.
'''

import json
import os
from abc import ABC, abstractmethod
import boto3
# from dotenv import load_dotenv

# load_dotenv()

    # "resource":"/database/shopping-cart",
    # "path":"/database/shopping-cart",
    # "httpMethod":"GET",
    # shopping cart has an ID so have an ID parameter
    # if event['path'] == '/database/shopping-cart' or have a variable with this value

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('Users')

access_key = os.getenv('ACCESS_KEY')

secret_access_key = os.getenv('SECRET_ACCESS_KEY')

session = boto3.Session(aws_access_key_id = access_key,
aws_secret_access_key = secret_access_key,
region_name = "us-east-1")

db = session.resource("dynamodb")




def lambda_handler(event):
    '''Lambda function that will take in an event and perform
    different actions depending on the path and HTTP Method
    sent in the event parameter.
    '''
    print(event)
    # When using this path and method, must provide ID of the shopping
    # cart you want to retrieve as a query parameter.
    if event['path'] == '/database/shopping-cart' and event['httpMethod'] == 'GET':
        table = db.Table("Shopping_Cart")
        get_action = GetAction(event, table)
        response = get_action.action()
        # print(response['Item']['cart'])
        print(response['Item'])
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item']['cart'], indent=2,default=str)
        }
    # When using this path and method, must provide ID of the user account you
    # want to retrieve as a query parameter.
    if event['path'] == '/database/user-account' and event['httpMethod'] == 'GET':
        table = db.Table("Users")
        get_action = GetAction(event, table)
        response = get_action.action()
        print(response['Item'])
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'], indent=2,default=str)
        }
    # When using this path and method, must provide the ID and the cart
    # values the newly created cart as json body data.
    if event['path'] == '/database/shopping-cart' and event['httpMethod'] == 'POST':
        table = db.Table("Shopping_Cart")
        decoded_event = json.loads(event['body'])
        item ={
                'ID': int(decoded_event['ID']),
                'cart': decoded_event['cart']
        }
        post_action = PostAction(event, table, item)
        response = post_action.action()
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            'body': 'Created new shopping cart'
        }
    # When using this path and method, must provide the ID email, password,
    # phone, and username values the newly created cart as json body data.
    if event['path'] == '/database/user-account' and event['httpMethod'] == 'POST':
        table = db.Table("Users")
        decoded_event = json.loads(event['body'])
        item ={
                'ID': int(decoded_event['ID']),
                'email': decoded_event['email'],
                'password': decoded_event['password'],
                'phone': decoded_event['phone'],
                'username': decoded_event['username']
            }
        post_action = PostAction(event, table, item)
        response = post_action.action()
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            'body': 'Created new user account'
        }

    # Idea for updating cart
    # When an item is added or removed from the cart,
    # it should send body data of the updated cart.
    # Then retrieve that body data to update it with.
    # When using this path and method, send the ID of the
    # shopping cart you want to update as a query parameter and then
    # pass the new cart data as body data.
    if event['path'] == '/database/shopping-cart' and event['httpMethod'] == 'PUT':
        table = db.Table("Shopping_Cart")
        decoded_event = json.loads(event['body'])

        update_expression = "SET cart =:cart"
        expression_attribute_values = {
            ':cart' : decoded_event['cart']
        }

        # decodedExpressionAttributes = json.dumps(expression_attribute_values)

        put_action = PutAction(event, table, update_expression, expression_attribute_values)
        response = put_action.action()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            'body': 'Updated a shopping cart'
        }
    # When using this path and method, must pass the ID of
    # the user accound you want to update as a query parameter,
    # and then pass the new user acount data as body data.
    if event['path'] == '/database/user-account' and event['httpMethod'] == 'PUT':

        table = db.Table("Users")
        decoded_event = json.loads(event['body'])

        update_expression = "SET password = :password, phone = :phone, username = :username"
        expression_attribute_values = {
            ':password' : decoded_event['password'],
            ':phone' : decoded_event['phone'],
            ':username': decoded_event['username']
        }

        put_action = PutAction(event, table, update_expression, expression_attribute_values)
        response = put_action.action()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            'body': 'Updated a user account'
        }
    # When using this path and method, must pass the ID of the shopping cart
    # that you want to delete as a query parameter.
    if event['path'] == '/database/shopping-cart' and event['httpMethod'] == 'DELETE':
        table = db.Table("Shopping_Cart")

        delete_action = DeleteAction(event, table)
        response = delete_action.action()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            'body': 'Deleted a shopping cart'
        }
    # When using this path and method, must pass the ID of the user
    # acount you want to delete at query parameter.
    if event['path'] == '/database/user-account' and event['httpMethod'] == 'DELETE':
        table = db.Table("Users")

        delete_action = DeleteAction(event, table)
        response = delete_action.action()

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            'body': 'Deleted a user account'
        }
    return None

class DBActionInterface(ABC):
    '''
    Interface for action that will interact with
    the DynamoDB database.
    '''
    @abstractmethod
    def action(self):
        '''Perform action'''

class GetAction(DBActionInterface):
    '''
    This class defines that will perform a GET action on the 
    DynamoDB database. This class takes an event parameter and
    a table parameter. After action is performed it will
    return response.
    '''
    def __init__(self, event, table):
        self.event = event
        self.table = table

    def action(self):
        # print(event['queryStringParameters']['ID'])
        id_value = self.event['queryStringParameters']['ID']
        response = self.table.get_item(
            Key = {
                'ID': int(id_value)
            }
        )
        return response

class PostAction(DBActionInterface):
    '''
    This class defines that will perform a POST action on the 
    DynamoDB database. This class takes an event parameter and
    a table parameter and an Item parameter. After action is performed
    it will return response.
    '''
    def __init__(self, event, table, item):
        self.event = event
        self.table = table
        self.item = item

    def action(self):
        response = self.table.put_item(
            Item = self.item
        )
        return response

class PutAction(DBActionInterface):
    '''
    This class defines that will perform a PUT action on the 
    DynamoDB database. This class takes an event parameter and
    a table parameter an updateExpression parameter, and an
    expressionAttributeValues parmeter. After action is performed it will
    return response.
    '''
    def __init__(self, event, table, update_expression, expression_attribute_values):
        self.event = event
        self.table = table
        self.update_expression = update_expression
        self.expression_attribute_values = expression_attribute_values

    def action(self):
        id_value = self.event['queryStringParameters']['ID']
        # decodedExpressionAttributes = json.loads(self.expressionAttributeValues)
        response = self.table.update_item(
            Key = {
                'ID' : int(id_value)
            },
            UpdateExpression = self.update_expression,
            ExpressionAttributeValues = self.expression_attribute_values
        )
        return response

class DeleteAction(DBActionInterface):
    '''
    This class defines that will perform a DELETE action on the 
    DynamoDB database. This class takes an event parameter and
    a table parameter. After action is performed it will
    return response.
    '''
    def __init__(self, event, table):
        self.event = event
        self.table = table
    def action(self):
        id_value = self.event['queryStringParameters']['ID']
        response = self.table.delete_item(
            Key = {
                'ID' : int(id_value)
            }
        )
        return response
