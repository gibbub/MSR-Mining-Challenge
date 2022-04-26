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


y = commits.find({}, {'message': 1})    # Finds commits with messages & prints them
# for data in y: print(data)


bug_count = 0
debug_count = 0
refactor_count = 0
total = 0

bug_commits = []
debug_commits = []

for data in y:
    total += 1
    message = data['message']
    if "bug" in message or "Bug" in message or "BUG" in message:
        bug_commits.append(message)
        bug_count += 1
    if "debug" in message:
        debug_commits.append(message)
        debug_count += 1
    if "refactor" in message or "Refactor" in message:
        refactor_count += 1

print("---- Instances of 'bug' and 'debug' ----")
print(f" Total commits: {total}")
print(f"          Bugs: {bug_count}")
print(f"  Size of bugs: {len(bug_commits)}")
print(f"        Debugs: {debug_count}")
print(f"Size of debugs: {len(debug_commits)}")
print("")



refactor_debug_count = 0
refactor_bug_count = 0

for message in debug_commits:
    if "refactor" in message or "Refactor" in message:
        refactor_debug_count += 1

for message in bug_commits:
    if "refactor" in message or "Refactor" in message:
        refactor_bug_count += 1

print("---- Instances of 'refactor' alone, with bugs, and with debugs ----")
print(f"   Refactoring count:   {refactor_count}")
print(f"Refactoring & debugs:   {refactor_debug_count}")
print(f" Refactorings & bugs:   {refactor_bug_count}")

