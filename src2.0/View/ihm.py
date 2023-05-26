import json
import os.path

def createInitialConfigsJSON():
    res = {}
    resDir = '../Model/initialConfigs.json'

    if os.path.isfile(resDir):
        action = input("[Info] An initial Config file already exists.\n[Info] If you continue, a new one will be created and the old one will be overwrited.\nType q to quit, or anything else (enter) to continue :)\n")
        if action == 'q': return

    with open('ihm.json') as f:
        jsonObj = json.load(f)
        confObj = jsonObj['configFile']
        res = confObj
        for step in confObj:
            for key in confObj[step]:
                res[step][key] = input(confObj[step][key])
        
    with open(resDir, 'w') as outfile:
        json.dump(res,outfile)

def main():
    createInitialConfigsJSON()
    

if __name__ == "__main__":
    main()
