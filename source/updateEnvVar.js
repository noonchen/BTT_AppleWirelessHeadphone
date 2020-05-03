(async ()=> {

    //Change it to the name of your device 
    let devNAME = "Someone's AirPods Pro" 
    
    var props = await callBTT('get_trigger', {uuid: 'D0657B9A-53F4-49CE-8568-6D8248D0000E'});
    var oldConfig = JSON.parse(props)["BTTShellScriptWidgetGestureConfig"]
    var newConfig = oldConfig.split('=')[0].concat('="', devNAME, '"')
    
    var updateDefinition = {"BTTShellScriptWidgetGestureConfig" : newConfig}
    callBTT('update_trigger', {uuid: 'D0657B9A-53F4-49CE-8568-6D8248D0000E',json: JSON.stringify(updateDefinition)});
    
    returnToBTT(newConfig);
    })();