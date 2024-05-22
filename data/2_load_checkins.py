import json
import psycopg2
from psycopg2 import sql
from datetime import datetime

with psycopg2.connect(database = "yelp", user = "vorlov", host= "localhost", port = 5432, options="-c search_path=yelp_ds") as conn:
  with conn.cursor() as cursor:
    with open("yelp_academic_dataset_checkin.json") as checkins_file:
      for next_checkin_line in checkins_file:
        record = json.loads(next_checkin_line)

        business_id = record["business_id"]
        date_list = record["date"].split(",")

        for next_date in date_list:

            next_timestamp = datetime.strptime(next_date.strip(), '%Y-%m-%d %H:%M:%S')

            insertStmt = sql.SQL(
            "INSERT INTO CHECKIN(BUSINESS_ID, DATE) VALUES " + 
            "({business_id}, {date});").format(
                business_id = sql.Literal(business_id),
                date = sql.Literal(next_timestamp),
            )

            try:
                cursor.execute(insertStmt)
                conn.commit()
            except psycopg2.errors.ForeignKeyViolation as ex:
                print(f"FK constraint failed for: business_id={business_id} - {ex}")
                conn.rollback()
                break