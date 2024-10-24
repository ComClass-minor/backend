systemctl status mongod
mongosh mongodb://localhost:27017
show dbs
use community
db.students.find().pretty()
db.students.deleteOne({ user_id: "basic_user" })

python3 -m core.server

singup
{ 
    "user_id": "blue_flames", 
    "name": "blue flame", 
    "email": "blue_flame@gmail.com", 
    "password": "verysecurepassword123",
    "rating": 7 
}

signin
{
  "email": "blue_flame@gmail.com",
  "password": "verysecurepassword123"
}


eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJsdWVfZmxhbWVAZ21haWwuY29tIiwiZXhwIjoxNzI5Nzk2NzYzfQ.7IEBkNUl3A0qyQh8BG8GzH6KA27OZwfZ8eBISikhKiQ

gh pr create --base <base-branch> --head <branch-name> --title "PR Title" --body "Description of the changes"

group/create_group
{
    "name": "example_group",
    "feild": "example_field",
    "min_requirement": 1,
    "creator_id": "blue_flames"
}