# This file contains a parser which takes in SmartSHARK data and performs analyses #

import pymongo
from pycoshark.mongomodels import Commit, CommitChanges, Refactoring

client = pymongo.MongoClient("mongodb://localhost:27017/")

# Database Name
db = client["smartshark_2_2"]

# Collection Names
commits = db["commit"]
commit_changes = db["commit_changes"]
refactorings = db["refactoring"]

# Simple Tests
x = commits.find_one()
print(x)

y = commits.find({}, {'message': 1})    # Finds commits with messages & prints them
# for data in y: print(data)
z = []
#substring = "bug"
count = 0
count2 = 0

firstcommit = None
firstid = None

next = False
countCor = 0
nextcommits = []

for data in y:
    count2 += 1
    message = data['message']
    commitid = data['_id']
    if "refactor" in message or "Refactor" in message or "REFACTOR" in message or "rearrange" in message or "Rearrange" in message or "REARRANGE" in message or "restructure" in message or "Restructure" in message or "RESTRUCTURE" in message or "streamline" in message or "Streamline" in message or "STREAMLINE" in message or "redesign" in message or "Redesign" in message or "REDESIGN" in message or "alter" in message or "Alter" in message or "ALTER" in message:
        if "bug" in message or "Bug" in message or "BUG" in message or "fix" in message or "Fix" in message or "FIX" in message:
            print("Both commit")
            print(message)
            z.append(data)
            count += 1



print(count)




