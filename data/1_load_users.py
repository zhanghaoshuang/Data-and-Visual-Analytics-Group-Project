import json
import psycopg2
from psycopg2 import sql
from datetime import datetime

with psycopg2.connect(database = "Yelp", user = "postgres", password="sooners", host= "localhost", port = 5432, options="-c search_path=yelp_ds") as conn:
  with conn.cursor() as cursor:
    with open("yelp_academic_dataset_user.json",encoding= "UTF-8") as users_file:
      commit_count = 0
      for next_user_line in users_file:
        record = json.loads(next_user_line)

        friendsStr = record["friends"].strip()
        friends = [item.strip() for item in friendsStr.split(",")] if friendsStr else []

        eliteStr = record["elite"].strip()
        elite = [int(item.strip()) for item in eliteStr.split(",")] if eliteStr else []

        yelping_since_ts = datetime.strptime(record["yelping_since"], "%Y-%m-%d %H:%M:%S")

        insertStmt = sql.SQL(
          "INSERT INTO CUSTOMER (" + 
          "USER_ID, NAME, REVIEW_COUNT, YELPING_SINCE, FRIENDS, USEFUL, FUNNY, COOL, FANS, ELITE, AVERAGE_STARS, " +
          "COMPLIMENT_HOT, COMPLIMENT_MORE, COMPLIMENT_PROFILE, COMPLIMENT_CUTE, COMPLIMENT_LIST, COMPLIMENT_NOTE, " + 
          "COMPLIMENT_PLAIN, COMPLIMENT_COOL, COMPLIMENT_FUNNY, COMPLIMENT_WRITER, COMPLIMENT_PHOTOS" +
          ") VALUES " + 
          "({user_id}, {name}, {review_count}, {yelping_since}, {friends}, {useful}, {funny}, {cool}, {fans}, {elite}, {average_stars}, " + 
          "{compliment_hot}, {compliment_more}, {compliment_profile}, {compliment_cute}, {compliment_list}, {compliment_note}, " + 
          "{compliment_plain}, {compliment_cool}, {compliment_funny}, {compliment_writer}, {compliment_photos}" +
          ");").format(
            user_id = sql.Literal(record["user_id"]),
            name = sql.Literal(record["name"]),
            review_count = sql.Literal(record["review_count"]),
            yelping_since = sql.Literal(yelping_since_ts),
            friends = sql.Literal(friends),
            useful = sql.Literal(record["useful"]),
            funny = sql.Literal(record["funny"]),
            cool = sql.Literal(record["cool"]),
            fans = sql.Literal(record["fans"]),
            elite = sql.Literal(elite),
            average_stars = sql.Literal(record["average_stars"]),
            compliment_hot = sql.Literal(record["compliment_hot"]),
            compliment_more = sql.Literal(record["compliment_more"]),
            compliment_profile = sql.Literal(record["compliment_profile"]),
            compliment_cute = sql.Literal(record["compliment_cute"]),
            compliment_list = sql.Literal(record["compliment_list"]),
            compliment_note = sql.Literal(record["compliment_note"]),
            compliment_plain = sql.Literal(record["compliment_plain"]),
            compliment_cool = sql.Literal(record["compliment_cool"]),
            compliment_funny = sql.Literal(record["compliment_funny"]),
            compliment_writer = sql.Literal(record["compliment_writer"]),
            compliment_photos = sql.Literal(record["compliment_photos"])
          )

        cursor.execute(insertStmt)

        if (commit_count > 32):
          conn.commit()
          commit_count = 0
        else:
          commit_count += 1

    conn.commit()