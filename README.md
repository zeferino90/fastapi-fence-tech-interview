# Fence tech interview

## Objective of this document

I'm going to document what I'm doing or researching while doing the tech problem.

## Problem

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

# Basic usage

## Run local

### Install dependencies

```
pip install -r requirements.txt
```

### Run server

```
uvicorn app.main:app --reload
```

### Run test

```
pytest app/test/test.py
```

## Run with docker

### Run server

```
docker-compose up -d --build
```

### Run test

```
docker-compose exec app pytest app/test/test.py
```

## API documentation (provided by Swagger UI)

```
http://127.0.0.1:8000/docs
```

### Run server

```
docker-compose exec db psql --username=fastapi --dbname=fastapi
```


## Future ideas

- External logging:
  - Not reinventing the wheel
  - Centralized monitoring
  - Search and filter easily
  - Integrated with visualization on other softwares
  - Scales well
  - If it's a cloud system we dont need to manage the logging system
