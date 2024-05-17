# demo-api-with-flask

Atempt to build an REST API using **Flask 3+ and Python 3.12+**

## Prompt given to Gemini

```text
Hi, what do I need to know to build a python rest api and what are the steps to do it?
```

## Steps to Build a Python REST API:

### Choose a Web Framework: Popular options include:

Flask: Lightweight and flexible, good for smaller projects. (https://flask.palletsprojects.com/)
Django REST Framework: Built on top of Django, provides powerful features for complex APIs. (https://www.django-rest-framework.org/)
FastAPI: High performance, automatic data validation, modern design principles. (https://github.com/tiangolo/full-stack-fastapi-template)

Consider factors like project size, complexity, and your familiarity with each framework.

### Set Up Your Development Environment:

- Install Python (version 3.6 or later recommended). (https://www.python.org/downloads/)
- Install your chosen web framework using pip (Python's package manager):

```bash
pip install flask
```

### Define Your API Resources:

- Identify the data or functionality your API will manage (e.g., books, tasks, users).
- Plan URL endpoints for accessing these resources (e.g., /books, /tasks/123, /users/me).

```python 
# GET /projects
# POST /projects
# GET /projects/:id
# DELETE /projects/:id
# PUT /projects/:id

# GET /tasks/:projectid
# POST /tasks
# GET /tasks/:id
# DELETE /tasks/:id
# PUT /tasks/:id

# GET /records/:projectid
# GET /records/:taskid
# POST /records
# GET /records/:id
# DELETE /records/:id
# PUT /records/:id

```

### Create API Endpoints:

- Use your framework's decorators to define routes that handle HTTP requests for specific URLs.

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/books', methods=['GET'])
def get_books():
    # Fetch book data from a database or other source
    books = [
        {'title': 'Book 1', 'author': 'Author 1'},
        {'title': 'Book 2', 'author': 'Author 2'}
    ]
    return jsonify(books)  # Convert data to JSON format

if __name__ == '__main__':
    app.run(debug=True)
```

### Handle HTTP Methods:

- Use appropriate methods (GET, POST, PUT, DELETE) based on actions:
  - GET: Retrieve data (e.g., /books/123 to get details of a specific book).
  - POST: Create new data (e.g., /tasks to create a new task).
  - PUT: Update existing data (e.g., /users/me to update user information).
  - DELETE: Delete data (e.g., /tasks/123 to delete a task).

### Process Requests and Generate Responses:

- Write code to handle incoming requests:
  - Extract data from request objects (e.g., query parameters, JSON payloads).
  - Perform actions using your data model or logic (e.g., database interactions).
- Return appropriate responses with relevant HTTP status codes (e.g., 200 for success, 404 for not found).

### Error Handling and Validation:

- Implement mechanisms to gracefully handle errors and unexpected situations.
- Validate user input to ensure data integrity.

### Testing:

- Thoroughly test your API to ensure it behaves as expected.
- Use testing frameworks like pytest or unittest or manual testing with tools like Postman (https://www.postman.com/).

### Deployment:

- Choose a deployment method based on your needs:
  - Local development server (for testing).
  - Cloud platforms like Heroku or AWS.
  - Web hosting services.

## Additional Considerations:

- Database Integration: For storing and managing persistent data, connect your API to a database like PostgreSQL, MySQL, or SQLite.
- Security: Secure your API against unauthorized access and vulnerabilities. Implement authentication, authorization, and input validation.
- Documentation: Provide clear documentation for developers using your API, explaining endpoints, request/response formats, and authentication requirements.

## Resources read during the training

- [Flask docs](flask.palletsprojects.com/en/3.0.x/api)
- [XD-DENG/flask-example](https://github.com/XD-DENG/flask-example?tab=readme-ov-file)
- [Deploy a flask app](https://cleavr.io/cleavr-slice/how-to-deploy-python-flask-framework)