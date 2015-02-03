require(['jquery', 'Streamer', 'FrequencyPowerTable', 'SignalNameEnum', 'lodash', 'bootstrap'], function ($, Streamer, FrequencyPowerTable, SignalNameEnum, _) {
    var signalMap = {};
    var streamerRunning = false;
    var streamer = new Streamer();
    var contMode = true;
    var startTimedMode = false;
    var flushingChart = false;
    var request = function(request) {
        var endpoint = '//' + document.domain + ':' + location.port + '/';
        $.get(endpoint + request);
    };

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
        $('body').on('bufferUpdated',function(){
        	var power_dict = streamer.consumeData();
        	//console.log(power_dict);
        	if (power_dict == 'recording_done') {
        		//console.log('recording done');
        		$('#reset-btn').text('Record');
				startTimedMode = false;
				prompt_user_to_export_csv();
        	} else {
        		analyze_data(power_dict);
        	}
        });
    }

    $(document).ready(function () {
        if (window.navigator.platform && window.navigator.platform.indexOf('Mac') !== -1)
            switchDebugMode($('#debug-switch'));

        request('verify_user');
        $("#debug-switch").on('click', switchDebugMode);
		$('#cont-timed-switch').on('click', switchContMode);
		$('#reset-btn').on('click', resetBtn);
        $("#sensor_checkbox").on('change',':checkbox',function (event){
        	var sensorName = this.value;
        	if(this.checked) {
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

        /*$("#sensor_table").on('click', 'td', function (event) {
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
        });*/
    });

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

    function switchContMode ($btn) {
        if (!($btn instanceof jQuery))
            $btn = $($btn.target);

        if ($btn.hasClass('on')) {
            request('start_streaming');
            $btn.removeClass('on');
            $btn.text('Continuous Mode');
            //console.log("Continuous Mode");
            $('#reset-btn').text('Reset');
            contMode = true;

            clear_export_btn();
            clear_recording_buffer();
        } else {
            request('stop_streaming');
            $btn.addClass('on');
            $btn.text('Timed Mode');
            startTimedMode = false;
            $('#reset-btn').text('Start');
            contMode = false;
        }
    }

    function resetBtn ($btn) {
		if(contMode) {
			flushingChart = true;
			flushAllCharts();
			flushingChart = false;
			console.log('Reset');
		} else {
			if(startTimedMode) {
				$('#reset-btn').text('Record');
				request('stop_recording');
				startTimedMode = false;
			} else {
				clear_export_btn();
				$('#reset-btn').text('Stop');
				var timedsec = $('#timed-mode-input').val();
				if (!$.isNumeric(timedsec)) {
					$('#timed-mode-input').val(30);
					timedsec = $('#timed-mode-input').val();
				}
				request('start_recording/' + timedsec);
				console.log("Timed Mode : " + timedsec);
				startTimedMode = true;
			}
		}
	}

	function csvBtn ($btn) {
		//console.log('export csv');
		request('write_to_csv');
		clear_export_btn();
	}

	function prompt_user_to_export_csv () {
		// Use replaceWith to prevent two export buttons to draw simultaneously
		$('#export-csv-div').replaceWith('<div id="export-csv-div"><button type="button" id="export-csv-btn">Export</button></div>');
		$('#export-csv-btn').on('click', csvBtn);
	}

	function clear_export_btn() {
		$('#export-csv-div').replaceWith('<div id="export-csv-div"></div>');
	}

	function clear_recording_buffer() {
		request('clear_recording_buffer');
	}

    function removeTable (sensorName) {
        $('#' + sensorName + '-table').remove();
    }

    function flushAllCharts () {
    	_.forOwn(signalMap, function(frequencyPowerTable, sensorName) {
            if (frequencyPowerTable !== undefined) {
                _(SignalNameEnum.signalTypes).mapValues(function (signalType) {
                    frequencyPowerTable.flushAllCharts(signalType);
                });
            }
        });
    }

    /*
		power_dict format: {"delta":{{"F3":123,"F4":123}},"theta":{},"alpha":{},"beta":{},"gamma":{}}
    */
    function analyze_data (signals) {
        _.forOwn(signalMap, function(frequencyPowerTable, sensorName) {
            if (frequencyPowerTable !== undefined && !flushingChart) {
                _(SignalNameEnum.signalTypes).mapValues(function (signalType) {
                    frequencyPowerTable.handleIncomingSignalUpdate(signalType, signals[signalType.toLowerCase()][sensorName]);
                });
            }
        });
    }
});
