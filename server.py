from application import app # import app from application.py
from application.controllers import routes

if __name__ == '__main__': # if this file is run directly, run the app
    app.run(debug=True)  # run the app in debug mode