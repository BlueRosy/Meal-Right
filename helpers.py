# import lib
import sys
import json 
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

from flask import redirect, render_template, session
from functools import wraps


def error(error_message, code=400):
    """Render message as an apology to user."""

    return render_template("error.html", error_message=error_message), code

def success(success_message):
    """Render message as an apology to user."""

    return render_template("success.html", success_message=success_message)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
    
def getProtein(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1003:
            return nutrition.get('value')
        

def getFat(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1004:
            return nutrition.get('value')
        
def getCarbs(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1005:
            return nutrition.get('value')
        
def getCalorie(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1008:
            return nutrition.get('value')

def getSugar(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 2000:
            return nutrition.get('value')

def getFiber(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1079:
            return nutrition.get('value')
        
def getWater(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1051:
            return nutrition.get('value')
        
def getCa(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1087:
            return nutrition.get('value')
        
def getFe(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1089:
            return nutrition.get('value')
        
def getMg(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1090:
            return nutrition.get('value')
        
def getP(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1091:
            return nutrition.get('value')
        
def getK(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1092:
            return nutrition.get('value')
        
def getNa(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1093:
            return nutrition.get('value')
        
def getZn(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1095:
            return nutrition.get('value')
        
def getCu(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1098:
            return nutrition.get('value')
        
def getSe(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1103:
            return nutrition.get('value')
        
def getVitaminA(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1106:
            return nutrition.get('value')
        
def getVitaminA1(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1105:
            return nutrition.get('value')
        
def getVitaminB6(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1175:
            return nutrition.get('value')
        
def getVitaminB12(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1178:
            return nutrition.get('value')
        
def getVitaminC(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1162:
            return nutrition.get('value')
        
def getVitaminD(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1114:
            return nutrition.get('value')
        
def getVitaminE(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1109:
            return nutrition.get('value')
        
def getVitaminK(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1185:
            return nutrition.get('value')
        
def getFattedAcidSaturated(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1258:
            return nutrition.get('value')
        
def getFattyAcidMonounsaturated(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1292:
            return nutrition.get('value')
        
def getFattyAcidPolyunsaturated(foodNutritionlist):
    for nutrition in foodNutritionlist:
        if nutrition.get('nutrientId') == 1293:
            return nutrition.get('value')
 

def getSearchList(foodname):   
    """ 
    provding a foodlist based on what's search, 
    space: %20 replace 
    """
    
    foodname = " ".join(foodname.strip().split())
    foodname = foodname.replace(" ", "%20")
    
    try:
        api_key = 'tdHWwZ6dPvp170l950UUc9Yk4DypbaIh3fwlM746'
        html = urlopen("https://api.nal.usda.gov/fdc/v1/foods/search?api_key={}&query={}&dataType=Survey%20%28FNDDS%29".format(api_key, foodname))
    #     bs parsing html file, whether XML or JSON
        bs = BeautifulSoup(html, 'html.parser')
    #     json.loads only for str file
        FoodDict = json.loads(str(bs))['foods']
        return FoodDict
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None
    
    
def unit(value, unitname):
    if unitname.lower() == 'g':
        return f"{value:,.2f}g"
    if unitname.lower() == 'mg':
        return f"{value:,.2f}mg"
    if unitname.lower() == 'ml':
        return f"{value:,.2f}ml"
    if unitname.lower() == 'kcal':
        return f"{value:,.2f}KCAL"


def g(value):
    """format as g"""
    return f"{value:,.2f}g"

def kcal(value):
    """format as kcal"""
    return f"{value:,.2f}kcal"

def percentage(value):
    """Format value as %."""
    return f"{(100 * value):,.2f}%"


