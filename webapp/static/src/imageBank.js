require(['jquery', 'lodash'], function ($, _) {
    var BLANK = 'blank';
    var IMG_PATH = '/static/images/image_bank/';
    var images = [];
    var images_for_encoding = [];
    var images_for_encoding_indices = []; // indices from images array
    var num_images_to_present;
    var presentation_queue = [];
    var $imageScreen = $('<div id="image-screen" style="position:fixed;top: 0;bottom:0;left:0;right:0;z-index:1031;"/>');
    $('body').append($imageScreen.hide());

    $('#encoding-btn').click(function () {
        $.get('/image_bank_contents', function (data, status) {
            if (status === 'success') {
                images = data.files;
                num_images_to_present = images.length < 10 ? images.length : 10;
                generateList();
                presentImages(images_for_encoding);
            }
        }, 'json');
    });

    function generateList () {

        var img_index, i = 0;
        while (i < num_images_to_present) {
            img_index = parseInt(Math.random() * 100) % images.length;
            if (!_(images_for_encoding_indices).contains(img_index)) {
                images_for_encoding_indices[i] = img_index;
                images_for_encoding[i] = images[images_for_encoding_indices[i]];
                i++;
            }
        }
    }

    function presentImages(imagesToPresent) {
        pushImage(BLANK, 3);
        for (var index in imagesToPresent) {
            pushImage(imagesToPresent[index], 5);
            pushImage(BLANK, 2);
        }
        runPresentation();
    }

    function pushImage(img, seconds) {
        var style = {};
        if (img === BLANK) {
            style['background-image'] = 'none';
            style['background-color'] = '#000';
        } else {
            style['background-image'] = 'url("' + IMG_PATH + img + '")';
            style['background-color'] = 'none';
        }
        presentation_queue.push({style:style, time: seconds*1000});
    }

    function runPresentation () {
        if (presentation_queue.length === 0)
            return;

        var options = presentation_queue.shift();
        $imageScreen.css('background-color', '');
        $imageScreen.css('background-image', '');
        $imageScreen.css(options.style);
        $imageScreen.show();
        setTimeout(function() {
            $imageScreen.hide();
            runPresentation();
        }, options.time);
    }

    function clear() {
        images_for_encoding_indices = [];
        images_for_encoding = [];
    }
});