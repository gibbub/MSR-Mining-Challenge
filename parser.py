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