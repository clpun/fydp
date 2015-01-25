require(['jquery', 'Streamer', 'FrequencyPowerTable', 'SignalNameEnum', 'bootstrap', 'Chart'], function ($, Streamer, FrequencyPowerTable, SignalNameEnum) {
    var fpt;
    var deltapower;
	var thetapower;
	var alphapower;
	var betapower;
	var gammapower;
    $(document).ready(function () {
        $("td").click(function () {
            $(this).toggleClass("selected-cell");
            if ($(this).hasClass('selected-cell')) {
                fpt = new FrequencyPowerTable($(this).attr('id'));
                var table = fpt.toHtmlTable();
                $('#tables-spot').append(table);
                createDummyChartData(fpt);
            } else {
                removeTable($(this));
            }
        });
        var streamer = new Streamer();
        streamer.connect();
        streamer.request();
        $('body').on('bufferUpdated',function(){
        	var power_dict = streamer.consumeData();
        	console.log(power_dict);
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
    	var user = dict['userid'];
    	if(user != undefined) alert(user)
    	$('#userid').text(user);
    	deltapower = ['delta'];
    	thetapower = ['theta'];
    	alphapower = ['alpha'];
    	betapower = ['beta'];
    	gammapower = ['gamma'];
    }
});

