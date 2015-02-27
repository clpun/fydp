requirejs.config({
    baseUrl : 'static',
    paths : {
        jquery : 'lib/jquery-2.1.1',
        lodash : 'lib/lodash-2.4.1',
        bootstrap : 'lib/bootstrap',
        Chart : 'lib/Chart',
        socketio : 'lib/socket.io',
        Q : 'lib/q',
        webSocket : 'src/webSocket',
        main : 'src/main',
        Streamer : 'src/streaming/streamer',
        SignalNameEnum : 'src/gui/signalNameEnum',
        FrequencyPowerTable : 'src/gui/frequencyPowerTable',
        ContactQuality : 'src/gui/contactQuality',
        imageBank : 'src/imageBank',
        ImageBankManager : 'src/imageBankComponents/imageBankManager',
        ImageBankManagerUnitTest : 'src/imageBankComponents/imageBankManagerUnitTest'
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
else if (pathname.indexOf('/image_bank') !== -1) {
    if (window.location.hash === '#test')
        requirejs(['ImageBankManagerUnitTest']);
    else
        requirejs(['imageBank']);
} else
    requirejs(['main']);