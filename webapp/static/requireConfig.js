requirejs.config({
    baseUrl : 'static',
    paths : {
        jquery : 'lib/jquery-2.1.1',
        lodash : 'lib/lodash-2.4.1',
        bootstrap : 'lib/bootstrap',
        Chart : 'lib/Chart',
        socketio : 'lib/socket.io',
        webSocket : 'src/webSocket',
        main : 'src/main',
        Streamer : 'src/streaming/streamer',
        SignalNameEnum : 'src/gui/signalNameEnum',
        FrequencyPowerTable : 'src/gui/frequencyPowerTable'
    },
    shim : {
        "bootstrap" : {
            deps : ['jquery'],
            exports : 'Bootstrap'
        },
        "socketio" : {
            exports : 'io'
        }
    }
});

var pathname = window.location.pathname;
if (pathname.indexOf('/webSoc') !== -1)
    requirejs(['webSocket']);
else {
    requirejs(['main']);
}