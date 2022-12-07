# Welcome to 🎬 MovieMatch!

## Video Demonstration

https://youtu.be/Bs7M1c6fu_s

## Getting Started
Download the latest version of [Visual Studio Code](https://code.visualstudio.com/download).

In the terminal of Visual Studio Code (VSCode), clone the Github repository by inputting this into your preferred directory:

    git clone https://github.com/saharmaisha/moviematch.git

It may prompt you to allow Github to access VSCode, to which you will provide your password for access. 

Once it redirects you to your terminal, you may see something like this:

    Cloning into 'moviematch'...
    remote: Enumerating objects: 244, done.
    remote: Counting objects: 100% (31/31), done.
    remote: Compressing objects: 100% (28/28), done.
    remote: Total 244 (delta 4), reused 10 (delta 3), pack-reused 213
    Receiving objects: 100% (244/244), 749.94 KiB | 2.17 MiB/s, done.
    Resolving deltas: 100% (94/94), done.

 After this, execute this command:

    cd moviematch

Now, you have successfully entered the repository!

Because you are no longer in the CS50 workspace, where many libraries are pre-installed for you, you must install them into your own computer (You'll need them in order for the code to run properly. And it's good to have for your own projects as well 😉). 

Follow this guide to install [Python](https://docs.python-guide.org/starting/install3/osx/). And make sure to have [Pip](https://pip.pypa.io/en/stable/installation/) installed as well. You may already have these! To check, execute these commands in your terminal:

    python3 --version
    python3 -m pip --version

Now, execute these commands:

    pip3 install cs50
    pip3 install flask
    pip3 install flask_session
    pip3 install tempfile
    pip3 install helpers

## Running

Start Flask’s built-in web server (within `moviematch/`):

    flask run
   
   You may see something like:
   
    INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on http://127.0.0.1:5000
    * INFO: Press CTRL+C to quit
  
Enter the URL: `http://127.0.0.1:5000` or what your terminal outputs into your search bar and hit enter. You have successfully loaded 🎬 MovieMatch!

## Navigation

### Register
Time for the fun part... using our website! Once you enter, you will be prompted to login. If you do not have an account, which you probably don't  if you're using our website for the first time, click **Register** located in the top right corner, on the navigation bar. Create a username and password and then submit. You will automatically be logged in. **However, for future uses, you will be prompted to log in every time.**

### Log In

Click **Login** located in the top right corner, on the navigation bar, and enter your username and password. Then hit submit! 

### Home
After logging in you’ll be taken to the home page where you’ll then be prompted to click a button to begin filling out the movie preferences form. You can also always access the form by clicking **Form**, located in the top right corner, on the navigation bar.

### Form
After clicking the button you’ll be taken to the form page where you will have to fill out a few fields about your movie preferences

 - **You don’t have to submit something for every field.** If you wanted to just see what action movies, for example, are available to watch, you can choose "Action" in the genre category and submit—leaving everything else untouched. After submitting, you will be shown all of the action movies in our database!
 - **Some movie preference choices may not produce any results.** For example, if you chose an actor and a director that have not worked together you will not get any movie results. Luckily, you can just submit the form again with different preferences!

### Results
Once you’ve submitted the form you’ll be taken to page with movie results based on your preferences. You can browse the list for as long as you please.
On the **Results** page you have an option to check whether or not you’ve watched a movie under the column that says **Already Watched?** Check off the boxes that correspond to the movies that you have watched, and click Submit.

### Watched Movies
After clicking Submit on the **Results** page, you’ll be taken to the **Watched** page where you can see all the movies you’ve watched. If you want to see what movies you haven’t watched, they will be added to your "Unwatched" list which you can view by clicking **Unwatched**, located in the top right corner, on the navigation bar.

### Unwatched Movies
By clicking on **Unwatched**, located in the top right corner, on the navigation bar, you can view a list of movies that you have yet to watch! If it's been a while since you've viewed your unwatched movies list, and spot a movie that you've watched recently, you can check that movie off under the column that says **Already Watched?** and hit Submit. It will then remove the movie from your Unwatched list and add it to your Watched list.

### About
If you want to know more about a movie, you can click on the movie name in your **Results**, **Watched**, and **Unwatched** pages. This will lead you to the **About** page that provides a brief description and a poster of the movie.


