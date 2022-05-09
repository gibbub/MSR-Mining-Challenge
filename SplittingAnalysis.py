# This file contains a parser which takes in SmartSHARK data and performs analyses #

import pymongo
import unittest
from pycoshark.mongomodels import Commit, CommitChanges, Refactoring

client = pymongo.MongoClient("mongodb://localhost:27017/")

# Database Name
db = client["smartshark_2_2"]

# Collection Names
commits = db["commit"]

# Store different projects (found by ids) and measure how many times
# bug fixes and refactorings are used in commits
# Does the amount of refactorings go up the more bug fixes there are?

ac = commits.find({}, {'message': 1, 'committer_id': 1})

# Dictionary that stores a list of commits for each unique project
projects_byCommitterID = {}  # Commits with same committer ID (person who made the commit)

ac_count = 0
for data in ac:
    ac_count += 1
    committerID = data['committer_id']
    message = data['message']

    # Committer ID
    if committerID in projects_byCommitterID:
        projects_byCommitterID[committerID].append(message)
    else:
        projects_byCommitterID[committerID] = [message]


print("---- Pre-Stuff Info ----")
print(f"All commits: {ac_count}")
print(f"Projects by Committer ID: {len(projects_byCommitterID)}")
print(f"Average amount of commits per committer: {round(len(projects_byCommitterID) / ac_count, 2)}\n")


# Stores more detailed information about each set of commits
#  id:   { Total commits: #,
#         % Refactorings: #,
#         % 'Bug fix': #,
#         % 'Debug':   #  }
info_byCommitterID = {}

# Sort through every commiter & commit message and store associated information
for id in projects_byCommitterID:
    total = len(projects_byCommitterID[id])
    refactorings = 0
    bugfix = 0
    debug = 0

    for message in projects_byCommitterID[id]:
        if 'refactor' in message or 'Refactor' in message or 'REFACTOR' in message:
            refactorings += 1
        if ("bug" in message or "Bug" in message or "BUG" in message) and (
                "fix" in message or "Fix" in message or "FIX" in message):
            bugfix += 1
        if "debug" in message or "Debug" in message or "DEBUG" in message:
            debug += 1

    info_byCommitterID[id] = {"Total commits": total,
                         "% Refactorings": round((refactorings / total) * 100, 2),
                         "% 'Bug fix'": round((bugfix / total) * 100, 2),
                         "% 'Debug'": round((debug / total) * 100, 2)}


print("---- Splitting on Percent of Refactoring-Related Commits ----")
print(f"Info by Committer ID: {len(info_byCommitterID)}")

# Find average amount of refactorings per committer
# @param info: List of commits sorted by committer ID
def findRefactoringSplit(info):
    split = 0
    for i in info:
        split += info[i]["% Refactorings"]
    split = round(split / len(info))
    return split

# Find average amount of bug fixes per committer
# @param info: List of commits sorted by committer ID
def findBugFixSplit(info):
    split = 0
    for i in info:
        split += info[i]["% 'Bug fix'"]
    split = round(split / len(info))
    return split


# Splits commits into 2 groups: those <= given split and > given split
# @param s: Percent to split on
# @param info: Commits arranged by committer ID
def splitByRefactoring(s, info):
    under_split = {}
    over_split = {}
    for i in info:
        if info[i]["% Refactorings"] <= s:
            under_split[i] = info[i]
        else:
            over_split[i] = info[i]
    return [under_split, over_split]


split = findRefactoringSplit(info_byCommitterID)
split_bugfix = findBugFixSplit(info_byCommitterID)
s = splitByRefactoring(split, info_byCommitterID)
under_split = s[0]
over_split = s[1]

print(f"Split info on: {split}% refactorings")
print(f"Commits under/equal to refactorings split: {len(under_split)}")
print(f"Commits over refactorings split: {len(over_split)}")

avg_under_bugfix = 0
avg_under_debug = 0
avg_over_bugfix = 0
avg_over_debug = 0

for x in under_split:
    avg_under_bugfix += under_split[x]["% 'Bug fix'"]
    avg_under_debug += under_split[x]["% 'Debug'"]

for y in over_split:
    avg_over_bugfix += over_split[y]["% 'Bug fix'"]
    avg_over_debug += over_split[y]["% 'Debug'"]

avg_under_bugfix = round(avg_under_bugfix / len(under_split), 2)
avg_under_debug = round(avg_under_debug / len(under_split), 2)
avg_over_bugfix = round(avg_over_bugfix / len(over_split), 2)
avg_over_debug = round(avg_over_debug / len(over_split), 2)

print(f"Average % of commits under split that contain 'bug fix' : {avg_under_bugfix}")
print(f"Average % of commits under split that contain 'debug' : {avg_under_debug}")
print(f"Average % of commits over spilt that contain 'bug fix' : {avg_over_bugfix}")
print(f"Average % of commits over split that contain 'debug' : {avg_over_debug}")


print("\n---- Splitting on Percent of Bugfix-Related Commits ----")
print(f"Split info on: {split_bugfix}% bug fixes")

bugfix_under = {}
bugfix_over = {}
for info in info_byCommitterID:
    if info_byCommitterID[info]["% 'Bug fix'"] <= split_bugfix:
        bugfix_under[info] = info_byCommitterID[info]
    else:
        bugfix_over[info] = info_byCommitterID[info]

print(f"Commits under/equal to bug fix split: {len(bugfix_under)}")
print(f"Commits over to bug fix split: {len(bugfix_over)}")

avg_under_refactor = 0
avg_over_refactor = 0
for x in bugfix_under:
    avg_under_refactor += bugfix_under[x]["% Refactorings"]
for y in bugfix_over:
    avg_over_refactor += bugfix_over[y]["% Refactorings"]

avg_under_refactor = round(avg_under_refactor / len(bugfix_under), 2)
avg_over_refactor = round(avg_over_refactor / len(bugfix_over), 2)

print(f"Average % of commits under bugfix split that contain 'refactor' : {avg_under_refactor}")
print(f"Average % of commits over bugfix split that contain 'refactor' : {avg_over_refactor}")
