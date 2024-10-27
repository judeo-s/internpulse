# Internship Stage 4 - Library API

**Overview**
This repository contains the code for the library management API created as part of the backend developer internship program.

### Functionality

The API allows users to manage books in a library. The following operations are supported:

* **Create:** Add a new book by sending a POST request with the book details in the request body.
* **Retrieve:**
	+ Retrieve book information by ID: Send a GET request to a specific URL endpoint with the book ID.
	+ Retrieve book information by title: Send a GET request with the book title as a query parameter.
* **Update:**
	+ Update book information by ID: Send a PUT request with the new book details in the request body and the book ID in the URL.
	+ Update book information by title: Send a PUT request with the new book details in the request body and the book title as a query parameter.
* **Delete:**
	+ Delete book by ID: Send a DELETE request to a specific URL endpoint with the book ID.
	+ Delete book by title: Send a DELETE request with the book title as a query parameter.

### Technical Specifications

**API Framework:** Flask
**Data Persistence:** SQLite database

### Implementation

The API is structured as follows:

* `app.py`: The main entry point for the API, this file initializes the Flask application and defines the routes.
* `api`: A package containing the API code.
	+ `models.py`: Defines the database models for the books table.
	+ `views.py`: Contains the API endpoints.
	+ `__init__.py`: Initializes the API package.
* `tests`: A directory containing the unit tests for the API.
* `data`: A directory containing the database file.
* `requirements.txt`: A file containing the list of dependencies required for the API.

### Setup and Run the API

To set up and run the API locally, follow these steps:

1. **Clone the Repository**

	First, clone the repository to your local machine using the following command:
	+ `git clone https://github.com/judeo-s/internpulse.git`

2. **Install Dependencies**

	Next, install the necessary dependencies by running the following command:
	+ `pip install -r requirements.txt`

3. **Run the API**

	Finally, run the API by executing the following command:
	+ `python3 app.py`

### Postman API Documentation

The API is documented using Postman. To view the documentation, click [here](https://documenter.getpostman.com/view/37655731/2sAY4sk5Cs).
