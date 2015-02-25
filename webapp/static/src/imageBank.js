require(['jquery'], function($) {
    var images = [];
    var images_to_show = [];

    $.get('/image_bank_contents', function(data, status) {
        if (status === 'success') {
            images = data.filenames;
        }
    }, 'json');

    for (var i = 0; i < (images.length < 10 ? images.length : 10); i++) {
        images_to_show.append(
            images[i]
        );
    }
});