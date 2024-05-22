import json
import psycopg2
from psycopg2 import sql
from datetime import datetime

with psycopg2.connect(database = "Yelp", user = "postgres", password="sooners", host= "localhost", port = 5432, options="-c search_path=yelp_ds") as conn:
  with conn.cursor() as cursor:
    with open("yelp_academic_dataset_review.json",encoding= "UTF-8") as users_file:
      for next_user_line in users_file:
        record = json.loads(next_user_line)

        review_id = record["review_id"]
        user_id = record["user_id"]
        business_id = record["business_id"]
        next_timestamp = datetime.strptime(record["date"], "%Y-%m-%d %H:%M:%S")

        insertStmt = sql.SQL(
          "INSERT INTO REVIEW(REVIEW_ID, USER_ID, BUSINESS_ID, DATE, TEXT, STARS, USEFUL, FUNNY, COOL) VALUES " + 
          "({review_id}, {user_id}, {business_id}, {date}, {text}, {stars}, {useful}, {funny}, {cool});").format(
            review_id = sql.Literal(review_id),
            user_id = sql.Literal(user_id),
            business_id = sql.Literal(business_id),
            date = sql.Literal(next_timestamp),
            text = sql.Literal(record["text"]),
            stars = sql.Literal(record["stars"]),
            useful = sql.Literal(record["useful"]),
            funny = sql.Literal(record["funny"]),
            cool = sql.Literal(record["cool"])
          )

        try:
          cursor.execute(insertStmt)
          conn.commit()
        except psycopg2.errors.ForeignKeyViolation as ex:
          print(f"FK constraint failed for: review_id={review_id}, user_id={user_id}, business_id={business_id} - {ex}")
          conn.rollback()