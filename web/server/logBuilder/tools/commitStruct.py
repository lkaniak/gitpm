#class for internal commit modeling
class Commit():

    def __init__(self):
        self.caseid = 0
        self.user = ""
        self.hash = ""
        self.email = ""
        self.date = ""
        self.message = ""
        self.modifiedFiles = []
        #[GIT_OP, FILE_MOD]

    #METHODS
    def searchModifiedFiles(self,file):
        '''
        Searches if file was M/A/D in commit.
        '''
        for row, i in enumerate(self.modifiedFiles):
            try:
                column = i.index(file)
            except ValueError:
                continue
            return row, column
        return -1

    def stringify(self):
        mFiles = ""
        for file in self.modifiedFiles:
            mFiles += "{" + "{}".format(file[0]) + " {}".format(file[1].split('\n')[0]) + "} "
        return "{hash: "+self.hash+"}" + \
    " {user: "+self.user+"}" + \
    " {email: "+self.email+"}" + \
    " {date-time: "+self.date+"}" + \
    " {message: "+self.message+"}" + \
    " {modified-files: ["+mFiles[:-1]+"]}"

#helpers
def keywords():
    return {
        "M": "Modified",
        "A": "Added",
        "D": "Deleted",
        "R": "Renamed",
        "T": "Type-Changed",
        "U": "Unmerged",
        "X": "Unknown"}

