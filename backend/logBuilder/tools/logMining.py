import os,sys,inspect
from .commitStruct import Commit, keywords
from pathlib import Path

class LogMiner():
  '''
  this class is a file parser for I/O purposes.
  '''
  def readGitLog(self, filepath):
    try:
      listCommits = []
      commit = Commit()
      commitKeywords = keywords()
      with open(filepath, mode='r', encoding='utf-8') as file:
        for line in file:
          if line[0] == "\"": #indicates a commit start point
            s = line.replace(',', "")
            #remove aaaa""bbbb""...
            s = s.replace('\"\"', '\"')
            # split the string in tokens, remove first and last member
            # since they result in empty strings
            tokens = s.split("\"")[1:-1]
            #SET commit main info
            commit.hash = tokens[0]
            commit.user = tokens[1]
            commit.email = tokens[2]
            commit.date = tokens[3]
            commit.message = tokens[4]
            #SET modified files, along with Git terminology
          elif line[0] in commitKeywords.keys():
            commit.modifiedFiles.append(line.split("\t"))
          elif line[0] == '\n':
            listCommits.append(commit)
            commit = Commit()

        return listCommits

    except EOFError:
      print("error in reading data.")
      raise

    except IOError:
      print("file not found.")
      raise

  def generatePMlog(self, dict_commit_activity, cases, commitsThreshold):
    try:
      log = {}
      count = 0
      for tuple_obj in dict_commit_activity.items():
        commit = tuple_obj[1][0]
        key = cases.getCaseStrategy(commit)
        if cases.caseMap()[key][1] >= int(commitsThreshold):
          for activity in tuple_obj[1][1]:
            log[count] = {
              "case": cases.caseMap()[key][0],
              "activity": activity,
              "timestamp": commit.date,
              "commit": commit.hash,
            }
            count += 1

    except KeyError as e:
      print("error while processing event log at {}.".format(e))
      return -1
    finally:
      return log

  def writePMLog(self, data, filepath):
    try:
      my_file = Path(filepath)
      count = 1
      while my_file.is_file():
        filepath = filepath.split('.csv')[0]
        if '_copy' in filepath:
          filepath = filepath.split('_copy')[0] + '_copy' + str(count)
        else:
          filepath += '_copy' + str(count)
        count += 1
        filepath += '.csv'
        my_file = Path(filepath)
      with open(filepath, mode='w', encoding='utf-8') as file:
        file.write("Case ID,Activity,Timestamp,Commit\n")
        for rows in data.values():
          file.write('{},{},{},{}\n'.format( \
            rows['case'], \
            rows['activity'], \
            rows['timestamp'], \
            rows['commit']))
    except IOError:
      print("path not found.")
      raise
