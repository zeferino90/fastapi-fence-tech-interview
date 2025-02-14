# Fence tech interview

## 1. Objective of this document

I'm going to document what I'm doing or researching while doing the tech problem.

## 2. Problem

### Overview

You will be working with a basic FastAPI project. Your task is to implement an audit trail mechanism for the POST /items/ endpoint. The audit trail should log user activities such as the action performed, the endpoint accessed, and other relevant details.
If you have questions, ask, but it’s also good to take assumptions and keep developing according to them.

### Objectives

1. Log User Actions:
   - Record details like:
     - User ID
     - Action performed Timestamp of the action.
     - Payload data (the item created).
     - Endpoint accessed.
2. Store Audit Logs:
   - Save the logs in the format and method of your choosing.
3. Reusable Design:
   - Implement a scalable and reusable solution that could apply to other endpoints in the future.
4. Queryable Logs (Optional, bonus points):
   - Expose endpoints that allow viewing and filtering those logs.
   - Suggest or implement a way for admin users to query these logs.

### Project Details

- A basic FastAPI project is provided with:
  - A single POST /items/ endpoint to create items.
  - GET endpoints
- You can decide to use it or not based on your design choice
- https://github.com/fence-technology/fastapi

### Requirements

- Implement the audit trail mechanism efficiently.
- Keep your code clean, modular, and maintainable.
- Avoid logging sensitive information like passwords or tokens.
- Ensure your solution is scalable for a real-world application.

### Bonus Points

- Add features like:
  - Filters for querying logs (e.g., by user, action, or date).
  - Asynchronous logging using background tasks.
  - Tests to verify functionality and edge cases.
- Documented next steps with:
  - Assumptions taken
  - Missing things to have the full functionality ready
  - Upgrades to improve

### Deliverables

1. Functional code with the audit trail implemented.
2. Tests (if time permits).

### The review session with Fence

- You will present the solution showing how it works and what design choices you made.
- We will ask you about the why’s of certain design choices to understand your reasoning.

### Questions

- Do not hesitate to ask questions by sending an email to bandeira@fence.finance.
- We will try to respond as soon as possible.
- If no response is received, take an assumption and explain your assumption during the presentation, that is fine

## 3. Basic usage

### Run local

#### Install dependencies

```
pip install -r requirements.txt
```

#### Run server

```
uvicorn app.main:app --reload
```

#### Run test

```
pytest app/test/test.py
```

### Run with docker

#### Run server

```
docker-compose up -d --build
```

#### Run test

```
docker-compose exec app pytest app/test/test.py
```

## API documentation (provided by Swagger UI)

```
http://127.0.0.1:8000/docs
```

#### Run server

```
docker-compose exec db psql --username=fastapi --dbname=fastapi
```
## 4. Assumptions
### Database and Model Synchronization:  
Assumes that the database schema and the SQLModel models are always in sync.
Assumes that the AuditLog table is created correctly when SQLModel.metadata.create_all(engine) is called.
### Authentication and Authorization:  
Assumes that the get_current_user function will always return a valid username if the token is valid.
Assumes that the User model's verify_password method will correctly verify the password.
### Middleware and Logging:  
Assumes that the AuditLogMiddleware will correctly capture and log all API requests and responses.
Assumes that the request and response bodies can always be decoded and filtered correctly.
### Token Handling:  
Assumes that the JWT tokens are always correctly encoded and decoded using the SECRET_KEY and ALGORITHM.
Assumes that the token expiration is handled correctly and that expired tokens will raise the appropriate exceptions.
### Database Session Management:  
Assumes that the get_db function will always provide a valid database session.
Assumes that the database session is correctly managed and closed after each request.
### Unique Constraints and Indexes:  
Assumes that the username field in the User model is unique and indexed correctly.
### Environment Setup:  
Assumes that the environment variable TESTING is set to "true" during tests.
Assumes that the database connection string and other configurations are correctly set up in the environment.
### Data Seeding:  
Assumes that the seed_database function will correctly seed the initial data into the database.
These assumptions can lead to potential issues if any of them are not met. It is important to validate and handle exceptions for these assumptions to ensure the robustness of your application.


## 5. Missing things

### Error Handling  
Comprehensive error handling for database operations, JSON parsing, and token validation.
Custom exception handling for better error messages and debugging.

### Validation
I can improve the validation of the request body and query parameters, leveraging Pydantic models.

### Testing
Unit tests and integration tests to verify the functionality of the application.
Tests for edge cases and error scenarios.

### Documentation  
Improve readability for functions and classes so they are as self-explanatory as possible.
Additional documentation for setting up the development environment and running the application.

### Security
Secure handling of sensitive information such as passwords and tokens.
Implementation of rate limiting and other security measures to protect the API.

### Logging  
More detailed logging for debugging and monitoring purposes.
External logging integration for centralized monitoring and analysis.

### Configuration Management
Use of environment variables or configuration files to manage application settings.
Separation of development, testing, and production configurations.

### Scalability
Consideration for scaling the application, such as using background tasks for logging and other resource-intensive operations.


### Performance Optimization  
Optimization of database queries and API response times.
Use of caching mechanisms to improve performance.

### Code Quality
Code refactoring to improve readability and maintainability.
Adherence to coding standards and best practices. Putting in place tools like mypy, pylint, ruff, etc.
I'd like to add those tools to pre-commit so it's difficult to forget without running them.
In the same line I'd add those automation tools to the CI/CD pipeline.


## 6. Future ideas

- External logging:
  - Not reinventing the wheel
  - Centralized monitoring
  - Search and filter easily
  - Integrated with visualization on other software
  - Scales well
  - If it's a cloud system we don't need to manage the logging system
