import json
import psycopg2
from psycopg2 import sql
from datetime import datetime

with psycopg2.connect(database = "yelp", user = "vorlov", host= "localhost", port = 5432, options="-c search_path=yelp_ds") as conn:
  with conn.cursor() as cursor:
    with open("photos.json") as photos_file:
      for next_photo_line in photos_file:
        record = json.loads(next_photo_line)

        business_id = record["business_id"]
        photo_id = record["photo_id"]

        insertStmt = sql.SQL(
          "INSERT INTO PHOTO(PHOTO_ID, BUSINESS_ID, CAPTION, LABEL) VALUES " + 
          "({photo_id}, {business_id}, {caption}, {label});").format(
            photo_id = sql.Literal(photo_id),
            business_id = sql.Literal(business_id),
            caption = sql.Literal(record["caption"]),
            label = sql.Literal(record["label"])
          )

        try:
          cursor.execute(insertStmt)
          conn.commit()
        except psycopg2.errors.ForeignKeyViolation as ex:
          print(f"FK constraint failed for: photo_id={photo_id}, business_id={business_id} - {ex}")
          conn.rollback()
        except psycopg2.errors.UniqueViolation as uniq_ex:
          print(f"Unique constraint failed for: photo_id={photo_id}, business_id={business_id} - {uniq_ex}")
          conn.rollback()