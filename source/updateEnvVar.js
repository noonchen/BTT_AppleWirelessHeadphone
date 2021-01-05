(async ()=> {

    //Change it to the name of your device 
    let devNAME = "Someone's AirPods Pro" 
    
    let TB_uuid = 'D0657B9A-53F4-49CE-8568-6D8248D0000E';
    let MB_uuid = '3F38EE27-E68A-49D2-8969-787AAB07C3B9';
    
    //update TB trigger
    var props_tb = await callBTT('get_trigger', {uuid: TB_uuid});
    var oldConfig_tb = JSON.parse(props_tb)["BTTShellScriptWidgetGestureConfig"];
    var newConfig_tb = oldConfig_tb.split('=')[0].concat('="', devNAME, '"');
    var updateDefinition_tb = {"BTTShellScriptWidgetGestureConfig" : newConfig_tb};
    callBTT('update_trigger', {uuid: TB_uuid, json: JSON.stringify(updateDefinition_tb)});
    
    //update MB trigger
    var props_mb = await callBTT('get_trigger', {uuid: MB_uuid});
    var oldConfig_mb = JSON.parse(props_mb)["BTTAdditionalConfiguration"];
    var newConfig_mb = oldConfig_mb.split('=')[0].concat('="', devNAME, '"');
    var updateDefinition_mb = {"BTTAdditionalConfiguration" : newConfig_mb};
    callBTT('update_trigger', {uuid: MB_uuid, json: JSON.stringify(updateDefinition_mb)});
    
    //toggle device
    let shellscript = "\"BTT_PRESET_PATH\"/BTAudioSwitch -toggleSwitch -devName=".concat('\"', devNAME, '\"');
    let shellScriptWrapper = {
        script: shellscript};
    let result = await runShellScript(shellScriptWrapper);
    returnToBTT(result);
    })();