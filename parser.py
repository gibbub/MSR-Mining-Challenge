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
all_commits = commits.find({}, {'message': 1,'vcs_system_id': 1})  # Finds commits with messages & prints them

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
    if ("bug" in message or "Bug" in message or "BUG" in message) and ("fix" in message or "Fix" in message or "FIX" in message):
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

print(f"{round((refactor_bugfix_count / bugfix_count) * 100, 2)}% of commits containing 'bug fix' also contain 'refactor'")
print(f"{round((refactor_bugfix_count / refactor_count) * 100, 2)}% of commits containing 'refactor' also contain 'bug fix'\n")

print(f"{round((refactor_debug_count / debug_count) * 100, 2)}% of commits containing 'debug' also contain 'refactor'")
print(f"{round((refactor_debug_count / refactor_count) * 100, 2)}% of commits containing 'refactor' also contain 'debug'\n")

# Idea: Store different projects (found by ids) and measure how many times
# bug fixes and refactorings are used in commits
# Does the amount of refactorings go up the more bug fixes there are?

ac = commits.find({}, {'message': 1, 'vcs_system_id': 1, 'author_id': 1, 'committer_id': 1, 'parents': 1})

# Dictionary that stores a list of commits for each unique project
projects_byVCS = {}         # Commits with same version control system ID
projects_byAuthorID = {}    # Commits with same author ID (person who made commit code)
projects_byCommitterID = {} # Commits with same committer ID (person who made the commit)
projects_byParents = {}     # Commits that share the same commit parent(s) --> Actually commits from same project

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
    for p in parents:
        if p in projects_byParents:
            projects_byParents[p].append(message)
            break
        else:
            projects_byParents[p] = [message]
            break

print("---- Commits sorted by shared VCSs, author ids, committer ids, and parent commits ----")
print(f"All commits: {ac_count}")
print(f"Projects by VCS: {len(projects_byVCS)}")
print(f"Projects by AuthorID: {len(projects_byAuthorID)}")
print(f"Projects by Committer ID: {len(projects_byCommitterID)}")
print(f"Projects by Parent: {len(projects_byParents)}\n")



