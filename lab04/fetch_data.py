import pandas as pd
import boto3
import simplejson as json

def prepare_data(event, context):
  client = boto3.resource("dynamodb")
  s3_client = boto3.resource("s3")

  rating_table = client.Table("ratings")
  movie_table = client.Table("movies")

  rating_table.put_item(Item={"id": int(event["movieID"]), "user": event["user"], "rating": event["rating"]})


  df_uratings = pd.read_json(json.dumps(rating_table.scan()["Items"]), orient="records")
  df_movies = pd.read_json(json.dumps(movie_table.scan()["Items"]), orient="records")

  users = set(df_uratings["user"])
  movies = set(df_uratings["id"])


  s3_client.Bucket("movierecommenderdata").put_object(Key="user.json", Body=bytes(json.dumps(event["user"]).encode('UTF-8')))
  

  return {
    "users": list(users),
    "movies": list(movies),
    "df_uratings": df_uratings.to_json(orient="records"),
    "df_movies": df_movies.to_json(orient="records")
    }
