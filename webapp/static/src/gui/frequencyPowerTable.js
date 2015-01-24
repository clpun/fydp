define('FrequencyPowerTable', ['jquery', 'SignalNameEnum', 'Chart', 'lodash'], function ($, SignalNameEnum, Chart, _) {
    function FrequencyPowerTable(signalName) {
        if (!SignalNameEnum.verifySignal(signalName)) {
            console.error('Signal name invalid: ' + signalName);
            return null;
        }
        this.signalName = signalName;
        this.deltaPower = null;
        this.deltaSignal = null;
        this.thetaPower = null;
        this.thetaSignal = null;
        this.alphaPower = null;
        this.alphaSignal = null;
        this.betaPower = null;
        this.betaSignal = null;
        this.gammaPower = null;
        this.gammaSignal = null;
    }

    FrequencyPowerTable.prototype = {

        toHtmlTable : function() {
            var html = $('<div/>', {
                id : this.signalName + '-table',
                class : 'row'
            });
            var tableContainer = $('<div class="col-md-4"><h3>' + this.signalName + '</h3></div>');
            var table = $('<table class="table table-bordered"/>');
            var row = $('<tr/>')
                    .append('<th>Frequency</th>')
                    .append('<th>Power</th>')
                    .append('<th>Power Graph</th>');
            table.append(row);

            var self = this;
            _(SignalNameEnum.signalTypes).mapValues(function(signalType) {
                row = $('<tr/>')
                    .append('<td>' + signalType + '</td>')
                    .append('<td>' + self.getPowerForSignalType(signalType) + '</td>')
                    .append('<td><div class="row"><canvas id="' + signalType + self.signalName + '" width="200" height="200"></canvas></div></td>');
                self.createGraph(row.find('canvas'));
                table.append(row);
            });
            return html.append(tableContainer.append(table));
        },

        createGraph : function (canvas) {
            var dataArray = [0, 0];
            var lineChartData = {
                labels : ['0', '1'],
                datasets : [{
                    fillColor: "rgba(151,187,205,0.2)",
                    strokeColor: "rgba(151,187,205,1)",
                    pointColor: "rgba(151,187,205,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(151,187,205,1)",
                    data: dataArray
                }]
            };
            var ctx = canvas[0].getContext("2d");
            canvas.data('chart', new Chart(ctx).Line(lineChartData, {
                responsive: false,
                bezierCurve: false,
                datasetFill: false,
                pointDot: false,
                animation: true,
                animationSteps: 60
            }));
        },

        getPowerForSignalType : function (signalType) {
            return this[signalType.toLowerCase() + 'Power'];
        },

        getSignalForType : function (signalType) {
            return this[signalType.toLowerCase() + 'Signal'];
        }
    };

    return FrequencyPowerTable;
});