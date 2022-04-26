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

x = commits.find({}, {'message': 1})    # Finds commits with messages & prints them
# for data in x:
    # print(data)

