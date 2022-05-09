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
print(f"Average amount of commits per committer: {round(ac_count / len(projects_byCommitterID))}\n")


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
    split = round(split / len(info), 2)
    return split

# Find average amount of bug fixes per committer
# @param info: Commits arranged by committer ID
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

# Finds average amount of commits containing 'bug fix'
# @param info: Commits arranged by committer ID
def findAvgBugFixes(info):
    avg_bugfix = 0
    for i in info:
        avg_bugfix += info[i]["% 'Bug fix'"]
    avg_bugfix = round(avg_bugfix / len(info), 2)
    return avg_bugfix

# Finds average amount of commits containing 'debug'
# @param info: Commits arranged by committer ID
def findAvgDebugs(info):
    avg_debug = 0
    for i in info:
        avg_debug += info[i]["% 'Debug'"]
    avg_debug = round(avg_debug / len(info), 2)
    return avg_debug

#########################################################

print("\n*First Split ----")
split1 = findRefactoringSplit(info_byCommitterID)
temp1 = splitByRefactoring(split1, info_byCommitterID)
under_split = temp1[0]
over_split = temp1[1]

print(f"Bugfix |-------%2.01---------||<={split1}<||--------%3.4--------|")
print(f"Debug  |-------%0.56---------|<=2%<|--------%1.16-------|\n")
print(f"Split info on: {split1}% refactorings")
print(f"Commits under/equal to refactorings split: {len(under_split)}")
print(f"Commits over refactorings split: {len(over_split)}\n")
print(f"Average % of commits under split that contain 'bug fix' : {findAvgBugFixes(under_split)}")
print(f"Average % of commits over spilt that contain 'bug fix' : {findAvgBugFixes(over_split)}")
print(f"Average % of commits under split that contain 'debug' : {findAvgDebugs(under_split)}")
print(f"Average % of commits over split that contain 'debug' : {findAvgDebugs(over_split)}")

#############################################################

print("\n*2nd Split -----")

# 2nd Split (Under)
split2 = findRefactoringSplit(under_split)
temp2 = splitByRefactoring(split2, under_split)
under_split2 = temp2[0]
over_split2 = temp2[1]

# 2nd Split (Over)
split3 = findRefactoringSplit(over_split)
temp3 = splitByRefactoring(split3, over_split)
under_split3 = temp3[0]
over_split3 = temp3[1]

print(f"Bugfix |----%{findAvgBugFixes(under_split2)}----|<={split2}<|----%{findAvgBugFixes(over_split2)}----||<={split1}<||----%{findAvgBugFixes(under_split3)}----|{split3}|----%{findAvgBugFixes(over_split3)}----|")


print("\n*3rd Split -----")



print("\n---- Splitting on Percent of Bugfix-Related Commits ----")

split_bugfix = findBugFixSplit(info_byCommitterID)

bugfix_under = {}
bugfix_over = {}

for info in info_byCommitterID:
    if info_byCommitterID[info]["% 'Bug fix'"] <= split_bugfix:
        bugfix_under[info] = info_byCommitterID[info]
    else:
        bugfix_over[info] = info_byCommitterID[info]


avg_under_refactor = 0
avg_over_refactor = 0
for x in bugfix_under:
    avg_under_refactor += bugfix_under[x]["% Refactorings"]
for y in bugfix_over:
    avg_over_refactor += bugfix_over[y]["% Refactorings"]

avg_under_refactor = round(avg_under_refactor / len(bugfix_under), 2)
avg_over_refactor = round(avg_over_refactor / len(bugfix_over), 2)

print(f"Split info on: {split_bugfix}% bug fixes")
print(f"Commits under/equal to bug fix split: {len(bugfix_under)}")
print(f"Commits over to bug fix split: {len(bugfix_over)}")
print(f"Average % of commits under bugfix split that contain 'refactor' : {avg_under_refactor}")
print(f"Average % of commits over bugfix split that contain 'refactor' : {avg_over_refactor}")
