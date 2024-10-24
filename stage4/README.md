# Library System API

This project is a simple RESTful API to manage a library system. The API is built using Flask and uses SQLAlchemy to interact with a SQLite database.

## Functionality

The API offers the following functionalities:

* **Retrieve a list of all books:** Send a GET request to `/books` to retrieve a list of all books in the library. The response will include the title, author, genre, and publication date of each book.
* **Get the details of a specific book:** Send a GET request to `/books/<id>` to retrieve the details of a specific book. The response will include the title, author, genre, publication date, availability status, edition, and summary of the book.
* **Add a new book:** Send a POST request to `/books` to add a new book to the library. The request body should include the title, author, genre, publication date, availability status, edition, and summary of the book.
* **Update a book:** Send a PUT request to `/books/<id>` to update the details of an existing book. The request body should include the new values for the title, author, genre, publication date, availability status, edition, and summary of the book.
* **Delete a book:** Send a DELETE request to `/books/<id>` to delete a book from the library. The book will be deleted if it is lost, damaged, or no longer available in the library.

## API Endpoints

* **GET /books:** Retrieve a list of all books in the library.
* **GET /books/<id>:** Retrieve the details of a specific book.
* **POST /books:** Add a new book to the library.
* **PUT /books/<id>:** Update the details of an existing book.
* **DELETE /books/<id>:** Delete a book from the library.

## Request and Response Formats

* **Request Body:** The request body should be a JSON object with the following keys:
	+ `title`: The title of the book.
	+ `author`: The author of the book.
	+ `genre`: The genre of the book.
	+ `publication_date`: The publication date of the book.
	+ `availability_status`: The availability status of the book.
	+ `edition`: The edition of the book.
	+ `summary`: The summary of the book.
    + `created_at`: The date the book details were entered into the database.
    + `updated_at`: The date the book details were updated in the database.
    
* **Response:** The response will be a JSON object with the following keys:
	+ `status`: A string indicating the status of the request.
	+ `message`: A string indicating the result of the request.
	+ `data`: A JSON object containing the details of the book, if applicable.


