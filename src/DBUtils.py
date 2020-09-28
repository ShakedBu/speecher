import psycopg2


def execute_query(query, is_fetch=False, is_single_row=False):
    records = None
    try:
        # Open connection to our database
        connection = psycopg2.connect(user="speecher",
                                      password="Speecher1!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="speecher")
        cursor = connection.cursor()

        # Open a cursor to perform database operations
        cursor.execute(query)

        if is_fetch:
            if is_single_row:
                records = cursor.fetchone()
            else:
                records = cursor.fetchall()

        # Make the changes to the database if insert action
        if 'INSERT' in query or 'DELETE' in query:
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # Close database connection.
        if connection:
            cursor.close()
            connection.close()

        return records


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

        # Make the changes to the database if insert action
        # if 'INSERT' in query or 'DELETE' in query:
        #     connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # Close database connection.
        if connection:
            cursor.close()
            connection.close()

        return records
