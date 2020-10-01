import psycopg2
from psycopg2.extras import execute_values
from flask_jwt import current_identity
from flask import abort
import os


def execute_query_safe(query, args={}, is_fetch=False, is_single_row=False):
    records = None

    # For heroku - if prod then take this
    database_host = os.environ.get('DATABASE_HOST', "127.0.0.1")
    database_port = os.environ.get('DATABASE_PORT', "5432")

    try:
        # Open connection to our database
        if current_identity.username == 'speecher':
            connection = psycopg2.connect(user="speecher",
                                          password="Speecher1!",
                                          host=database_host,
                                          port=database_port,
                                          database="speecher")
        elif current_identity.username == 'speecher2':
            connection = psycopg2.connect(user="speecher_read",
                                          password="Speecher2@",
                                          host=database_host,
                                          port=database_port,
                                          database="speecher")
        else:
            abort(401)

        connection.set_session(autocommit=True)
        cursor = connection.cursor()

        # Open a cursor to perform database operations
        cursor.execute(query, args)

        if is_fetch:
            if is_single_row:
                records = cursor.fetchone()
            else:
                records = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error from PostgreSQL", error)

    finally:
        # Close database connection.
        if connection:
            cursor.close()
            connection.close()

        return records


def execute_insert_many_safe(query, args, template):
    records = None
    try:
        # Open connection to our database
        connection = psycopg2.connect(user="speecher",
                                      password="Speecher1!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="speecher")
        connection.set_session(autocommit=True)
        cursor = connection.cursor()

        # Open a cursor to perform database operations
        execute_values(cursor, query, args, template)

    except (Exception, psycopg2.Error) as error:
        print("Error while inserting data to PostgreSQL", error)

    finally:
        # Close database connection.
        if connection:
            cursor.close()
            connection.close()

        return records
