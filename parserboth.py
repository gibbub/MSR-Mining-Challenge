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



y = commits.find({}, {'message': 1, 'committer_id': 1})    # Finds commits with messages & prints them


projects_byCommitterID = {}  # Commits with same committer ID (person who made the commit)

for data in y:
    committerID = data['committer_id']
    message = data['message']

    # Committer ID
    if committerID in projects_byCommitterID:
        projects_byCommitterID[committerID].append(message)
    else:
        projects_byCommitterID[committerID] = [message]

#initializes counters
totalAll = 0
projectCount = 0
commitCount = 0
avg = 0
for id in projects_byCommitterID:
    all = 0
    projectCount += 1
    for message in projects_byCommitterID[id]:
        #checks for references to both refactoring and bug fixes
        if "refactor" in message or "Refactor" in message or "REFACTOR" in message or "rearrange" in message or "Rearrange" in message or "REARRANGE" in message or "restructure" in message or "Restructure" in message or "RESTRUCTURE" in message or "streamline" in message or "Streamline" in message or "STREAMLINE" in message or "redesign" in message or "Redesign" in message or "REDESIGN" in message or "alter" in message or "Alter" in message or "ALTER" in message:
            commitCount += 1
            if "bug" in message or "Bug" in message or "BUG" in message or "fix" in message or "Fix" in message or "FIX" in message:
                totalAll += 1
                all += 1
        elif "bug" in message or "Bug" in message or "BUG" in message or "fix" in message or "Fix" in message or "FIX" in message:
            commitCount += 1
    #only prints intances where references to both are present
    if all > 0:
        print(f"Both commits: {all}")
        avg += 1

#print total sums
print(f"Total committers: {projectCount}")
print(f"Total projects: {avg}")
print(f"Total commits: {commitCount}")
print(f"Total both commits: {totalAll}")

