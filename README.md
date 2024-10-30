systemctl status mongod
mongosh mongodb://localhost:27017
show dbs
use community
db.students.find().pretty()
db.students.deleteOne({ user_id: "basic_user" })
db.groups.deleteOne({ creator_id: "Vish02" })

python3 -m core.server

# Student Group Management API

A RESTful API for managing student groups and authentication. The API allows students to sign up, sign in, create groups, and manage their group memberships.

## Authentication Endpoints

### Sign Up
Create a new student account.

```http
POST /student/signup
```

**Request Body:**
```json
{
    "user_id": "Vish02",
    "name": "Vishal",
    "email": "Vishu",
    "password": "veryverysecurepassword123",
    "rating": 10
}
```

<!-- another user -->
```json
{
    "user_id": "blue_flames",
    "name": "blue flame",
    "email": "blue_flame@gmail.com",
    "password": "verysecurepassword123",
    "rating": 10
}
```

**Success Response:**
```json
{
    "status": "success",
    "message": "Student signed up successfully",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IlZpc2h1IiwiZXhwIjoxNzMwMzE5NDkxfQ.jBijfkT_GSj5QWsFjaejdz9V2eqSg_0GvLgeQ33QgUs",
        "student": {
            "id": "671ce6f7659d1fd2af977459",
            "name": "Vishal",
            "email": "Vishu",
            "created_at": "2024-10-26T18:26:23.865470",
            "updated_at": "2024-10-26T18:26:23.865526",
            "rating": 10,
            "group_list": [],
            "group_limit": 5
        }
    },
    "status_code": 201
}
```

### Sign In
Authenticate an existing student.

```http
POST /student/signin
```

**Request Body:**
```json
{
    "email": "Vishu",
    "password": "veryverysecurepassword123"
}
```

**Success Response:**
```json
{
    "status": "success",
    "message": "Student signed in successfully",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "student": {
            "id": "671ce6f7659d1fd2af977459",
            "user_id": "Vish02",
            "name": "Vishal",
            "email": "Vishu",
            "created_at": "2024-10-26T18:26:23.865000",
            "updated_at": "2024-10-26T18:26:23.865000",
            "rating": 10,
            "group_list": [],
            "group_limit": 5
        }
    },
    "status_code": 200
}
```

## Group Management Endpoints

### Create Group
Create a new study group.

```http
POST /group/create_group
```

**Request Body:**
```json
{
    "name": "Django",
    "feild": "Web Development",
    "min_requirement": 5,
    "creator_id": "Vish02"
}
```

**Success Response:**
```json
{
    "status": "success",
    "message": "Group created successfully",
    "data": null,
    "status_code": 201
}
```

## Database Schema

### Student Collection

```javascript
{
    _id: ObjectId,
    id: ObjectId,
    user_id: String,
    name: String,
    email: String,
    password: String,  // Hashed using bcrypt
    created_at: DateTime,
    updated_at: DateTime,
    rating: Number,
    group_list: Array,
    group_limit: Number
}
```

## Status Codes

- 200: OK
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

<!-- 
```bash
gh pr create --base <base-branch> --head <branch-name> --title "PR Title" --body "Description of the changes"
``` -->

group_id : "67223f67f9e66bc05ca502c4"
user_id : "blue_flames"

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJsdWVfZmxhbWVAZ21haWwuY29tIiwiZXhwIjoxNzMwMzIyMDQ2fQ.iQ4uydAs0Wskcrg3SDrHOIyHatfc2D1pkCQmb0sF7ro