define('SignalNameEnum', function () {
    return {
        left : {
            AF3 : 'AF3',
            F3 : 'F3',
            F7 : 'F7',
            FC5 : 'FC5',
            T7 : 'T7',
            P7 : 'P7',
            O1 : 'O1'
        },
        right : {
            AF4 : 'AF4',
            F4 : 'F4',
            F8 : 'F8',
            FC6 : 'FC6',
            T8 : 'T8',
            P8 : 'P8',
            O2 : 'O2'
        },
        signalTypes : {
            Delta : 'Delta',
            Theta : 'Theta',
            Alpha : 'Alpha',
            Beta : 'Beta',
            Gamma : 'Gamma'
        },

        verifySignal : function (signalName) {
            return this.left.hasOwnProperty(signalName) || this.right.hasOwnProperty(signalName);
        },

        getAllSignals : function () {
            var names = [];
            for (var name in this.left) {
                if (this.hasOwnProperty('left')) {
                    names.push(name);
                }
            }
            for (var name in this.right) {
                if (this.hasOwnProperty('right')) {
                    names.push(name);
                }
            }
            return names;
        }
    };
});