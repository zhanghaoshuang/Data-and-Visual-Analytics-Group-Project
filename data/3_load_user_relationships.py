import json
import psycopg2
from psycopg2 import sql

with psycopg2.connect(database = "yelp", user = "vorlov", host= "localhost", port = 5432, options="-c search_path=yelp_ds") as conn:
  with conn.cursor() as cursor:
    with open("yelp_academic_dataset_user.json") as users_file:
      commit_count = 0
      for next_user_line in users_file:
        record = json.loads(next_user_line)

        user_id = record["user_id"]

        friendsStr = record["friends"].strip()
        friends = [item.strip() for item in friendsStr.split(",")] if friendsStr else []

        if not len(friends):
          continue

        for next_friend_user_id in friends:
            insertStmt = sql.SQL(
            "INSERT INTO CUSTOMER_RELATIONSHIP (FIRST_USER_ID, SECOND_USER_ID) VALUES " + 
            "({first_user_id}, {second_user_id});").format(
                first_user_id = sql.Literal(user_id),
                second_user_id = sql.Literal(next_friend_user_id)
            )

            try:
                cursor.execute(insertStmt)
                conn.commit()
            except psycopg2.errors.ForeignKeyViolation as ex:
                print(f"FK constraint failed for: first_user_id={user_id}, second_user_id={next_friend_user_id} - {ex}")
                conn.rollback()