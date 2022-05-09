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
totalBugs = 0
totalRefact = 0
projectCount = 0
projects = 0


for id in projects_byCommitterID:
    projectCount += 1
    bugs = 0
    refactors = 0
    nextC = False
    #finds all cases of bug in commit messages
    for message in projects_byCommitterID[id]:
        if "bug" in message or "Bug" in message or "BUG" in message or "fix" in message or "Fix" in message or "FIX" in message:
            bugs += 1
            totalBugs += 1
            nextC = True
        #checks the following commit message for references to refactoring
        elif nextC:
            if "refactor" in message or "Refactor" in message or "REFACTOR" in message or "rearrange" in message or "Rearrange" in message or "REARRANGE" in message or "restructure" in message or "Restructure" in message or "RESTRUCTURE" in message or "streamline" in message or "Streamline" in message or "STREAMLINE" in message or "redesign" in message or "Redesign" in message or "REDESIGN" in message or "alter" in message or "Alter" in message or "ALTER" in message:
                refactors += 1
                totalRefact += 1
            nextC = False
    #only prints instances where refactoring follows bug fixes
    if bugs > 0 and refactors > 0:
        print(f"Bug commits: {bugs}")
        print(f"Refactor commits: {refactors}")
        projects += 1

#prints totals
print(f"Total committers: {projectCount}")
print(f"Total projects: {projects}")
print(f"Total bug commits: {totalBugs}")
print(f"Total refactor commits: {totalRefact}")







