from app import app
from controllers.api_project import *
from controllers.api_task import *
from controllers.api_record import *

if __name__ == '__main__':
    app.run(debug=True)