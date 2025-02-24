1. `python --version`
2. in main dir - create `app.py` and `templates` folder
3. in template - create a `index.html`
4. create a virtual enviroment `python -m venv venv`
5. activate venv - `venv/Scripts/Activate`
6. install following libraries - `pip install Flask tabula-py pandas`
7. run the app.py - `python app.py`

the steps i have compleated 
- Set up your project structure.
- Created a basic Flask application (app.py).
- Designed a simple user interface (index.html).
- Created and activated a virtual environment.
- Installed all necessary Python libraries within the virtual environment.
- Started the Flask application without errors.
- Accessed the UI in your web browser.

8. install java - Install Java Development Kit (JDK) - search on Google for "download java jdk"  or go directly to Oracle's website. Look for the "Java SE Downloads" or "JDK Downloads" section.

9. put that path inside the enviroment variable in your system variable section of the window setting.


10. **Recreating the venv**
- deactivate
- Remove-Item -Path venv -Recurse -Force
- python -m venv venv
- pip install -r requirements.txt
- 