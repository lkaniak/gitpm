import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from .commitStruct import Commit

class CaseMapper():
    '''
    this class is a parser for activities in the commit data.
    '''
    #'{:03}'.format(1)
    _caseID = 1
    _caseStrategy = {
        'caseid': '',
        'activity': ''
    }
    _caseMap = {}

    #SET caseID
    def caseID(self, inc):
        self._caseID += inc

    #GET caseMap
    def caseMap(self):
        return self._caseMap
    #SET caseMap
    def setCaseMap(self, caseID, activity):
        self._caseMap[caseID] = activity

    #SET caseStrategy
    def caseStrategy(self, key, value):
        try:
            if key.lower() != 'caseid':
                if key.lower() != 'activity':
                    raise ValueError
                else:
                    self._caseStrategy[key.lower()] = value
            else:
                self._caseStrategy[key.lower()] = value
        except ValueError:
            print("invalid key for input: {}".format(key))

    #methods
    def incEvent(self, instance):
        inc = self.caseMap()[instance][1] + 1
        self.caseMap()[instance][1] = inc

    def build(self, instance):
        #[caseID, activity(event)]
        if instance not in self.caseMap().keys():
            self.caseMap()[instance] = [self._caseID,1]
            self.caseID(1)
        else:
            self.incEvent(instance)

    def findMessageTag(self, message, tagDefiner):
        parsedStringArray = message.split(tagDefiner)
        tag = ''
        if len(parsedStringArray) == 1:
            # default return if a tag is not found in the message
            return 'XX'
        else:
            for c in parsedStringArray[1]:
                if c.isdigit() or c.isalpha():
                    tag += c
            return tag



    def activityBuilder(self, commit, mod):
        activityList = []
        for activity in commit.modifiedFiles:
            for mFile in activity[1:]:
                if 'dir' in self._caseStrategy['activity']:
                    activityList.append(self.parseActivityByDir(mFile))
                elif 'tag' in self._caseStrategy['activity']:
                    activity = mod + self.parseActivityByDir(mFile)
                    activityList.append(activity)
                #print(activityList)
        return activityList

    def parseActivityByDir(self, activityString):
        result = ''
        if '\n' in activityString:
            activityString = activityString.split('\n')[0]
        if '/' in activityString:
            paths = activityString.split('/')[:-1]
            for path in paths:
                result += path + '-'
            result = result[:-1]
        else:
            result = 'ROOT'
        return result

    def parseActivityByDirSimplified(self, activityString):
        result = ''
        if '\n' in activityString:
            activityString = activityString.split('\n')[0]
        if '/' in activityString:
            paths = activityString.split('/')[:-1]
            result = paths[0]
        else:
            result = 'ROOT'
        return result

    def parseActivityByFilename(self, activityString):
        result = ''
        if '\n' in activityString:
            activityString = activityString.split('\n')[0]
        if '/' in activityString:
            parsedString = activityString.split('/')
            activity = self.parseActivityByDir(parsedString[-1])
            parsedString = parsedString[:-1]
            for path in parsedString:
                result += path + '-'
            result = result[:-1]
            result += '_' + activity
        else:
            if '.' in activityString[0]:
                result = activityString.split('.')[1]
            elif '.' in activityString:
                result = activityString.rsplit('.', 1)[0]
            else:
                result = activityString
        return result

    def getCaseStrategy(self, commit):
        if self._caseStrategy['caseid'] is 'version':
            return commit.email

    def getCaseStrategyModifier(self, commit):
        if 'tag' in self._caseStrategy['activity']:
            return self.findMessageTag(commit.message, '#') + '#'
        else:
            return ''

sys.path.remove(parentdir)