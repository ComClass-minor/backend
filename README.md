systemctl status mongod
mongosh mongodb://localhost:27017
show dbs
use community
db.students.find().pretty()
db.students.deleteOne({ user_id: "basic_user" })

python3 -m core.server

singup
{ 
    "user_id": "Vish02", 
    "name": "Vishal", 
    "email": "Vishu", 
    "password": "veryverysecurepassword123",
    "rating": 10 
}
response
{
    "status": "success",
    "message": "Student signed up successfully",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IlZpc2h1IiwiZXhwIjoxNzI5OTcwNzg1fQ.nZaisOc6Wd0_uWZsGB2v2bA2g-i1rHJdSggPSzHGU44",
        "student": {
            "id": "id=ObjectId('671ce6f7659d1fd2af977459') user_id='Vish02' name='Vishal' email='Vishu' password='$2b$12$vO1HKKhE9nchH2B4/Ap1bumm1teWUZBBDKAs6pfaUv5sCSbojKACK' created_at=datetime.datetime(2024, 10, 26, 18, 26, 23, 865470) updated_at=datetime.datetime(2024, 10, 26, 18, 26, 23, 865526) rating=10 group_list=[] group_limit=5",
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




signin
{
  "email": "Vishu",
  "password": "veryverysecurepassword123"
}
response
{
    "status": "success",
    "message": "Student signed in successfully",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IlZpc2h1IiwiZXhwIjoxNzI5OTcxMTQzfQ.YViyl2qolG0DOGjeJnJGkBT22p-Gw8gGkcm1G5Zv4i0",
        "student": {
            "id": "671ce6f7659d1fd2af977459",
            "user_id": "Vish02",
            "name": "Vishal",
            "email": "Vishu",
            "password": "$2b$12$vO1HKKhE9nchH2B4/Ap1bumm1teWUZBBDKAs6pfaUv5sCSbojKACK",
            "created_at": "2024-10-26T18:26:23.865000",
            "updated_at": "2024-10-26T18:26:23.865000",
            "rating": 10,
            "group_list": [],
            "group_limit": 5
        }
    },
    "status_code": 200
}

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJsdWVfZmxhbWVAZ21haWwuY29tIiwiZXhwIjoxNzI5Nzk2NzYzfQ.7IEBkNUl3A0qyQh8BG8GzH6KA27OZwfZ8eBISikhKiQ

gh pr create --base <base-branch> --head <branch-name> --title "PR Title" --body "Description of the changes"

group/create_group
{
    "name": "Django",
    "feild": "Web Development",
    "min_requirement": 5,
    "creator_id": "Vish02"
}
response
{
    "status": "success",
    "message": "Group created successfully",
    "data": null,
    "status_code": 201
}


database student 
  {
    _id: ObjectId('671ce6f9659d1fd2af97745a'),
    id: ObjectId('671ce6f7659d1fd2af977459'),
    user_id: 'Vish02',
    name: 'Vishal',
    email: 'Vishu',
    password: '$2b$12$vO1HKKhE9nchH2B4/Ap1bumm1teWUZBBDKAs6pfaUv5sCSbojKACK',
    created_at: ISODate('2024-10-26T18:26:23.865Z'),
    updated_at: ISODate('2024-10-26T18:34:19.189Z'),
    rating: 10,
    group_list: null,
    group_limit: 4
  }