from decimal import Decimal
import boto3
import simplejson as json

from flask import Flask, request, Response, request

app = Flask(__name__)
client = boto3.resource("dynamodb")

@app.route("/movies", methods=["GET"])
def get_movies():
  return json.dumps(scan_entire_table("movies"), use_decimal=True)

@app.route("/movies/create", methods=["POST"])
def create_movie_table():
  create_movies_table()
  return Response(status=204)

@app.route("/movies", methods=["POST"])
def save_movies():
  import_items("movies", json.loads(request.data, use_decimal=True))
  return Response(status=204)

@app.route("/ratings", methods=["GET"])
def get_ratings():
  return json.dumps(scan_entire_table("ratings"), use_decimal=True)

@app.route("/ratings/create", methods=["POST"])
def create_rating_table():
  create_ratings_table()
  return Response(status=204)

@app.route("/ratings", methods=["POST"])
def save_ratings():
  import_items("ratings", json.loads(request.data, use_decimal=True))
  return Response(status=204)

@app.route("/recommendation", methods=["POST"])
def start_recommendation():
  step_function_cli = boto3.client("stepfunctions")
  response = step_function_cli.start_execution(
    stateMachineArn="arn:aws:states:eu-central-1:532990971325:stateMachine:Movie-Recommendation-Lab04",
    input=request.get_data(as_text=True)
  )
  print(response["executionArn"])
  state_machine = step_function_cli.describe_execution(executionArn=response["executionArn"])
  while(state_machine["status"] == "RUNNING"):
    state_machine = step_function_cli.describe_execution(executionArn=response["executionArn"])
  
  return state_machine["output"]

@app.route("/users/create", methods=["POST"])
def create_user_table():
  create_users_table()
  return Response(status=204)

@app.route("/users", methods=["GET"])
def get_users():
  return json.dumps(scan_entire_table("users"), use_decimal=True)

@app.route("/users", methods=["POST"])
def save_users():
  import_users("users", json.loads(request.data, use_decimal=True))
  return Response(status=204)

def scan_entire_table(name):
  table = client.Table(name)
  response = table.scan(ReturnConsumedCapacity="TOTAL")
  items = response['Items']
  while 'LastEvaluatedKey' in response:
      print(response['LastEvaluatedKey'])
      response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
      items.extend(response['Items'])

  return items

def import_items(table_name, items):
  table = client.Table(table_name)
  for item in items:
    print(f"Saving: {item}")
    table.put_item(Item=item)

def import_users(table_name, users):
  table = client.Table(table_name)
  for user in users:
    print(f"Saving: {user}")
    table.put_item(Item={"user": user})

def create_movies_table(): 
  client.create_table(
    TableName="movies",
    KeySchema=[
      {
        "AttributeName": "id",
        "KeyType": "HASH"
      },
      {
        "AttributeName": "title",
        "KeyType": "RANGE"
      }
    ],
    AttributeDefinitions=[
      {
        "AttributeName": "id",
        "AttributeType": "N"
      },
      {
        "AttributeName": "title",
        "AttributeType": "S"
      }
    ],
    ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
    }
  )


def create_ratings_table():
  client.create_table(
    TableName="ratings",
    KeySchema=[
      {
        "AttributeName": "id",
        "KeyType": "HASH"
      }
      ,
      {
        "AttributeName": "user",
        "KeyType": "RANGE"
      }
    ],
    AttributeDefinitions=[
      {
        "AttributeName": "id",
        "AttributeType": "N"
      },
      {
        "AttributeName": "user",
        "AttributeType": "S"
      }
    ],
    ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
    }
  )

def create_users_table():
  client.create_table(
    TableName="users",
    KeySchema=[
      {
        "AttributeName": "user",
        "KeyType": "HASH"
      }
    ],
    AttributeDefinitions=[
      {
        "AttributeName": "user",
        "AttributeType": "S"
      }
    ],
    ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
    }
  )

if __name__ == "__main__":
  app.run(threaded=True, host='0.0.0.0', port=5000)