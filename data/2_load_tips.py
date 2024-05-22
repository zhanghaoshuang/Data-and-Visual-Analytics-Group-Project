import json
import psycopg2
from psycopg2 import sql
from datetime import datetime

with psycopg2.connect(database = "yelp", user = "vorlov", host= "localhost", port = 5432, options="-c search_path=yelp_ds") as conn:
  with conn.cursor() as cursor:
    with open("yelp_academic_dataset_tip.json") as tips_file:
      for next_tip_line in tips_file:
        record = json.loads(next_tip_line)

        business_id = record["business_id"]
        user_id = record["user_id"]
        next_timestamp = datetime.strptime(record["date"], "%Y-%m-%d %H:%M:%S")

        insertStmt = sql.SQL(
          "INSERT INTO TIP(USER_ID, BUSINESS_ID, DATE, TEXT, COMPLIMENT_COUNT) VALUES " + 
          "({user_id}, {business_id}, {date}, {text}, {compliment_count});").format(
            user_id = sql.Literal(user_id),
            business_id = sql.Literal(business_id),
            date = sql.Literal(next_timestamp),
            text = sql.Literal(record["text"]),
            compliment_count = sql.Literal(record["compliment_count"])
          )

        try:
          cursor.execute(insertStmt)
          conn.commit()
        except psycopg2.errors.ForeignKeyViolation as ex:
          print(f"FK constraint failed for: user_id={user_id}, business_id={business_id} - {ex}")
          conn.rollback()