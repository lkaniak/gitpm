# This file holds models for activity parsing within the commits.
# The model needs to be declared in here and implemented on the processMining.py script

def version_dir(caseBuilder, commits):
    caseBuilder.caseStrategy('caseID', 'version')
    caseBuilder.caseStrategy('activity', 'dir')
    for commit in commits:
        #build cIDs
        caseBuilder.build(commit.email)
        case = caseBuilder.caseMap()[commit.email]
        commit.caseid = case[0]

def bug_status(caseBuilder, commits):
    pass

def branch_dir(caseBuilder, commits):
    caseBuilder.caseStrategy('caseID', 'branches')
    caseBuilder.caseStrategy('activity', 'dir')

def version_tagDir(caseBuilder, commits):
    caseBuilder.caseStrategy('caseID', 'version')
    caseBuilder.caseStrategy('activity', 'tag')
    for commit in commits:
        #build cIDs
        caseBuilder.build(commit.email)
        case = caseBuilder.caseMap()[commit.email]
        commit.caseid = case[0]


def selectMethod(opt, commits, caseBuilder):
    '''activity parser selector'''
    #version/release as Case ID and dir as activities (each commit is a version of the software)
    if opt == '1':
        version_dir(caseBuilder, commits)

    #Bug issue as Case ID and issue status as activities (needs gitHub API)
    elif opt == '2':
        bug_status(caseBuilder, commits)

    #Branches as Case ID and dir as activities (needs gitHub API)
    elif opt == '3':
        branch_dir(caseBuilder, commits)

    #user email as Case ID and tag + dir as activities
    elif opt == '4':
        version_tagDir(caseBuilder, commits)

