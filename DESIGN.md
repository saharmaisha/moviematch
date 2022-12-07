# Understanding

## `app.py`
Lines 1-8 approximately consist of import statements that allow the program to access multiple libraries (`cs50`, `flask`, `flask_session`...)

Lines 11-27 are additions to configure the application, session, and the CS50 library to use the SQLite database. After these configurations our main functions come in.

### `index()`

 - Redirects to `index.html` which is the home page.

### `login()`
-   If a `GET` request is sent to the server:
	- The user is redirected to the login page, `login.html`.
-   If a `POST` request is sent to the server, which means the user clicked **Submit** on the login page:
	- Validate the form submission by checking if both the username and password fields are filled after clicking **Submit**. If not, return to an apology which is found in `helpers.py`.
	-   Sets variables that hold the corresponding information for that specific user.
	- If that username or password does not exist, it returns to an apology.
	- Sets the `session["user_id"]` to the `id` of the current user to remember who is logged in.
	- After the **Submit** button is pressed, the user is redirected to the home page.

### `logout()`
- After the user clicks **Log Out**, located in the top right corner, on the navigation bar, it clears the session and returns the user back to the login page.

### `register()`
-   If a `GET` request is sent to the server:
	- The user is redirected to the register page, `register.html`.
-   If a `POST` request is sent to the server, which means the user clicked **Submit** on the register page:
	- Validate the form submission by checking if the username, password, and password confirmation fields are filled after clicking **Submit**. If not, return an apology which is found in `helpers.py`.
	- Add the user to the database by inserting their `username` and `hash` (hashed password) into the `users` table in `moviematch.db`, our database.
	- If the username already exists, return an apology that says "username taken".
	- Sets the `session["user_id"]` to the `id` of the current user to remember who is logged in.
	- After the **Submit** button is pressed, the user is redirected to the home page.

### `form()`
-   Stores the `DISTINCT` directors from the `Director` column in the `movies` table into a variable directors to be passed into `form.html` to produce the dropdown menu for directors.
- Stores the `DISTINCT` actors from the `Star1` column in `movies` table into a variable directors to be passed into `form.html` to produce the dropdown menu for actors.
- If a `GET` request is sent to the server:
	- The user is redirected to the form page, `form.html`.
- If a `POST` request is sent to the server, which means the user clicked **Submit** on the register page:
	- Validates the form submission by checking the fields. If the user does not change any field, it returns an apology. And if the user submits at least one field, it inserts their preferences into the `form` table in `moviematch.db`.
	- If any fields are NULL, or `None`  in Python, it sets them to a default value.

### `results()`
- If a `GET` request is sent to the server:
	- A `submission` variable holds the most recent form submission. This is why we `ORDER BY id desc`, so the form submission that is last added is appears at the top. So, we can refer to it at the 0th index.
	- When people input one genre, like "Drama", for example, we must take into account movies with multiple genres such as "Comedy, Drama, Family" or "Action, Drama". So, we then check if the genre input is NULL. If it is, we can insert the NULL value directly into the SQL query that selects the movie(s) that fits the user's preferences. If it is not NULL, it concatenates itself with `%` on the left and right side of the genre, so when it is inputted into the SQL query, it takes into account text that comes before and after the word "Drama" and counts it as a Drama movie, and not it's own unique genre instead. We do this within the `sub_genre` variable.
	- The movies that match the user's preferences are stored in a variable called `mov_results`. `mov_results` checks whether the field in movies matches the respective field in movies or is NULL. 
	- The data stored in the `results` table in `moviematch.db` is deleted after to repopulate later, after the next form submission.
	- Then, for each movie that is stored in the final movie results, is inserted into the `results` table.
	- We then check if this movie already exists in the `watched` table of `moviematch.db` because we do not want previously seen results to appear again in new form submission results. So, we check the length of the results from the `SELECT` query that checks if there exists a movie that matches the movie name of each movie in `mov_results`, and if it is 1 (meaning one exists already), we remove it from the `results` table.
	- Then, we pass in the `results` variable that holds all of the finalized movie results as we're rendering the template for `results.html`. 
- If a `POST` request is sent to the server, which means the user clicked **Submit** on the results page:
	- For every result, it checks to see if a checkbox was checked. It does this by first checking if the `name` value in the HTML, which is `yes[id]` with `[id]` being the specific id that is associated with each movie. We concatenate these two together in `results.html`. So, in order to use `request.form.get()`, we created a seperate variable called yes_var that typecasts the movie id into a string, so we can concatenate it with "yes" within the function `request.form.get()` to retrieve the value `"on"` or `"off"` depending on whether the user checked or not. 
	- If a checkbox is clicked, it then checks if the movie already exists in the `watched` table. If it does exist, it deletes it from `watched`, and inserts it as a new value in `watched`. We do this so the users see that their most recent request was completed, by seeing their new "watched" movie at the bottom of the list.
	- A `unwatched` variable is created to store the results if the checkbox was not clicked. Then, it checks whether this movie already exists in the `watched` table. If it does, we remove it from the `to_watch` table to avoid the same movie being shown inaccurately in two different tables.
	- The `results` table is then cleared to be repopulated later. 
	- A `watched` variable that holds the finally updated list of watched movies is then passed in to render the template of `watched.html`.

### `watched()`
- It renders the template for `watched.html` using the variable `watched` which stores all of the values in the `watched` table. This variable is passed in to `watched.html` so we can access it in the HTML using Jinja later.

### `unwatched()`
- It renders the template for `unwatched.html` using the variable `unwatched` which stores all of the values in the `to_watch` table. This variable is passed in to `unwatched.html` so we can access it in the HTML using Jinja later.

### `about()`
- If a `GET` request is sent to the server:
	- an `info` variable is created that stores the info from the `movies` table that matches the name of the movie that the user has clicked on. It gets this value by using `request.args.get('movie')` which takes the value of the movie variable that has a value stored in the URL of the `about.html`. For example, if the URL is: `http://127.0.0.1:5000/about?movie=The%20Intouchables`, the `request.args.get('movie')` will return `The Intouchables`. 
	- It renders the template for `about.html` using the variable `info` . This variable is passed in to `about.html` so we can access it in the HTML using Jinja later.
- If a `POST` request is sent to the server, which means the user clicked on a movie name:
	- An `unwatched` variable is created that stores all of the rows in the `to_watch` table.
	- Then, using the same tactic we used for the checkbox in the results page, it checks to see if a checkbox is clicked. If it was, it removes it from `to_watch` and inserts it into `watched`. This is done because users should have an easy way of checking movies off of their unwatched list and adding them into their watched list.
	- We delete the information stored in the `results` table to repopulate later with new form submission results.
	- Finally, a `watched` variable is created that stores the updated list of watched movies that is passed into `watched.html` using `render_template()`.

## `helpers.py`

### `apology()`
- Renders message as an apology to the user. It uses a cat meme and returns an error message with the code 400.

### `login_required()`
- It checks to see if the `session["user_id"]` value is NULL, or `None` in Python, and if it is, it redirects to the login page.

## `moviematch.db`

### `movies`
- "Poster_Link" TEXT
- "Series_Title" TEXT
- "Released_Year" TEXT
-  "Certificate" TEXT
- "Runtime" TEXT
- "Genre" TEXT
- "IMDB_Rating" TEXT
- "Overview" TEXT
- "Meta_score" TEXT
- "Director" TEXT
- "Star1" TEXT
- "Star2" TEXT
- "Star3" TEXT
- "Star4" TEXT
- "No_of_Votes" TEXT
- "Gross" TEXT

### `users`
- id INTEGER PRIMARY KEY
- username TEXT NOT NULL
- hash TEXT NOT NULL

### `results`
- id INTEGER PRIMARY KEY
- movie_name TEXT NOT NULL
- runtime TEXT NOT NULL
- genre TEXT NOT NULL
- rating NUMERIC NOT NULL
- released_year INTEGER NOT NULL
- user_id INTEGER NOT NULL
- director TEXT NOT NULL
- watched TEXT

### `watched`
- id INTEGER PRIMARY KEY
- movie_name TEXT NOT NULL
- runtime TEXT NOT NULL
- genre TEXT NOT NULL
- rating NUMERIC NOT NULL
- released_year INTEGER NOT NULL
- user_id INTEGER NOT NULL
- director TEXT NOT NULL

### `to_watch`
- id INTEGER PRIMARY KEY
- movie_name TEXT NOT NULL
- runtime TEXT NOT NULL
- genre TEXT NOT NULL
- rating NUMERIC NOT NULL
- released_year INTEGER NOT NULL
- user_id INTEGER NOT NULL
- director TEXT NOT NULL

### `form`
- id INTEGER PRIMARY KEY
- director TEXT
- genre TEXT
- actor TEXT
- minyear INTEGER
- maxyear INTEGER
- user_id INTEGER
- minrating NUMERIC
- maxrating NUMERIC

## templates/

In the **Template** folder, we hold the various different HTML pages needed for our website

### `layout.html`

The layout page has all the features that are consistent throughout each of our HTML files:

  

- Navigation bar
- Links to CSS, Bootstrap (etc.)

  

### `index.html`

This is our home page. It includes the welcome message and a button that is linked to `form.html`.

  

### `login.html`

This is the page where the user logs in. It includes fields for the `username` and `password` and a **Submit** button.

  

### `register.html`

This is the page where the user registers if they don't already have an account. It includes fields for `username`, `password`, and `password confirmation`.

  

### `form.html`

This is the page that contains the contents of our form.

  

- `Favorite genre`:

Lists types of genres that will appear in a dropdown menu

- `Favorite director` & `Favorite actor`:

Lists different directors and actors by using a for loop that will look through the directors column of the menu table when it is passed later on. Designed to show up as a dropdown menu.

- `Minimum year`, `Minimum rating` , `Maximum year`, & `Maximum rating`:

Create a slider to choose your preference for these categories

- In a script tag, this addition of Javascript is used to produce a number based on the value the slider has landed on

  

### `results.html`

This page is for your movie results. After you've filled out `form.html` you will be taken to this page. A table has been created that will display your movie results. Using Jinja `movie name`, `director`, `runtime`, `genre`, `rating`, and `released year` are displayed when all of these values are passed to `results.html` . It includes the addition of a checkbox that can be selected when the user has watched a movie. After the user has selected everything they have watched they are able to `Submit`.

  

### `watched.html`

This page is for the movies the user has already watched. A table is created that only includes the movies the user has already watched. After the user selects the movies they have watched on the `results.html` page, the movies are then moved to the `watched` SQL table which are then shown on this page. Using Jinja `movie name`, `director`, `runtime`, `genre`, `rating`, and `released year` are displayed using a for loop. All of these values are passed to `watched.html` in `app.py` which is how the information is accessed.

Using an anchor tag the movie name’s href is set to `/about?movie= {{watch.movie_name}}` which, using Jinja, sets the URL equal to the movie name (after it's passed) so that you can access it later on. Then when the link is pressed and you're sent to `about.html` the movie name is embedded into the URL so that you can access the movie name after the link is pressed. Using Jinja in `about.html`, the program uses the movie name in the URL and grabs the information for that specific movie.


### `unwatched.html`

This page is for the movies the user has not watched. A table is created that only includes the movies the user has not watched. After the user selects the movies they have not watched on the `results.html` or `watched.html`page, the movies are then moved to the `unwatched` SQL table which are then shown on this page. Using Jinja `movie name`, `director`, `runtime`, `genre`, `rating`, and `released year` are displayed using a for loop. All of these values are passed to `unwatched.html` in `app.py` which is how the information is accessed.

### `apology.html`

This page links an image that is used for error messages. You can choose what text is displayed on the image but that is specified in the `app.py` when apology is called.

### `about.html`

This page displays a description of the movie with a quick summary, stars list, and the movie poster. Using Jinja, the movie name is passed to `about.html` and using a for loop the specified information is displayed.

## static/

`styles.css`

- `nav .navbar brand`

Sets the font size in the navigation bar

- `.slidecontainer` and `.navbar-light`

Set slider container to have a width of 100% and the color to be white

- `.slider`, .`slider.hover`, `.slider::webkit`, `.slider:: -moz`

Designs slider to look be a certain size and color

- `.h1`

Sets all text in an h1 tag to use a specific font

- `.body`

Sets page background color, text color, font size, and font type

- `a:link`

Sets link color

- `a:visited`

Sets a color for links that have been visited

- `a:hover`

Sets a color that is activated when the cursor is hovering over a link

- `a:active`

Sets color when link is clicked

- `table, th, td`

Sets border color for all tables and table attributes

  

`favicon.ico`

  

- Stores the favicon