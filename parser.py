# This file contains a parser which takes in SmartSHARK data and performs analyses #

import pymongo
import unittest
from pycoshark.mongomodels import Commit, CommitChanges, Refactoring

client = pymongo.MongoClient("mongodb://localhost:27017/")

# Database Name
db = client["smartshark_2_2"]

# Collection Names
commits = db["commit"]

# ~~~~~~~~~~
# Analyses
# ~~~~~~~~~~
all_commits = commits.find({}, {'message': 1, 'vcs_system_id': 1})  # Finds commits with messages & prints them

bug_count = 0
bugfix_count = 0
debug_count = 0
refactor_count = 0
total = 0

bug_commits = []
bugfix_commits = []
debug_commits = []

# Instances of "bug", "debug", and "refactor" in all commits
for data in all_commits:
    total += 1
    message = data['message']
    if "bug" in message or "Bug" in message or "BUG" in message:
        bug_commits.append(message)
        bug_count += 1
    if ("bug" in message or "Bug" in message or "BUG" in message) and (
            "fix" in message or "Fix" in message or "FIX" in message):
        bugfix_commits.append(message)
        bugfix_count += 1
    if "debug" in message or "Debug" in message or "DEBUG" in message:
        debug_commits.append(message)
        debug_count += 1
    if "refactor" in message or "Refactor" in message or "REFACTOR" in message:
        refactor_count += 1

refactor_bug_count = 0
refactor_debug_count = 0
refactor_bugfix_count = 0

# Instances where "refactor" and "bug"/"bug fix"/"debug" are used in same commit message
for message in bug_commits:
    if "refactor" in message or "Refactor" in message or "REFACTOR" in message:
        refactor_bug_count += 1

for message in bugfix_commits:
    if "refactor" in message or "Refactor" in message or "REFACTOR" in message:
        refactor_bugfix_count += 1

for message in debug_commits:
    if "refactor" in message or "Refactor" in message or "REFACTOR" in message:
        refactor_debug_count += 1

print("---- Instances of 'bug', 'bug fix, and 'debug' ----")
print(f"     Total commits: {total}")
print(f"    Contains 'bug': {bug_count}")
print(f"Contains 'bug fix': {bugfix_count}")
print(f"  Contains 'debug': {debug_count}")
print("")

print("---- Instances of 'refactor' alone, with bugs, bugfixes, and debugs ----")
print(f"      Commits with 'refactor':   {refactor_count}")
print(f"    With 'refactor' and 'bug':   {refactor_bug_count}")
print(f"With 'refactor' and 'bug fix':   {refactor_bugfix_count}")
print(f"  With 'refactor' and 'debug':   {refactor_debug_count}")
print("")

print("---- Percentages ----")
print(f"{round((refactor_bug_count / bug_count) * 100, 2)}% of commits containing 'bug' also contain 'refactor'")
print(f"{round((refactor_bug_count / refactor_count) * 100, 2)}% of commits containing 'refactor' also contain 'bug'\n")

print(
    f"{round((refactor_bugfix_count / bugfix_count) * 100, 2)}% of commits containing 'bug fix' also contain 'refactor'")
print(
    f"{round((refactor_bugfix_count / refactor_count) * 100, 2)}% of commits containing 'refactor' also contain 'bug fix'\n")

print(f"{round((refactor_debug_count / debug_count) * 100, 2)}% of commits containing 'debug' also contain 'refactor'")
print(
    f"{round((refactor_debug_count / refactor_count) * 100, 2)}% of commits containing 'refactor' also contain 'debug'\n")

# Idea: Store different projects (found by ids) and measure how many times
# bug fixes and refactorings are used in commits
# Does the amount of refactorings go up the more bug fixes there are?

ac = commits.find({}, {'message': 1, 'vcs_system_id': 1, 'author_id': 1, 'committer_id': 1, 'parents': 1})

# Dictionary that stores a list of commits for each unique project
projects_byVCS = {}  # Commits with same version control system ID
projects_byAuthorID = {}  # Commits with same author ID (person who made commit code)
projects_byCommitterID = {}  # Commits with same committer ID (person who made the commit)
projects_byParents = {}  # Commits that share the same commit parent(s)

ac_count = 0
for data in ac:
    ac_count += 1
    vcsID = data['vcs_system_id']
    authorID = data['author_id']
    committerID = data['committer_id']
    parents = data['parents']

    message = data['message']

    # VCS
    if vcsID in projects_byVCS:
        projects_byVCS[vcsID].append(message)
    else:
        projects_byVCS[vcsID] = [message]

    # Author ID
    if authorID in projects_byAuthorID:
        projects_byAuthorID[authorID].append(message)
    else:
        projects_byAuthorID[authorID] = [message]

    # Committer ID
    if committerID in projects_byCommitterID:
        projects_byCommitterID[committerID].append(message)
    else:
        projects_byCommitterID[committerID] = [message]

    # Parents
    p_len = len(parents)
    p_count = 0
    for p in parents:
        p_count += 1
        if p in projects_byParents:
            projects_byParents[p].append(message)
            break
        else:
            if p_count == p_len:
                projects_byParents[p] = [message]

print("---- Commits sorted by shared VCSs, author ids, committer ids, and parent commits ----")
print(f"All commits: {ac_count}")
print(f"Projects by VCS: {len(projects_byVCS)}")
print(f"Projects by AuthorID: {len(projects_byAuthorID)}")
print(f"Projects by Committer ID: {len(projects_byCommitterID)}")
print(f"Projects by Parent: {len(projects_byParents)}\n")


# By Committer ID
# Stores info by:
#  id:   { Total commits: #,
#         % Refactorings: #,
#         % 'Bug fix': #,
#         % 'Debug':   #  }
info_byCommitterID = {}

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

print(f"Info by Committer ID: {len(info_byCommitterID)}")

split = 0
for info in info_byCommitterID:
    #print(info_byCommitterID[info]["% Refactorings"])
    split += info_byCommitterID[info]["% Refactorings"]

split = round(split / len(info_byCommitterID))

print(f"Split info on: {split}% refactorings")

under_split = {}
over_split = {}

for info in info_byCommitterID:
    if info_byCommitterID[info]["% Refactorings"] <= split:
        under_split[info] = info_byCommitterID[info]
    else:
        over_split[info] = info_byCommitterID[info]

print(f"Commits under or equal to split (by committer ID): {len(under_split)}")
print(f"Commits over split (by committer ID): {len(over_split)}")
print("\nNow we are going to examine whether projects with more refactorings \nhave more bug fixes, or the other way around")

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

