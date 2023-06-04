import json
import os.path

def createInitialConfigsJSON():
    res = {}
    resDir = './static/configs/initialConfigs.json'

    if os.path.isfile(resDir):
        action = input("[Info] An initial Config file already exists.\n[Info] If you continue, a new one will be created and the old one will be overwritten.\nType q to quit, or anything else (enter) to continue :)\n")
        if action == 'q': return

    with open('./static/templates/ihm.json') as f:
        jsonObj = json.load(f)
        res = jsonObj
        for step in jsonObj:
            for key in jsonObj[step]:
                res[step][key] = input(jsonObj[step][key])
        
    with open(resDir, 'w') as outfile:
        json.dump(res,outfile)

def createOrUpdateRoutersJSON():
    initialConfigs = json.load(open("./static/configs/initialConfigs.json"))

    if os.path.isfile('./static/configs/routers.json'):
        action = input("[Info] A router config file already exists.\n[Info] If you continue, a new one will be created and the old one will be overwritten.\nType q to quit, or anything else (enter) to continue :)\n")
        if action == 'q': return

    routerObj = {"CE":[],"PE":[],"P":[]}
    currentLoopback = 1
    currentIpSuffix = 1
    routerTemplates = json.load(open("./static/templates/routers.json"))
    
    for i in range(0,int(initialConfigs["routers"]["nbOfCE"])):
        routerCE = {}
        for elem in routerTemplates["CE"]:
            if elem == "loopback0": 
                routerCE[elem] = str(routerTemplates["CE"][elem]).replace("$",str(currentLoopback))
                currentLoopback = currentLoopback+1
            else: 
                routerCE[elem] = str(routerTemplates["CE"][elem]).replace("$",str(i))
        routerObj["CE"].append(routerCE)
    
    for i in range(0,int(initialConfigs["routers"]["nbOfPE"])):
        routerPE = {}
        for elem in routerTemplates["PE"]:
            if elem == "loopback0": 
                routerPE[elem] = str(routerTemplates["PE"][elem]).replace("$",str(currentLoopback))
                currentLoopback = currentLoopback+1
            elif "IPg" in elem and elem != "IPg1/0":
                routerPE[elem] = str(routerTemplates["PE"][elem]).replace("$",str(currentIpSuffix))
                currentIpSuffix = getNewIpSuffix(currentIpSuffix)
            else: 
                routerPE[elem] = str(routerTemplates["PE"][elem]).replace("$",str(i))
        routerObj["PE"].append(routerPE)

    for i in range(0,int(initialConfigs["routers"]["nbOfP"])):
        routerP = {}
        for elem in routerTemplates["P"]:
            if elem == "loopback0": 
                routerP[elem] = str(routerTemplates["P"][elem]).replace("$",str(currentLoopback))
                currentLoopback = currentLoopback+1
            elif "IPg" in elem:
                routerP[elem] = str(routerTemplates["P"][elem]).replace("$",str(currentIpSuffix))
                currentIpSuffix = getNewIpSuffix(currentIpSuffix)
            else: 
                routerP[elem] = str(routerTemplates["P"][elem]).replace("$",str(i))
        routerObj["P"].append(routerP)
    
    with open("./static/configs/routers.json", 'w') as outfile:
        json.dump(routerObj,outfile)
    
    print("[Done] A new router config json file have been automatically created in ./static/configs/routers.json \nKindly check it, as default configs might not work well for some specific cases :)")

def getNewIpSuffix(currentIp):
    if (currentIp+2)%4 == 0: return currentIp+3
    return currentIp+1

def main():
    # ihm test
    createInitialConfigsJSON()
    createOrUpdateRoutersJSON()
    

if __name__ == "__main__":
    main()
