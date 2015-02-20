define('ContactQuality', ['jquery', 'SignalNameEnum', 'lodash'], function ($, SignalNameEnum, _) {
    var allSignalNames = SignalNameEnum.getAllSignals();
    function ContactQuality() {
        /*
            baseImageWidth = 560.0
            baseImageHeight = 552.0
            O2 : 440 321
            O1 : 440 170
            P7 : 367 91
            P8 : 367 401
            T7 : 262 57
            T8 : 265 437
            FC5 : 218 112
            FC6 : 216 379
            F3 : 188 170
            F4 : 188 320
            F7 : 144 98
            F8 : 144 393
            AF3 : 130 199
            AF4 : 130 292
        */
        var baseImageWidth = 560.0;
        var baseImageHeight = 552.0;
        var currentDimention = 200.0;
        for (var name in allSignalNames) {
            self[allSignalNames[name] + 'contactQuality'] = 0;
            if (allSignalNames[name] == 'AF3') self[allSignalNames[name]+'position'] = [130.0*currentDimention/baseImageHeight - 2,199.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'AF4') self[allSignalNames[name]+'position'] = [130.0*currentDimention/baseImageHeight - 2,292.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'F3') self[allSignalNames[name]+'position'] = [188.0*currentDimention/baseImageHeight - 2,170.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'F4') self[allSignalNames[name]+'position'] = [188.0*currentDimention/baseImageHeight - 2,320.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'F7') self[allSignalNames[name]+'position'] = [144.0*currentDimention/baseImageHeight - 2,98.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'F8') self[allSignalNames[name]+'position'] = [144.0*currentDimention/baseImageHeight - 2,393.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'FC5') self[allSignalNames[name]+'position'] = [218.0*currentDimention/baseImageHeight - 2,112.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'FC6') self[allSignalNames[name]+'position'] = [216.0*currentDimention/baseImageHeight - 2,379.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'T7') self[allSignalNames[name]+'position'] = [262.0*currentDimention/baseImageHeight - 2,57.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'T8') self[allSignalNames[name]+'position'] = [265.0*currentDimention/baseImageHeight - 2,437.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'P7') self[allSignalNames[name]+'position'] = [367.0*currentDimention/baseImageHeight - 2,91.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'P8') self[allSignalNames[name]+'position'] = [367.0*currentDimention/baseImageHeight - 2,401.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'O1') self[allSignalNames[name]+'position'] = [440.0*currentDimention/baseImageHeight - 2,170.0*currentDimention/baseImageWidth - 2];
            else if (allSignalNames[name] == 'O2') self[allSignalNames[name]+'position'] = [440.0*currentDimention/baseImageHeight - 2,321.0*currentDimention/baseImageWidth - 2];
        }
    }

    ContactQuality.prototype = {

        createBaseImage : function() {
            return '<div id="contact-quality-container"><div id="contact-quality-base-image"></div></div>';
            //return '<div id="contact-quality-base-image"></div>';
        },

        createContactQualityLabels : function() {
            var string = "";
            for (var name in allSignalNames) {
                string += '<div class="_0" id="' + allSignalNames[name] + 'contactQuality"></div>';
            }
            return string;
        },

        getChannelQuality : function (signalType) {
            return self[signalType + 'contactQuality'];
        },

        getLabelPosition : function (signalType) {
            return (self[signalType + 'position']);
        },

        getNameForChannel : function (signalType) {
            return (signalType + 'contactQuality');
        },

        handleIncomingSignalUpdate : function (signalType, value) {
            var label = $('#'+signalType+'contactQuality');
            if(label.hasClass('_'+value)){
                //
            } else {
                label.removeClass();
                if(value > 5) value = '5';
                label.addClass('_'+value);
            }
        },
    };
    return ContactQuality;
});