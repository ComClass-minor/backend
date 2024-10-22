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
  "password": "verysecurepassword123"
}

signin
{
  "email": "blue_flame@gmail.com",
  "password": "verysecurepassword123"
}
