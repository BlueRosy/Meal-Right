import psycopg2 

# connect to the db
connect = psycopg2.connect(
    host = "ep-withered-lake-46572808-pooler.us-east-1.postgres.vercel-storage.com",
    database = "verceldb",
    user = "default",
    password = "xOYnls4XI2ub",
    port="5432"
    
)

# cursor
cur = connect.cursor()

# delete db tables if exists
# create statement is case sensitive single quote for string, double quote for column and table
cur.execute("DROP TABLE IF EXISTS users;")
cur.execute("DROP TABLE IF EXISTS foodbag;")
cur.execute("DROP TABLE IF EXISTS diaries;")
connect.commit()

# execute create table SQL query
cur.execute(
    'CREATE TABLE users ("id" serial NOT NULL, "name" VARCHAR(255) NOT NULL,"hash" VARCHAR(255) NOT NULL, PRIMARY KEY("id"));'
    )
connect.commit()

cur.execute(
    'CREATE TABLE foodbag ("id" serial NOT NULL, "user_id" VARCHAR(255) NOT NULL, "food" VARCHAR(255) NOT NULL, "fdcId" VARCHAR(255) NOT NULL, "protein_100g" NUMERIC(8,2) NOT NULL, "fat_100g" NUMERIC(8,2) NOT NULL, "carbs_100g" NUMERIC(8,2) NOT NULL, "calorie_100g" NUMERIC(8,2) NOT NULL, "servingSize" INTEGER NOT NULL, PRIMARY KEY("id"));'
    )
connect.commit()

cur.execute(
    'CREATE TABLE diaries ("id" serial NOT NULL, "user_id" VARCHAR(255) NOT NULL, "date" DATE NOT NULL, "food" VARCHAR(255) NOT NULL, "fdcId" VARCHAR(255) NOT NULL, "protein_100g" NUMERIC(8,2) NOT NULL, "fat_100g" NUMERIC(8,2) NOT NULL, "carbs_100g" NUMERIC(8,2) NOT NULL, "calorie_100g" NUMERIC(8,2) NOT NULL, "servingSize" INTEGER NOT NULL, PRIMARY KEY("id"));'
            )
connect.commit()


# close the cursor
cur.close()

# close the connection
connect.close()