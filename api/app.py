import os
import sys

from cs50 import SQL
import psycopg2
import psycopg2.extras
import datetime
from datetime import date, timedelta
import pytz
from flask import Flask, flash, redirect, render_template, request, session
# from flask_sqlalchemy import SQLAlchemy
from urllib.error import URLError, HTTPError
from requests.exceptions import RequestException
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import error, success, login_required, getSearchList, unit, g, kcal, percentage, getProtein, getFat, getCarbs, getCalorie, getSugar, getFiber, getWater, getCa, getFe, getMg, getP, getK, getNa, getZn, getCu, getSe, getVitaminA, getVitaminA1, getVitaminB6, getVitaminB12, getVitaminC, getVitaminD, getVitaminE, getVitaminK, getFattedAcidSaturated, getFattyAcidMonounsaturated, getFattyAcidPolyunsaturated

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["g"] = g
app.jinja_env.filters["kcal"] = kcal
app.jinja_env.filters["percentage"] = percentage
app.jinja_env.filters["getProtein"] = getProtein
app.jinja_env.filters["getFat"] = getFat
app.jinja_env.filters["getCarbs"] = getCarbs
app.jinja_env.filters["getCalorie"] = getCalorie
app.jinja_env.filters["getSugar"] = getSugar
app.jinja_env.filters["getFiber"] = getFiber
app.jinja_env.filters["getWater"] = getWater
app.jinja_env.filters["getCa"] = getCa
app.jinja_env.filters["getFe"] = getFe
app.jinja_env.filters["getMg"] = getMg
app.jinja_env.filters["getP"] = getP
app.jinja_env.filters["getK"] = getK
app.jinja_env.filters["getNa"] = getNa
app.jinja_env.filters["getZn"] = getZn
app.jinja_env.filters["getCu"] = getCu
app.jinja_env.filters["getSe"] = getSe
app.jinja_env.filters["getVitaminA"] = getVitaminA
app.jinja_env.filters["getVitaminA1"] = getVitaminA1
app.jinja_env.filters["getVitaminB6"] = getVitaminB6
app.jinja_env.filters["getVitaminB12"] = getVitaminB12
app.jinja_env.filters["getVitaminC"] = getVitaminC
app.jinja_env.filters["getVitaminD"] = getVitaminD
app.jinja_env.filters["getVitaminE"] = getVitaminE
app.jinja_env.filters["getVitaminK"] = getVitaminK
app.jinja_env.filters["getFattedAcidSaturated"] = getFattedAcidSaturated
app.jinja_env.filters["getFattyAcidMonounsaturated"] = getFattyAcidMonounsaturated
app.jinja_env.filters["getFattyAcidPolyunsaturated"] = getFattyAcidPolyunsaturated


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SECRET_KEY"] = 'mySecret'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://default:xOYnls4XI2ub@ep-withered-lake-46572808-pooler.us-east-1.postgres.vercel-storage.com/verceldb"
# app.config["SESSION_TYPE"] = "sqlalchemy"
# db = SQLAlchemy(app)
# app.config["SESSION_SQLALCHEMY"] = db

# db.create_all()

# Session(app)

# Configure postgres database
# connect to the db
connect = psycopg2.connect(
    host = "ep-withered-lake-46572808-pooler.us-east-1.postgres.vercel-storage.com",
    database = "verceldb",
    user = "default",
    password = "xOYnls4XI2ub",
    port="5432",
    keepalives=1,
    keepalives_idle=30,
    keepalives_interval=10,
    keepalives_count=5
)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def welcome():
    if not session.get("user_id"):
        return render_template("welcome.html")
    return redirect("/home")

@app.route("/register", methods=["GET", "POST"])
def register():
    """REGISTER USER"""
    
    if request.method == "POST":
        
        # ensure username is submitted
        if not request.form.get("username"):
            return error("Dear, username seems to be missed !", 400)
        
        # ensure password is sumbitted
        if not request.form.get("password") or not request.form.get("confirmation"):
            return error("Dear, password seems to be missed!", 400)
        
        # ensure passwords are matched
        if request.form.get("password") != request.form.get("confirmation"):
            return error("Dear, passwords seem unmatched!", 400)
        
        # ensure username doesn't exist in the food.db
        cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        name = request.form.get("username")
        p1 = request.form.get("password")
        p2 = request.form.get("confirmation")
        cursor.execute('SELECT COUNT(*) as "counts" FROM users WHERE "name" = %s', (name,))
        rows = cursor.fetchall()
        cursor.close()
        if rows[0]["counts"] > 0:
            return error("Dear, username has been used!", 400)
        
        # store the valid username and password into db
        cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute('INSERT INTO users (name, hash) VALUES (%s, %s);', (name, generate_password_hash(p1)))
        connect.commit()
        
        
        # store user in the session
        cursor.execute("SELECT id FROM users WHERE name = %s;", (name,))
        row = cursor.fetchall()
        session["user_id"] = row[0]["id"]
        
        cursor.close()
        
        return redirect("/home")
        
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """ 
        USER LOG IN
    """
    
    if request.method == "POST":
        
        # check if inputs username and password 
        name = request.form.get("username")
        p = request.form.get("password")
        
        if not name:
            return error("Dear, we don't receive your username !", 403)
        if not p:
            return error("Dear, we don't receive your password !", 403)
        
        # check if username exists in db
        cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
        row = cursor.fetchall()
        cursor.close()
        if len(row) == 0:
            return error("Dear, you seem unregistered yet !", 403)
        
        # check if username and password are matched with db
        if not check_password_hash(row[0]["hash"], p):
            return error("Dear, you seem to enter a wrong password!", 403)
        
        session["user_id"] = row[0]["id"]
        return redirect("/home")
        
    return render_template("login.html")

@app.route("/home")
@login_required
def home():
    """report user's food bag nutrition facts"""
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    
    user_id = session["user_id"]
    
    # get total summary for current food bag
    ## note: calorie = calc per serving * servings, fat, carb and protein too
    cursor.execute(
        'SELECT COALESCE(SUM("calorie_100g" * "servingSize" / 100), 0) as calories, COALESCE(SUM("fat_100g" * "servingSize" / 100), 0) as fat, COALESCE(SUM("carbs_100g" * "servingSize" / 100), 0) as carbs, COALESCE(SUM("protein_100g" * "servingSize" / 100), 0) as protein FROM foodbag WHERE user_id = %s', (str(user_id),))
    
    res = cursor.fetchall()
    
    # get information about single items inside the food bag
    cursor.execute('SELECT food, COALESCE(SUM("servingSize"), 0) as servings, COALESCE(SUM("calorie_100g" * "servingSize" / 100), 0) as calories FROM foodbag WHERE user_id = %s GROUP BY(food) ORDER BY 3 DESC;', (str(user_id), ))
    
    foodbag = cursor.fetchall()
    cursor.close()
    
    return render_template("home.html", 
                           calories=res[0]["calories"],
                           fat=res[0]["fat"],
                           carbs=res[0]["carbs"],
                           protein=res[0]["protein"],
                           foodbag=foodbag)
    
    
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    
    """ A main function for our web app: 
        allowing user search for food nutrition
    """
    
    if request.method == "POST":
        
        # check if input is empty
        searchkey = request.form.get("foodname")
        # print(searchkey)
        if not searchkey:
            return error("Dear, you seem to input nothing !", 403)
        
        
        # check if the item in the USDA searchlist
        try:
            res = getSearchList(searchkey)
        except (URLError, HTTPError, RequestException):
            return error("Dear, network seems to be busy. Please try searching later !", 403)
        
        if not res:
            return error("Dear, nothing has been found ! we will try to add more data soon !", 403)
        
        # get valid information about food description, nutrition info
        return render_template("searchresult.html", res=res, searchkey=searchkey)
        
    return render_template("search.html")


@app.route("/addbagsuccess", methods=["POST"])
@login_required
def add_item():
    
    """get user_id, cart item, servings, other basic info: protein, fat, carbs, calories into db table foodbags"""
    
    
    fdcId = request.form.get("fdcId")
    item = request.form.get("item")
    servingSizeUnit = request.form.get("servingSizeUnit")
    protein = request.form.get("protein")
    fat = request.form.get("fat")
    carbs = request.form.get("carbs")
    calorie = request.form.get("calorie")
    
    # check if data not missing
    if not fdcId or not item or not servingSizeUnit or not protein or not fat or not carbs or not calorie:
        return error("Dear, essential data inputs seem missed out ! we can't put this item in your foodbag", 403)
    
    
    # check if number is valid
    try:
        protein = float(protein)
        fat = float(fat)
        carbs = float(carbs)
        calorie = float(calorie)
        servingSizeUnit = int(servingSizeUnit)
    except ValueError:
        return error("Dear, data input is invalid !", 403)
    else:
        if protein < 0 or fat < 0 or carbs < 0 or calorie < 0 or servingSizeUnit <= 0:
            return error("Dear, data input is not positive !", 403)
    
    # check if fdcId has already in the foodbag
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute(
        'SELECT COALESCE(COUNT(*), 0) as counts FROM foodbag WHERE user_id = %s and "fdcId" = %s', (str(session["user_id"]), fdcId))
    
    records = cursor.fetchall()
    
    if records[0]["counts"] > 0:
        cursor.execute('UPDATE foodbag SET "servingSize" = "servingSize" + %s WHERE user_id = %s and "fdcId" = %s;', (servingSizeUnit, str(session["user_id"]), fdcId))
        
        connect.commit()
        
    # insert all info into current food bags
    else: 
        cursor.execute('INSERT INTO foodbag (user_id, "fdcId", food, "servingSize", "protein_100g", "fat_100g", "carbs_100g", "calorie_100g") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (str(session["user_id"]), fdcId, item, servingSizeUnit, protein, fat, carbs, calorie))
        
        connect.commit()
    
    cursor.close()
    
    return success("food has been successfully added into your bag !")


@app.route("/foodbag", methods=["POST", "GET"])
@login_required
def foodbag():
    """ CHECK USER's foodbag items and add or remove some amount """
    
    if request.method == "POST":
        
        # check user wants to add or remove some amount 
        update = request.form.get("new_serving_size")
        fdcId = request.form.get("fdcId")
        remove = request.form.get("remove_all")
        
        # check if user request to remove all
        if remove:
            try:
                remove = int(remove)
            except ValueError:
                return error("dear, it seems an invalid operation !", 403)
            else:
                if remove == 1:
                    # remove all user's foodbag item
                    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                    cursor.execute("DELETE FROM foodbag WHERE user_id = %s;", (str(session["user_id"]), ))
                    connect.commit()
                    cursor.close()
                    return success("your foodbag is now empty !")
                else:
                    return error("dear, it seems an invalid operation !", 403) 
        
        if not fdcId:
            return error("dear, we don't know which item you want to remove or add !", 403)
        
        if not update:
            return error("dear, we don't know which amount you want to update !", 403)
        
        # verify if the number is positive integer
        try:
            update = int(update)
        except ValueError:
            return error("dear, you inputed an invalid amount !", 403)
        else:
            if update < 0:
                return error("dear, you inputed a nagative amount !", 403)
        
        # verify if the fdcId in the foodbag
        cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute('SELECT COALESCE(count(*), 0) as counts FROM foodbag WHERE user_id = %s and "fdcId" = %s', (str(session["user_id"]), fdcId ))
        
        records = cursor.fetchall()
        cursor.close()
        
        if records[0]["counts"] == 0:
            return error("dear, your foodbag doesn't contain this item !", 403)
        
        # delete the whole item from database
        if update == 0:
            cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            cursor.execute('DELETE FROM foodbag WHERE user_id = %s and "fdcId" = %s;', (str(session["user_id"]), fdcId))
            connect.commit()
            cursor.close()
            return success("item has been removed from your foodbag !")
        # update the item amount in the database
        else:
            cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            cursor.execute('UPDATE foodbag SET "servingSize" = %s WHERE user_id = %s and "fdcId" = %s;', (update, str(session["user_id"]), fdcId))
            connect.commit()
            cursor.close()
            return success("item amount has been updated in your foodbag !")
    
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)              
    cursor.execute('SELECT "fdcId", food, COALESCE(SUM("servingSize"), 0) as servings FROM foodbag WHERE user_id = %s GROUP BY "fdcId", food ORDER BY food;', (str(session["user_id"]), ))
    
    foodbag = cursor.fetchall()
    cursor.close()
    
    return render_template("foodbag.html", foodbag=foodbag)
                

@app.route("/calorie_diary", methods=["POST", "GET"])
@login_required
def diary():
    """ SHOW USER CALORIE HISTORY BY DATE"""
    
    if request.method == "POST":
        diary_date = request.form.get("record_date")
        
        # check if date is empty
        if not diary_date:
            return error("dear! you haven't specify which date to save your foodbag snapshot !", 403)
        
        
        # validate a user input of date 'YYYY-mm-dd'. 
        try:
            date.fromisoformat(diary_date)
        except ValueError:
            return error("dear! you inputed an invalid date !", 403)
        
        # validate if certain date diary has already saved.
        cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT COALESCE(COUNT(*), 0) as counts FROM diaries WHERE user_id = %s AND date = %s", (str(session["user_id"]), diary_date))
        
        records = cursor.fetchall()
        cursor.close()
        
        if records[0]["counts"] > 0:
            return error("dear! you already have this date's diary ! please delete it first !", 403)
        
        # put foodbag data in diary catelog
        cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute('INSERT INTO diaries (user_id, date, food, "fdcId", "protein_100g", "fat_100g", "carbs_100g", "calorie_100g", "servingSize") SELECT user_id, %s, food, "fdcId", "protein_100g", "fat_100g", "carbs_100g", "calorie_100g", "servingSize" FROM foodbag WHERE user_id = %s', (diary_date, str(session["user_id"])))
        
        connect.commit()
        cursor.close()
        
        return success("you have successfully recorded your foodbag snapshot in your cal diary !")
    
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute('SELECT date, COALESCE(SUM("calorie_100g" * "servingSize" / 100), 0) as calories, COALESCE(SUM("fat_100g" * "servingSize" / 100), 0) as fat, COALESCE(SUM("carbs_100g" * "servingSize" / 100), 0) as carbs, COALESCE(SUM("protein_100g" * "servingSize" / 100), 0) as protein FROM diaries WHERE user_id = %s GROUP BY date ORDER BY date DESC;', (str(session["user_id"]), ))
    
    histories = cursor.fetchall() 
    cursor.close()
    return render_template('calorie_diary.html', histories=histories)

@app.route("/delete_diary", methods=["POST"])      
@login_required
def delete_diary():
    """DELETE SPECIFIC DATE FODD RECORD"""
    
    delete_date = request.form.get('deleteDate')
    
    # check the value is null
    if not delete_date:
        return error("dear, you don't specify a specific diary date to delete !", 403)
    
    # check if the date is valid
    try:
        date.fromisoformat(delete_date)
    except ValueError:
        return error("dear! you specified an invalid date !", 403)
    
    # check if the date information appeared in user diary
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT COALESCE(COUNT(*), 0) as counts FROM diaries WHERE user_id = %s AND date = %s", (str(session["user_id"]), delete_date))
    
    records = cursor.fetchall()
    cursor.close()
    
    if records[0]["counts"] == 0:
        return error("dear! you don't have this date's diary !", 403)
    
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute("DELETE FROM diaries WHERE user_id = %s AND date = %s", (str(session["user_id"]), delete_date))
    
    connect.commit()
    cursor.close()
    
    return success("diary record for this specific date has been deleted !")

@app.route("/historyDetails", methods=["POST"])
@login_required
def historyDetails():
    """ SHOW USER SPECIFIC DATE FOOD CONSUMPTION HISTORIES OR FOODBAG SNAPSHOT"""
    
    checkDate = request.form.get('checkDate')
    
    # check if checkDate is NULL
    if not checkDate:
        return error("dear! we don't know at which date you want to see your food consumption details!", 403)
    
    # check if checkDate is valid
    try:
        date.fromisoformat(checkDate)
    except ValueError:
        return error("dear! you specified an invalid date !", 403)
    
    # check if the date information appeared in user diary
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT COALESCE(COUNT(*), 0) as counts FROM diaries WHERE user_id = %s AND date = %s", (str(session["user_id"]), checkDate))
    
    records = cursor.fetchall()
    cursor.close()
    
    if records[0]["counts"] == 0:
        return error("dear! you don't have this date's food consumption details !", 403)
    
    # show results on the webpage
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute('SELECT COALESCE(SUM("calorie_100g" * "servingSize" / 100), 0) as calories, COALESCE(SUM("fat_100g" * "servingSize" / 100), 0) as fat, COALESCE(SUM("carbs_100g" * "servingSize" / 100), 0) as carbs, COALESCE(SUM("protein_100g" * "servingSize" / 100), 0) as protein FROM diaries WHERE user_id = %s AND date = %s', (str(session["user_id"]), checkDate))
    
    res = cursor.fetchall()
    
    # get information about single items inside the food bag
    cursor.execute('SELECT "fdcId", food, COALESCE(SUM("servingSize"), 0) as servings, COALESCE(SUM("calorie_100g" * "servingSize" / 100), 0) as calories FROM diaries WHERE user_id = %s AND date = %s GROUP BY "fdcId", food ORDER BY 4 DESC;', (str(session["user_id"]), checkDate))
    
    foodbag = cursor.fetchall()
    
    cursor.close()
    return render_template("history_details.html", 
                           checkDate=checkDate,
                           calories=res[0]["calories"],
                           fat=res[0]["fat"],
                           carbs=res[0]["carbs"],
                           protein=res[0]["protein"],
                           foodbag=foodbag)
    

@app.route("/history_recover", methods=["POST"]) 
@login_required
def historyRecover():
    """recover all historical records from a certain date to foodbag"""
    
    recover_date = request.form.get("recover_date")
    
    # check if recover date is NULL
    if not recover_date:
        return error("dear! we don't know at which date you want to recover your food consumption!", 403)
    
    # check if recover_date is valid
    try:
        date.fromisoformat(recover_date)
    except ValueError:
        return error("dear! you specified an invalid date !", 403)
    
    # check if the date information appeared in user diary
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT COALESCE(COUNT(*), 0) as counts FROM diaries WHERE user_id = %s AND date = %s", (str(session["user_id"]), recover_date))
    
    records = cursor.fetchall()
    cursor.close()
    
    if records[0]["counts"] == 0:
        return error("dear! you don't record your consumption at this date !", 403)
    
    # recover results into foodbag, note: sqlite3 syntax 
    # still note: if item has already in the foodbag, must update rather than insert
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute('DELETE FROM foodbag WHERE user_id = %s AND "fdcId" IN (SELECT DISTINCT("fdcId") FROM diaries WHERE user_id = %s AND date = %s);', (str(session["user_id"]), str(session["user_id"]), recover_date))
    
    connect.commit()

    cursor.execute('INSERT INTO foodbag (user_id, food, "fdcId", "protein_100g", "fat_100g", "carbs_100g", "calorie_100g", "servingSize") SELECT user_id, food, "fdcId", "protein_100g", "fat_100g", "carbs_100g", "calorie_100g", "servingSize" FROM diaries WHERE user_id = %s AND date = %s;', (str(session["user_id"]), recover_date))
    
    connect.commit()
    cursor.close()
    
    return success("historical consumption has been recovered in your foodbag !")


@app.route("/item-recover", methods=["POST"])
@login_required
def itemRecover():
    fdcId = request.form.get("recover_fdcId")
    amount = request.form.get("recover_amount")
    
    
    # test whether item or amount is none
    if not fdcId:
        return error("dear! we don't know which item you want to recover.", 403)
    
    if not amount:
        return error("dear! we don't know how many you want to recover.", 403)
    
    # test datatype
    try:
        amount = int(amount)
    except ValueError:
        return error("dear! you need to specify a positive amount to recover.", 403)
    else:
        if amount <= 0:
            return error("dear! you need to specify a positive amount to recover.", 403)
    
    # test if the item contain in the diary 
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute('SELECT COALESCE(COUNT(*), 0) as counts FROM diaries WHERE user_id = %s AND "fdcId" = %s;', (str(session['user_id']), fdcId))
    
    records = cursor.fetchall()
    cursor.close()
    if records[0]['counts'] <= 0:
        return error("dear! your diary doesn't contain this item!", 403)
    
    # test if item already contain in the foodbag
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute('SELECT COALESCE(COUNT(*), 0) as counts FROM foodbag WHERE user_id = %s AND "fdcId" = %s;', (str(session["user_id"]), fdcId))
    
    records = cursor.fetchall()
    cursor.close()
    if records[0]['counts'] > 0:
        return error("dear! your foodbag already contains this item. please directly edit it there", 403)
    
    # recover item and amount to foodbag
    cursor = connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute('INSERT INTO foodbag (user_id, food, "fdcId", "protein_100g", "fat_100g", "carbs_100g", "calorie_100g", "servingSize") SELECT user_id, food, "fdcId", "protein_100g", "fat_100g", "carbs_100g", "calorie_100g", %s FROM diaries WHERE user_id = %s AND "fdcId" = %s LIMIT 1;', (amount, str(session["user_id"]), fdcId))
    
    connect.commit()
    cursor.close()
    
    return success("item has been added into your foodbag !")
    
               
@app.route("/logout")
def logout():
    """Log User Out"""

    session.clear()
    
    return redirect("/")

