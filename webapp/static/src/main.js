require(['jquery', 'Streamer', 'FrequencyPowerTable', 'SignalNameEnum', 'lodash', 'bootstrap'], function ($, Streamer, FrequencyPowerTable, SignalNameEnum, _) {
    var signalMap = {};
    var streamerRunning = false;
    var streamer = new Streamer();
    var REQUEST_NAME = 'request_test_data'; // For actual data use: 'request'

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

    function runStreamer () {
        if (streamerRunning) return;
        streamerRunning = true;

        streamer.connect();
        //streamer.request(REQUEST_NAME);
        $('body').on('bufferUpdated',function(){
        	var power_dict = streamer.consumeData();
        	console.log(power_dict);
        	analyze_data(power_dict);
        });
    }

    $(document).ready(function () {
        if (window.navigator.platform && window.navigator.platform.indexOf('Mac') !== -1)
            switchDebugMode($('#debug-switch'));

        $("#debug-switch").on('click', switchDebugMode);

        $("#sensor_table").on('click', 'td', function (event) {
            var $td = $(event.target);
            var sensorName = $td.text();

            $td.toggleClass("selected-cell");
            if ($td.hasClass('selected-cell')) {
                var frequencyPowerTable = new FrequencyPowerTable(sensorName);
                $('#tables-spot').append(frequencyPowerTable.toHtmlTable());
                signalMap[sensorName] = frequencyPowerTable;

                runStreamer();
            } else {
                removeTable(sensorName);
                signalMap[sensorName] = undefined;
                if (_(signalMap).values().compact().size() === 0) {
                    streamer.stop();
                }
            }
        });
    });

    var request = function(request) {
        var endpoint = '//' + document.domain + ':' + location.port + '/';
        $.get(endpoint + request);
    };

    function switchDebugMode ($btn) {
        if (!($btn instanceof jQuery))
            $btn = $($btn.target);

        if ($btn.hasClass('on')) {
            $btn.removeClass('on');
            $btn.text('Debug Mode: OFF');
            request('disable_test_mode');
        } else {
            $btn.addClass('on');
            $btn.text('Debug Mode: ON');
            request('enable_test_mode');
        }
    }

    function removeTable (sensorName) {
        $('#' + sensorName + '-table').remove();
    }

    /*
		power_dict format: {"delta":{{"F3":123,"F4":123}},"theta":{},"alpha":{},"beta":{},"gamma":{}}
    */
    function analyze_data (signals) {
        _.forOwn(signalMap, function(frequencyPowerTable, sensorName) {
            if (frequencyPowerTable !== undefined) {
                _(SignalNameEnum.signalTypes).mapValues(function (signalType) {
                    frequencyPowerTable.handleIncomingSignalUpdate(signalType, signals[signalType.toLowerCase()][sensorName]);
                });
            }
        });
    }
});
