define('Streamer', ['jquery', 'socketio'], function ($, io) {
    function Streamer() {}

    Streamer.prototype = {
        connecting : false,
        connected : false,
        socket : null,
        buffer : [],
        _bufferLock : false,
        connectedCallback : undefined,

        connect : function () {
            this.socket = io.connect('http://' + document.domain + ':' + location.port + '/api');
            var self = this;
            this.connecting = true;
            self.connected = true;
            this.socket.on('response', function(resp) {
                while (self._bufferLock);
                self._bufferLock = true;
                if (resp.data instanceof Array) {
                    resp.data.forEach(function (val) {
                        self.buffer.push(val);
                    });
                } else {
                    self.buffer.push(resp.data);
                }
                self._bufferLock = false;
                $('body').trigger('bufferUpdated');
            });
            this.socket.on('disconnect', function() {
                alert('socket disconnected');
                self.connect();
            });
            //console.log('connected from streamer = ' + self.connected);
        },

        request : function (eventName, req) {
            if (!this.connected) return;
            console.log('requesting data');
            this.socket.emit(eventName, {data: req});
        },

        stop : function () {
            this.socket.disconnect();
        },

        consumeData : function () {
            if (!this.connected) return;

            return this.buffer.shift();
        }

    };

    return Streamer;
});