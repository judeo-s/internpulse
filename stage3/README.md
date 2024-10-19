## Internship Stage 3 - Product Management API

**Overview**
In this stage of the internship, all backend developer interns were tasked to
implement a product management API.



## TASK

This repository contains the backend API implementation for a simple product management system, completed as part of the Internpulse backend developer internship.

### Functionality

The API offers functionalities for managing products, including:

* **Create:** Add a new product by sending a POST request with the product name in the request body.
* **Retrieve:**
    * Retrieve product information by name: Send a GET request with the product name as a query parameter.
    * Retrieve product information by ID: Send a GET request to a specific URL endpoint with the product ID.
* **Update:**
    * Update product name by name: Send a PUT request with the new name in the request body and the old name as a query parameter.
    * Update product name by ID: Send a PUT request with the new name in the request body and the product ID in the URL.
* **Delete:**
    * Delete product by name: Send a DELETE request with the product name as a query parameter.
    * Delete product by ID: Send a DELETE request to a specific URL endpoint with the product ID.

### Technical Specifications

**API Framework:** [**Specify chosen framework here (e.g., Flask, Django, Express)**]
**Data Persistence:** [**Specify chosen storage method here (e.g., In-memory storage, Database - name)**]
**Error Handling:** Implemented for various scenarios with appropriate HTTP status codes (e.g., 400, 404, 500).
**Testing:** Unit tests cover the functionality of each API endpoint.

### Deliverables

* Functional backend API code with unit tests
* Documentation (README.md) explaining:
    * API Endpoints
    * Request/Response Formats
    * Error Handling
* Instructions for running the API locally (command line commands)

### Evaluation Criteria

* Functionality and correctness of the API
* Code quality, readability, and maintainability
* Unit test coverage and effectiveness
* Clarity and completeness of the documentation

### Deployment (Optional)

You can deploy the API to a platform like PythonAnywhere, Vercel, Netlify, or any other preferred service. 

### Getting Started

1. Clone this repository.
2. Install the required dependencies (refer to `requirements.txt` if using).
3. Refer to the specific framework documentation for instructions on running the API locally.

**Note:** Replace bracketed information with specifics based on your chosen framework and implementation details.

### Additional Resources

* Framework Documentation (link to official documentation)
* Unit Testing Tutorial (link to relevant tutorial)

This README serves as a starting point. Feel free to add further details and explanations as you build the API.
