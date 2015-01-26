require(['jquery', 'Streamer', 'FrequencyPowerTable', 'SignalNameEnum', 'lodash', 'bootstrap', 'Chart'], function ($, Streamer, FrequencyPowerTable, SignalNameEnum, _) {
//    var fpt;
//    var deltapower;
//	var thetapower;
//	var alphapower;
//	var betapower;
//	var gammapower;

    var signalMap = {};

    function putPowerTablesIntoMap() {
        _(SignalNameEnum.left).mapValues(function(value) {
            var table = new FrequencyPowerTable(value);
            $('#tables-spot').append(table.toHtmlTable());
            signalMap[value] = table;
        });
        _(SignalNameEnum.right).mapValues(function(value) {
            var table = new FrequencyPowerTable(value);
            $('#tables-spot').append(table.toHtmlTable());
            signalMap[value] = table;
        });
    }

    $(document).ready(function () {
//        $("td").click(function () {
//            $(this).toggleClass("selected-cell");
//            if ($(this).hasClass('selected-cell')) {
//                putPowerTablesIntoMap();
//            } else {
//                removeTable($(this));
//            }
//        });
        putPowerTablesIntoMap();
        var streamer = new Streamer();
        streamer.connect();
        streamer.request();
        $('body').on('bufferUpdated',function(){
        	var power_dict = streamer.consumeData();
        	analyze_data(power_dict);
        });
        $('#submitbtn').click(function(){
	        console.log('clicked');
	        // streamer.request();
	        // console.log('after click');
    	});
    });

    function createDummyChartData(fpt) {
        for (var i = 0; i < 20; i++)
            fpt.handleIncomingSignalUpdate(SignalNameEnum.signalTypes.Alpha, Math.floor(Math.random() * 100))
    }

    function removeTable (classSelected) {
        var classToRemove = classSelected.attr('id');
        $('#' + classToRemove + '-table').remove();
    }

    /*
		power_dict format: {"delta":{{"F3":123,"F4":123}},"theta":{},"alpha":{},"beta":{},"gamma":{}}
    */
    function analyze_data (dict) {
        var receivedSignalTypes = _(dict).keys();
        receivedSignalTypes.forEach(function(signalType) {
            var sensors = _(dict[signalType]).keys();
            sensors.forEach(function (sensor) {
                signalMap[sensor].handleIncomingSignalUpdate(signalType, dict[signalType][sensor]);
            });
        });

//    	var user = dict['userid'];
//    	if(user != undefined) alert(user);
//    	$('#userid').text(user);
//    	deltapower = ['delta'];
//    	thetapower = ['theta'];
//    	alphapower = ['alpha'];
//    	betapower = ['beta'];
//    	gammapower = ['gamma'];
    }
});

