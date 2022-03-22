# 'website' is a python package because __init__.py is located in the folder. Thus, turning 'website' folder into a package
from distutils.log import debug
from pickle import TRUE
from website import create_app

app = create_app()

# Flask web server is executed ONLY if THIS main.py is executed
if __name__ == '__main__':
    # starts up the web app and debug=TRUE will refresh the web app everytime we make changes and run it.
    # Note: debug=TRUE needs to be removed in work setting. 
    app.run(debug=TRUE)
    