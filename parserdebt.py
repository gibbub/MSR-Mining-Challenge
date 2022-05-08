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
    if "debt" in message or "Debt" in message or "DEBT" in message:
        print("Technical debt commit")
        print(message)
        z.append(data)
        count += 1
        next = True
    elif next==True:
        print('this is the next commit')
        print(commitid)
        print(message)
        nextcommits.append(data)
        if "bug" in message or "Bug" in message or "BUG" in message:
            countCor+=1
        next = False


print(count)
print(countCor)



