require(['jquery', 'Streamer', 'FrequencyPowerTable', 'SignalNameEnum', 'bootstrap', 'Chart'], function ($, Streamer, FrequencyPowerTable, SignalNameEnum) {
    var fpt;
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
    });

    function createDummyChartData(fpt) {
        for (var i = 0; i < 20; i++)
            fpt.handleIncomingSignalUpdate(SignalNameEnum.signalTypes.Alpha, Math.floor(Math.random() * 100))
    }

    function removeTable (classSelected) {
        var classToRemove = classSelected.attr('id');
        $('#' + classToRemove + '-table').remove();
    }
});

