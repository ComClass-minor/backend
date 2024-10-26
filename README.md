systemctl status mongod
mongosh mongodb://localhost:27017
show dbs
use community
db.students.find().pretty()
db.students.deleteOne({ user_id: "basic_user" })

python3 -m core.server

# Student Group Management API

A RESTful API for managing student groups and authentication. The API allows students to sign up, sign in, create groups, and manage their group memberships.

## Authentication Endpoints

### Sign Up
Create a new student account.

```http
POST /signup
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

**Success Response:**
```json
{
    "status": "success",
    "message": "Student signed up successfully",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
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
POST /signin
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