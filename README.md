# Serverless CRUD API

A fully functional Serverless CRUD API built with Python to manage users and their managers using AWS Lambda-style handlers. This API supports user creation, retrieval, updating, and deletion operations with proper validations.

## Features

- ✅ Create new user
- 🔍 Fetch user by `user_id` or `manager_id`
- 🗑 Delete user
- ✏ Update user or bulk-update manager IDs
- 🔄 Input validation and error handling
- 📁 Clean separation of concerns (validation, data access, business logic)

## API Endpoints

| Method | Endpoint              | Description                                         |
|--------|-----------------------|-----------------------------------------------------|
| POST   | /create-user          | Create a new user                                   |
| GET    | /get-user/{user_id}   | Get user info by user ID or manager ID             |
| GET    | /get-user             | Get all users                                       |
| DELETE | /delete-user          | Delete user by user ID                              |
| PATCH  | /update-user          | Update user info or bulk update manager ID         |

## Folder Structure

- `user_table.py` - Handles data storage and retrieval
- `validation.py` - Manages all input and business rule validations
- `user.py` - Defines the `UserData` class
- `handlers.py` - API logic entry point for Lambda functions

## Tech Stack

- Python
- AWS Lambda-compatible handler structure
- JSON-based APIs

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/serverless-crud-api.git
