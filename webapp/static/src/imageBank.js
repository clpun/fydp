require(['jquery', 'lodash', 'ImageBankManager'], function ($, _, ImageBankManager) {
    var $blankDiv = $('<div class="slideshow-image">').css({
        position : "fixed",
        top : 0,
        bottom : 0,
        left : 0,
        right : 0,
        zIndex : 1031,
        backgroundSize : "100vw 100vh",
        backgroundColor : '#000'
    }).attr('tabindex', -1);
    var presentation_queue = [];
    var imageBankManager = new ImageBankManager();
    var $encodingButton = $('#encoding-btn');
    var $retrievalButton = $('#retrieval-btn');
    var $body = $('body');

    $body.append($blankDiv.hide());

    $encodingButton.attr('disabled', 'disabled');
    $retrievalButton.attr('disabled', 'disabled');

    imageBankManager.loadImages().then(function () {
        $('#encoding-btn').removeAttr('disabled');
        $('#retrieval-btn').removeAttr('disabled');

    });

    $encodingButton.click(function () {
        presentation_queue = [];
        imageBankManager.generateImagesForEncoding();
        pushImage($blankDiv, 3);
        for (var i = 0; i < imageBankManager.numberOfImagesInSlideShow; i++) {
            pushImage(imageBankManager.popNextImage$Div(), 5);
            pushImage($blankDiv, 2);
        }
        runPresentation();
    });

    $retrievalButton.click(function () {
        presentation_queue = [];
        imageBankManager.generateImagesForRetrieval();
        pushImage($blankDiv, 3);
        for (var i = 0; i < imageBankManager.numberOfImagesInSlideShow; i++) {
            pushImage(imageBankManager.popNextImage$Div(ImageBankManager.RETRIEVAL), 5);
            pushImage($blankDiv, 2);
        }
        runPresentation();
    });

    function pushImage ($img, seconds) {
        presentation_queue.push({$img : $img, time : seconds * 1000});
    }

    function runPresentation () {
        if (presentation_queue.length === 0) {
            return;
        }
        var currentOptions = presentation_queue.shift();
        currentOptions.$img.show();
        setTimeout(function () {
            currentOptions.$img.hide();
            runPresentation();
        }, currentOptions.time);
    }
});