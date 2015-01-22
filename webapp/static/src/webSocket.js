require(['jquery', 'Streamer'], function ($, Streamer) {
    $(document).ready(function() {
        var streamer = new Streamer();
        streamer.connect();
        streamer.request('val');

        var receivedValue = $('#receivedValue');
        $('body').on('bufferUpdated', function () {
            var value = streamer.consumeData();
            while (value != undefined) {
                receivedValue.text(value);
                console.log(value);
                value = streamer.consumeData();
            }
        });
    });
});