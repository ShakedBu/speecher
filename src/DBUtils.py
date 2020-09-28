import psycopg2
from psycopg2.extras import execute_values


def execute_query_safe(query, args={}, is_fetch=False, is_single_row=False):
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
