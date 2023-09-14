# this file is a controller for the Event Log generation

from sys import platform as _platform
import os, sys

from .tools.exceptions import *

from .tools import commitStruct
from .tools import logMining
from .tools import processMining
from .tools.models import selectMethod

from os import environ
from dotenv import load_dotenv
load_dotenv()

processor = logMining.LogMiner()

def writeCSV(log, name):
    processor.writePMLog(log, '{}{}.csv'.format(environ.get('TEMPDIR_PATH'), name))

def readLogFile(inputString):

    commits = processor.readGitLog(inputString)
    return commits

def buildActivity(caseBuilder, commits):

    hash_commitActivity = {}
    count = 0
    for commit in commits:
        modifier = caseBuilder.getCaseStrategyModifier(commit)
        activityList = caseBuilder.activityBuilder(commit, modifier)
        hash_commitActivity[count] = [commit,activityList]
        count += 1

    return hash_commitActivity

def getModifiedFileKeyword(mFile):
    commitKeywords = commitStruct.keywords()
    for key, value in commitKeywords.items():
        if value == mFile.status:
            return key

def parseCommits(commitsToParse):
    commits = []
    for c in commitsToParse:
        commit = commitStruct.Commit()
        commit.hash = c.hashID
        commit.user = c.user
        commit.email = c.email
        commit.date = c.date.strftime('%Y-%m-%dT%H:%M:%S%z')
        commit.message = c.message
        for modifiedFile in c.modifiedFiles:
            commit.modifiedFiles.append([getModifiedFileKeyword(modifiedFile), modifiedFile.modifiedFile])
        commits.append(commit)
    return commits


def miner(**kwargs):
    caseBuilder = processMining.CaseMapper()
    commitsThreshold = kwargs.get('minCommits', None)
    if not commitsThreshold:
        commitsThreshold = 10
    opt = '1'
    if 'arguments' in kwargs and '--local' in kwargs['arguments']:
        inputString =  "%r"%sys.argv[2]
        inputString = inputString.split('\'')[2]

        if _platform == "linux" or _platform == "linux2" or  _platform == "darwin":
        # linux or MAC OS X
            if '\\' in inputString:
                inputString.replace('\\\\', '/')

        elif _platform == "win32" or  _platform == "win64":
        # Windows
            if '/' in inputString:
                inputString.replace('/', '\\\\')

        repoName = inputString.split('log_git_')[1].split('.csv')[0]
        outputString = "log_prom_" + ''.join(repoName) + ".csv"

        # step #1: read log file and extract raw data into objects:
        commits = readLogFile(inputString)

    elif 'commits' not in kwargs or not kwargs['commits']:
        raise CommitsNotFound

    # commits came from database
    else:
        commits = parseCommits(kwargs['commits'])

    try:
    # step #2: choose the PM model and build case ID
        selectMethod(opt, commits, caseBuilder)
    # step #3: build activities names (filepath remap -> activity)
        activities = buildActivity(caseBuilder, commits)

    # step #4: generate output (csv) ready for DISCO or ProM format
        output = processor.generatePMlog(activities, caseBuilder, commitsThreshold)
        del caseBuilder
        return output

    except ValueError:
        raise Exception('Unsupported filename passed. ')

    except CommitsNotFound as e:
        raise Exception({'error': e.args[0]['errors'], 'message': e.args[0]['message']})


def main(argv):
    pass
    #TODO: process arguments for local mining

if __name__ == '__main__':
    main(sys.argv)