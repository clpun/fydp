require(['jquery', 'lodash'], function ($, _) {
    var BLANK = 'blank';
    var IMG_PATH = '/static/images/image_bank/';
    var images = [];
    var images_for_encoding = [];
    var indices_of_images_for_encoding = []; // indices from images array
    var num_images_to_present;
    var presentation_queue = [];
    var $imageScreen = $('<div id="image-screen" style="position:fixed;top: 0;bottom:0;left:0;right:0;z-index:1031;background-size: 100vw 100vh;"/>');
    $('body').append($imageScreen.hide());

    $('#encoding-btn').click(function () {
        $.get('/image_bank_contents', function (data, status) {
            if (status === 'success') {
                clearImageInfo();
                images = data.files;
                num_images_to_present = images.length < 10 ? images.length : 10;
                generateList();
                presentImages(images_for_encoding);
                replaceHalf(images_for_encoding);
            }
        }, 'json');
    });

    $('#retrieval-btn').click(function () {
        presentImages(images_for_encoding);
    });

    function generateList () {
        var img_index, i = 0;
        while (i < num_images_to_present) {
            img_index = parseInt(Math.random() * 100) % images.length;
            if (!_(indices_of_images_for_encoding).contains(img_index)) {
                indices_of_images_for_encoding[i] = img_index;
                images_for_encoding[i] = images[indices_of_images_for_encoding[i]];
                i++;
            }
        }
    }

    function replaceHalf(images_to_replace) {
        var num_to_replace = images_to_replace.length/2;
        var replaced_indices = [];
        for (var i = 0; i < num_to_replace;) {
            var index_to_replace = parseInt(Math.random() * 100)%num_to_replace;
            if (!_(replaced_indices).contains(index_to_replace)) {
                var index_to_replace_with = parseInt(Math.random() * 100) % images.length;
                if (!_(indices_of_images_for_encoding).contains(index_to_replace_with)) {
                    images_to_replace[index_to_replace] = images[index_to_replace_with];
                    indices_of_images_for_encoding.push(index_to_replace_with);
                    i++;
                }
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

    function clearImageInfo() {
        images = [];
        images_for_encoding = [];
        indices_of_images_for_encoding = [];
        num_images_to_present;
        presentation_queue = [];
    }
});