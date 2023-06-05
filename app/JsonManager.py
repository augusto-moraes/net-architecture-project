import json
import os.path

initialConfigsDir = './static/configs/initialConfigs.json'
routersConfigDir = './static/configs/routers.json'

def createInitialConfigsJSON():
    res = {}

    if os.path.isfile(initialConfigsDir):
        action = input("[Info] An initial config file already exists.\n[Info] If you continue, a new one will be created and the old one will be overwritten.\nType q to quit, or anything else (enter) to continue :)\n")
        if action == 'q': return

    with open('./static/templates/ihm.json') as f:
        jsonObj = json.load(f)
        res = jsonObj
        for step in jsonObj:
            for key in jsonObj[step]:
                res[step][key] = input(jsonObj[step][key])
        
        if res["routers"]["nbOfPE"] > res["routers"]["nbOfCE"]:
            print("[Warning] Weird behaviour: You have more PEs than CEs. Is that right? \nPlease check the initialConfigs.json file")
        
        res["project"]["server_url"] = "http://192.168.33.128:3080"
        res["project"]["user"] = "admin"
        res["project"]["cred"] = "1234"
        
    with open(initialConfigsDir, 'w') as outfile:
        json.dump(res,outfile)

def createOrUpdateRoutersJSON():
    initialConfigs = getInitialConfigs()

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
            elif elem == "vrfInt" or elem == "availableInt":
                routerCE[elem] = routerTemplates["PE"][elem]
            else: 
                routerCE[elem] = str(routerTemplates["CE"][elem]).replace("$",str(i))
        routerObj["CE"].append(routerCE)
    
    for i in range(0,int(initialConfigs["routers"]["nbOfPE"])):
        routerPE = {}
        for elem in routerTemplates["PE"]:
            if elem == "loopback0": 
                routerPE[elem] = str(routerTemplates["PE"][elem]).replace("$",str(currentLoopback))
                currentLoopback = currentLoopback+1
            elif elem == "vrfInt" or elem == "availableInt":
                routerPE[elem] = routerTemplates["PE"][elem]
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
            elif elem == "vrfInt" or elem == "availableInt":
                routerP[elem] = routerTemplates["PE"][elem]
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

def getInitialConfigs():
    if not os.path.isfile(initialConfigsDir):
        action = input("[Error] Oops, something went wrong: no initial configs file have been found\nType enter to create a new one")
        if action == 'q': return
        createInitialConfigsJSON()
    return json.load(open("./static/configs/initialConfigs.json"))

def getRoutersConfig():
    if not os.path.isfile(routersConfigDir):
        action = input("[Error] Oops, something went wrong: no routers configs file have been found\nType enter to create a new one")
        if action == 'q': return
        createOrUpdateRoutersJSON()
    return json.load(open("./static/configs/routers.json"))

def main():
    # ihm test
    createInitialConfigsJSON()
    createOrUpdateRoutersJSON()
    

if __name__ == "__main__":
    main()
