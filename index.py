#! C:/path_to_python/python.exe

from md99authtoken import md99authtoken

# system modules
import os
import sys
import json

# local modules
import config
import data

#---------------------------------------
def entryPoint1 ():
   
    # ------- Section: Route Detection -----------
    path = os.environ["REQUEST_URI"]
    authParams = getAuthRoute1 (path)

    if authParams[0] == "error":
        print ("<br />Invalid Route")
        print ("<br />")
        print (authParams)
        return

    print ("<br />Requesting the URL for")
    print ("<br /> - Value: " + str(authParams[0]))
    print ("<br /> - Asset: " + authParams[1])
        
    publicKey = config.getConfig ("public_key")
    secretKey = config.getConfig ("secret_key")
    value     = authParams[0]
    assetName = authParams[1]
    fullUrl   = md99authtoken.processAll (publicKey, secretKey, value, assetName)

    print ("<br />Image URL:")
    print ("<br />")
    print (fullUrl)

#---------------------------------------
def entryPoint2 ():

    # ------- Section: Route Detection -----------
    path = os.environ["REQUEST_URI"]
    customerName = getCustomerNameFromRoute (path)

    if customerName == "**error**":
        print ("<br />Invalid Route")
        print ("<br />")
        return

    print ("<br />Requesting the URL for")
    print ("<br /> - Customer: " + customerName)
        
    publicKey = config.getConfig ("public_key")
    secretKey = config.getConfig ("secret_key")
    assetName = config.getConfig ("default_asset");
    value     = data.getCustomerValue (customerName)
    fullUrl   = md99authtoken.processAll (publicKey, secretKey, value, assetName)

    print ("<br />Image URL:")
    print ("<br />")
    print (fullUrl)

#---------------------------------------
def entryPoint3 ():
   
    # ------- Section: Route Detection -----------
    path = os.environ["REQUEST_URI"]
    if validateAuthRoute2 (path) == False:
        print ("<br />Unknown URL")
        return
    
    value, assetName = getPostParams ()
    if value == None:
        print ("<br />Invalid Post Params")
        return
        
    publicKey = config.getConfig ("public_key")
    secretKey = config.getConfig ("secret_key")
    fullUrl   = md99authtoken.processAll (publicKey, secretKey, value, assetName)

    print ("<br />Image URL:")
    print ("<br />")
    print (fullUrl)

# ------- Function: Strip the Route -----------
def getAuthRoute1 (origPath):
    parts = origPath.split('/');
    start = 0
    if len(parts[0]) == 0:
        start = 1
    if len(parts) < start+3:
        return ["error", 0]
    if parts[start].lower() != "getauthurl":
        return ["error", 0]
        
    return [parts[start+1], parts[start+2]]

def validateAuthRoute2 (origPath):
    parts = origPath.split('/')
    numParts = len(parts)
    start = 0
    if len(parts[0]) == 0:
        start = 1
        numParts -= 1

    if numParts != 4:
        return False
        
    if parts[start+0].lower() != "get":
        return False
    if parts[start+1].lower() != "authurl":
        return False
    if parts[start+2].lower() != "from":
        return False
    if parts[start+3].lower() != "post":
        return False
        
    return True

def getCustomerNameFromRoute (origPath):
    parts = origPath.split('/');
    
    if len(parts[0]) == 0:
        parts.pop(0)
        
    if len(parts) != 4:
        return "**error**"
        
    if parts[0].lower() != "get":
        return "**error**"
    if parts[1].lower() != "customer":
        return "**error**"
    if parts[2].lower() != "score":
        return "**error**"
        
    return parts[3]

#---------------------------------------
def getPostParams ():
    postStr = str (sys.stdin.read())
    try:
        postArray = json.loads (postStr)
    except:
        print("Invalid JSON")
        return None, None

    if 'asset_name' in postArray  and  'value' in postArray:
        return postArray['value'], postArray['asset_name']

    if len (postArray) == 1:
        level2 = postArray[0]
        if 'asset_name' in level2  and  'value' in level2:
            return level2['value'], level2['asset_name']
            
    return None, None
    
#---------------------------------------
# This is what is executed on startup

print("Content-Type: text/html\n")

#--- This version uses a simple URL and can be run from a browser
#--- /myserver.com/getauthurl/55/first-asset
#entryPoint1()

#--- This version uses a simple URL and can be run from a browser
#--- /myserver.com/get/customer/score/betty
entryPoint2()

#--- This version uses POST params and needs to be run from a command prompt
#--- curl -H "Content-Type:application/json" -d "{\"asset_name\":\"bar-full\",\"value\":\"69\"}" -X POST http://myserver.com/get/authurl/from/post
#entryPoint3()

