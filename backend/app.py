from pymongo import MongoClient

# must run python3 -m pip install pymongo[tls]
client = MongoClient("mongodb+srv://huiminwu@mit.edu:stoop123@cluster0.j7aiy.mongodb.net/stoop?retryWrites=true&w=majority")
db = client.test
print(db.users)
print(db.volunteers)
print(db.requests) # how do i test this annie
# i will run u should see my terminal bc i shared it w u