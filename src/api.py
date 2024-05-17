from app import app

from controllers.api_project import *
from controllers.api_task import *
from controllers.api_record import *
from controllers.api_project_v2 import *
from controllers.api_task_v2 import *
from controllers.api_record_v2 import *

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))
