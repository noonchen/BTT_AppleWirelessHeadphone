#!/usr/bin/env python3
#encoding:utf-8
from subprocess import check_output
import plistlib, os

disconnectedBGColor = "59,59,59,255"
connectedBGColor = "110,193,56,255"
# devNAME = "Noon’s AirPods Pro" # For testing only
devNAME = os.environ['devNAME'].strip('"')
osascript = ['osascript']
asobjc = ['''use framework "IOBluetooth"''',
          '''set deviceList to current application's IOBluetoothDevice's pairedDevices()''',
          '''set devNames to (deviceList's valueForKey:"name") as list''',
          '''set devStatus to (deviceList's valueForKey:"connected") as list''',
          '''set devAddress to (deviceList's valueForKey:"addressString") as list''',
          '[devNames, devStatus, devAddress]']
BT_plist_path = "/Library/Preferences/com.apple.Bluetooth.plist"
IOBTUI_resPath = "/System/Library/Frameworks/IOBluetoothUI.framework/Versions/A/Resources"

def jsonfy(text="", icon_data="", icon_path="", background_color="", font_color="", font_size=0):
    '''
    Convert data into JSON string for BTT to render
    '''
    import json
    dict = {}
    if text != "": dict["text"] = text
    if icon_data != "": dict["icon_data"] = icon_data
    if icon_path != "": dict["icon_path"] = icon_path
    if background_color != "": dict["background_color"] = background_color
    if font_color != "": dict["font_color"] = font_color
    if font_size != 0: dict["font_size"] = font_size
    return json.dumps(dict, ensure_ascii=False)

def getIconPath(IOBTUI_resPath, ProductID):
    with os.scandir(IOBTUI_resPath) as it:
        for item in it:
            if item.name.startswith("AssetPaths") and item.name.endswith(".plist"):
                info_dict = plistlib.load(open(item.path, 'rb'))
                if ProductID in info_dict:
                    return os.path.join(IOBTUI_resPath, info_dict[ProductID]['ImageName'])

def formatBatteryString(devCache, ProductID, connected):
    TwoBatteryProduct = ["0x2002", "0x200F", "0x200E"]
    if ProductID in TwoBatteryProduct:
        fontsize = 11
        Lbat = str(devCache["BatteryPercentLeft"]) if connected else '0'
        Rbat = str(devCache["BatteryPercentRight"]) if connected else '0'
        return fontsize, "🅛 %s\n🅡 %s"%(Lbat+'%' if Lbat!='0' else 'NC', Rbat+'%' if Rbat!='0' else 'NC')
    else:
        fontsize = 15
        bat = str(devCache["BatteryPercentSingle"]) if connected else '0'
        return fontsize, "%s"%(bat+'%' if bat!='0' else 'NC')

def main():
    # Get name, status and mac addr of current BT devices
    [osascript.extend(["-e", L]) for L in asobjc]
    rawInfo = check_output(osascript).decode('utf-8').strip().split(', ')
    N_devs = int(len(rawInfo)/3)
    BT_dict = dict(zip(rawInfo[:N_devs], [[rawInfo[N_devs+i], rawInfo[2*N_devs+i]] for i in range(N_devs)]))

    if devNAME in BT_dict:
        connected = True if BT_dict[devNAME][0] == "1" else False
        macAddr = BT_dict[devNAME][1]
        # Get detailed data from BT device cache
        devCache = plistlib.load(open(BT_plist_path, 'rb'))["DeviceCache"][macAddr]
        
        if "ProductID" in devCache:
            ProductID = "0x%X"%int(devCache["ProductID"])
            IconPath = getIconPath(IOBTUI_resPath, ProductID)
            fontsize, BatteryString = formatBatteryString(devCache, ProductID, connected)
            BGcolor = connectedBGColor if connected else disconnectedBGColor
            return jsonfy(text=BatteryString, icon_path=IconPath, font_size=fontsize, background_color=BGcolor)
        else:
            return jsonfy(text="ID not found", background_color=disconnectedBGColor)
    else:
        # Name is not correct or the device hasn't been connected to mac before
        return jsonfy(text="Not configured", background_color=disconnectedBGColor)
    
if __name__ == "__main__":
    print(main())
