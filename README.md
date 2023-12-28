# MEAL RIGHT

#### Video Demo: https://youtu.be/lZcHN4blUQc

#### Description: "Meal Right" is a responsive calorie consumption calculation and management web application. Users can use this app to check nutrition details of their daily consumed food, calculate everyday’s calorie consumption and record it forever in the diary as their consumption history. The user experience will be similar to adding goods into shopping carts. All the food nutrition data sources from USDA (United States Department of Agriculture) database. Welcome to play with this app and any feedback. I will very appreciate it.

#### Languages: Python, HTML, CSS, JavaScipt, Postgresql

#### Web Main functions:

1. Add food: users can search for any food keywords and get all relevent search results from USDA food database. Users can also check a certain item's nutrition details by clicking on the item name showing in the search result page.
2. Food Bag: users can edit their foodbag items' amount, remove all items, or save the foodbag snapshot into their diaries by date.
3. Cal Diary: users can check their food consumption histories and details there. Or if users want to recover a certain date's consumption history or put an item appearing in the diary back to the foodbag again, they can do so through this section.
4. current foodbag nurtition statistics summary: it will be presented on the user home page automatically. Users just need to add food in their foodbags. home page will automatically calculate the total calories, fat, carbs, and proteins of items inside this foodbag.

#### Main Design:

- Python files:
  - app.py designs all main functions showing in this flask application.
  - helps.py includes helper functions that will be used in the app.py.
- The templates folder contains 11 html files.
  - welcome.html for the welcome page design.
  - register.html for the user registration page design.
  - login.html for the user log in page design.
  - home.html for the user home page after logging in the website. It will show summarized nutrition statistics for all the food items inside the user current foodbag.
  - search.html and searchresult.html are for the first web function "Add Food". search.html presents users a search page where users can search for any food item. The search keywords will be post to "USDA DATABASE" and the API will return all relevant food results, which will be presented through the searchresult.html. Since request USDA RESTFUL API service sometimes returns results with a long waiting time or even raises a timeout error, I added a loading page and raised exceptions for all possible url request errors.
  - Inside the searchresult.html, I designed a **pop-up modal** for each food item, so that users can click on each item name to see its detailed nutrition components.
  - foodbag.html page is for the second web function "Food Bag". It is similar to a shopping cart, where users can manage food items inside their current foodbags, edit the amount, remove all items, or save the current foodbag snapshot in their calorie diaries forever. Inside this webpage, I design a pop-up modal to allow users edit the amount of food items inside their foodbags.
  - calorie_diary.html is for the third web function "Cal Diary". This will allow user to check their food consumption histories ordered by date. For each diary record, users can check details or delete record.
  - "check details" function was designed inside the history_details.html, which allows users to see food consumption details per historic diary record. It will present nutrition summary statistics for each diary record, similar to the home page statistics but in a historical version.
  - Inside the check details page, users can also choose to recover this date's consumption history into their foodbag, or put back any food item appearing in their diary history by clicking on the item name and specifying the recover amount. Recovering the whole day consumption was completed through submitting a form and recovering item function was done though a pop-up modal.
  - Finally, success.html is for presenting a successful message to hint users that their operations are successful. error.html is for presenting an error message to suggest that the operations raise some errors. Designing these two pages are for better user experiences.
- static folder contains many png, gif, CSS, and JS files
  - styles.css is for treating general styling, like clearing the page format, declaring font family, font size and color usage.
  - register.css is for register and login page unqiue styling. It aims at styling the form elements.
  - home.css is for most pages styling after logging in. It aims at styling for table elements.
  - error.css is for error page and success page unique styling designs.
  - form.css is for redesigning all pages including a form element (login.html, register.html, and searchresult.html) to be a flex element rather than a grid element. (I first designed them as a grid element but later on, I found that grid is not very supportive in the firebox browser. Thus, I changed my styling design lastly for accommodating different browsers)
  - Notice that I didn't design a separate media.css but chose to put responsive css styling for different screen sizes into different css files separately to make sure that two stylings won't be controversial.
  - loading.js is my only JavaScipt file. Most pop-up modal JS codes are directly put inside the html file.
- DataBase:
  - use a postgres database, which contains 3 tables: users, foodbag, and diaries
    - users: saved users' register information, including username and passwords (encrpyted).
    - foodbag: saved users' current foodbag items, amounts and nutrtion details.
    - diaries: saved users' historical foodbag items, amounts, and nurtrition details. (added one more column 'date', compard to foodbag)
