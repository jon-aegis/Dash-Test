import psycopg2

try:
    connection = psycopg2.connect(user = "doadmin",
                                  password = "edcm6ngdzp8lm3b2",
                                  host = "db-postgresql-nyc1-73839-do-user-6782550-0.db.ondigitalocean.com",
                                  port = "25060",
                                  database = "defaultdb",
                                  sslmode = "require")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")