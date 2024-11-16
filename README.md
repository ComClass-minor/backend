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

```json
{
    "status": "success",
    "message": "Student signed up successfully",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJsdWVfZmxhbWVAZ21haWwuY29tIiwiZXhwIjoxNzMwOTM0MTIxfQ.c-5-7dO0oNnfLW_ITbEsVkDufoeTmry7VCVp5P1qKlc",
        "student": {
            "id": "672b99ff3eb7e8eac55ef74e",
            "name": "blue flame",
            "email": "blue_flame@gmail.com",
            "created_at": "2024-11-06T22:01:59.939992",
            "updated_at": "2024-11-06T22:01:59.940032",
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

## API Create Blog

```http
POST /blog/create_blog
```

**Request Body:**
```json
{
    "title": "Hell Yeah",
    "content": "too too much content",
    "author_id": "satyam"
}
```

**Success Response:**
```json
{
    "status": "success",
    "message": "Blog created successfully",
    "data": null,
    "status_code": 201
}
``` 
{
    "status": "success",
    "message": "Student signed in successfully",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhdHlhbV9qaGFAZ21haWwuY29tIiwiZXhwIjoxNzMxNzczNzU5fQ.flXVpUqq3WaUFM4MW1T-cJaGG_J43l8A4vb_oJgNYHg",
        "student": {
            "id": "672c89ef6df9367db4775391",
            "user_id": "satyam",
            "name": "Satyam Jha",
            "email": "satyam_jha@gmail.com",
            "password": "$2b$12$biS7/ItHPiFbH2N2ja339et0P9/BQBl1uFS3qdzijWvKYCXR2oNoO",
            "created_at": "2024-11-07T09:35:43.123000",
            "updated_at": "2024-11-07T09:35:43.123000",
            "rating": 10,
            "group_list": [],
            "group_limit": 5
        }
    },
    "status_code": 200
}

## API Get Blogs

```http
GET /blog/get_blogs?author_id={author_id} || GET /blog/get_blogs?author_id=satyam 
```

**Success Response:**
```json
{
    "status": "success",
    "message": "Blogs retrieved successfully",
    "data": [
        {
            "id": "6738b9b77109004fe268674b",
            "title": "Hell Yeah",
            "content": "too too much content",
            "author_id": "satyam",
            "created_at": "2024-11-16T15:26:47.358000",
            "total_likes": 0
        }
    ],
    "status_code": 200
}
```

## API Like Blog

```http
PUT /blog/like_blog
```

**Request Body:**
```json
{
    "blog_id" : "6738b9b77109004fe268674b",
    "user_id" : "satyam"
}
```

**Success Response:**
```json
{
    "status": "success",
    "message": "Blog removed successfully",
    "data": {
        "blog_id": "6738b9b77109004fe268674b",
        "deleted_at": "2024-11-16T16:42:27.437510"
    },
    "status_code": 200
}
```
