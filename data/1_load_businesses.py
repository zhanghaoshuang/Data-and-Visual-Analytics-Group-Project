import json
import psycopg2
from psycopg2 import sql
from psycopg2.extras import Json

with psycopg2.connect(database = "yelp", user = "postgres", host= "localhost", port = 5432, options="-c search_path=yelp_ds") as conn:
  with conn.cursor() as cursor:
    with open("yelp_academic_dataset_business.json") as businesses_file:
      commit_count = 0
      for next_business_line in businesses_file:
        record = json.loads(next_business_line)

        insertStmt = sql.SQL(
          "INSERT INTO BUSINESS(BUSINESS_ID, NAME, ADDRESS, CITY, STATE, POSTAL_CODE, LATITUDE, LONGTITUDE, STARS, REVIEW_COUNT, IS_OPEN, ATTRIBUTES, CATEGORIES, HOURS) VALUES " + 
          "({business_id}, {name}, {address}, {city}, {state}, {postal_code}, {latitude}, {longitude}, {stars}, {review_count}, {is_open}, {attributes}, {categories}, {hours});").format(
            business_id = sql.Literal(record["business_id"]),
            name = sql.Literal(record["name"]),
            address = sql.Literal(record["address"]),
            city = sql.Literal(record["city"]),
            state = sql.Literal(record["state"]),
            postal_code = sql.Literal(record["postal_code"]),
            latitude = sql.Literal(record["latitude"]),
            longitude = sql.Literal(record["longitude"]),
            stars = sql.Literal(record["stars"]),
            review_count = sql.Literal(record["review_count"]),
            is_open = sql.Literal(bool(record["is_open"])),
            attributes = sql.Literal(json.dumps(record["attributes"])),
            categories = sql.Literal(json.dumps(record["categories"])),
            hours = sql.Literal(json.dumps(record["hours"]))
          )

        cursor.execute(insertStmt)

        if (commit_count > 32):
          conn.commit()
          commit_count = 0
        else:
          commit_count += 1

    conn.commit()