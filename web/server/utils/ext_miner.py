import os, sys, subprocess, json, copy

# these functions control file reading on the process discovery step.

def readJSON(path):
      with open(path, mode='r', encoding='utf-8') as file:
            return json.load(file)

def readDOT(path):
      with open(path, mode='r', encoding='utf-8') as file:
            return file.read()


def callProcessMiner(**kwargs):
      """Runs MINERful on a .xes file located in temp folder.
      """
      params = copy.deepcopy(kwargs.get("params", []))
      if 'automaton' in params:
            params.remove("automaton")
            params.extend(['-pA',  "{}{}.dot".format(kwargs['tempDir'], kwargs['logName'])])
      commandList = ["./run-MINERful.sh",
            "-iLF",
            "{}{}.xes".format(kwargs['tempDir'], kwargs['logName']),
            "-JSON", "{}{}.json".format(kwargs['tempDir'], kwargs['logName']),
            ]
      commandList.extend(params)
      minerRetCode = subprocess.call(commandList, shell=False, cwd="{}".format(kwargs['pathToMiner']))


if __name__ == '__main__':
      callProcessMiner(sys.argv[1])
