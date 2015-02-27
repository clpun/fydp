define('ImageBankManager', ['jquery', 'lodash', 'Q'], function ($, _, Q) {
    'use strict';

    var IMG_PATH = '/static/images/image_bank/';
    var RETRIEVAL = 'retrieval';

    function ImageBankManager () {
        this.image$divs = [];
        this.imageFileNames = [];
        this.imagesLoaded = false;
        this.encodingImagesGenerated = false;
        this.imageIndicesForEncoding = []; // indices in image$div instance variable
        this.encodingStepFinished = false;
        this.imageIndicesForRetrieval = []; // indices in image$div instance variable
        this.retrievalImagesGenerated = false;
        this.numberOfImagesInSlideShow = 0;
        this.numberOfImagesLoaded = 0;
    }

    ImageBankManager.prototype = {
        loadImages : function () {
            var self = this;
            return Q($.get('/image_bank_contents', function (data, status) {
                if (status === 'success') {
                    data.files.forEach(function (filename, index) {
                        var $imageDiv = $('<div/>').css({
                            position : "fixed",
                            top : 0,
                            bottom : 0,
                            left : 0,
                            right : 0,
                            zIndex : 1031,
                            backgroundSize : "100vw 100vh",
                            backgroundImage : IMG_PATH + filename
                        });
                        $('body').append($imageDiv.hide());
                        self.image$divs.push($imageDiv);
                    });
                    self.imageFileNames = data.files;
                    self.imagesLoaded = true;
                    self.numberOfImagesLoaded = data.files.length;
                    self.numberOfImagesInSlideShow = (data.files.length < 10 ? data.files.length : 10);
                }
            }, 'json'));
        },

        getImageFileNames : function() {
            if (!this.imagesLoaded) {
                console.error('Must first load images, call loadImages()');
                return;
            }
            return this.imageFileNames;
        },

        generateImagesForEncoding : function (imageIndices) {
            if (!this.imagesLoaded) {
                console.error("Must first load images, call loadImages()");
                return;
            }
            if (imageIndices !== undefined) {
                this.imageIndicesForEncoding = imageIndices;
                return;
            }

            for (var i = 0; i < this.numberOfImagesInSlideShow;) {
                var imgIndex = parseInt(Math.random()*100)%this.numberOfImagesLoaded;
                var self = this;
                if (!_(this.imageIndicesForEncoding).contains(imgIndex)) {
                    self.imageIndicesForEncoding.push(imgIndex);
                    i++;
                }
            }
            this.encodingImagesGenerated = true;
        },

        getImagesForList : function(type) {
            if (!this.encodingImagesGenerated || (type === RETRIEVAL && !this.retrievalImagesGenerated)) {
                console.error('Need to perform encoding step first');
                return;
            }
            var imagesList = [];
            var self = this;
            var imagesIndexList;
            if (type === RETRIEVAL)
                imagesIndexList = this.imageIndicesForRetrieval;
            else
                imagesIndexList = this.imageIndicesForEncoding;

            imagesIndexList.forEach(function (index) {
                imagesList.push(self.imageFileNames[index]);
            });
            return imagesList;
        },

        popNextImage$Div : function(type) {
            var nextIndex;
            if (type === RETRIEVAL) {
                if (!this.encodingImagesGenerated || !this.encodingStepFinished) {
                    console.error('Need to perform encoding step first');
                    return;
                }
                nextIndex = this.imageIndicesForRetrieval.shift();
            } else {
                nextIndex = this.imageIndicesForEncoding.shift();
            }
            return this.image$divs[nextIndex];
        },

        generateImagesForRetrieving : function() {
            if (!this.encodingImagesGenerated) {
                console.error('Need to generate images for encoding  first');
                return;
            }
            var numToReplace = this.numberOfImagesInSlideShow/2;
            var replacedIndicesFromEncodingImages = [];
            this.imageIndicesForRetrieval = this.imageIndicesForEncoding.slice();
            var self = this;
            for (var i = 0; i < numToReplace;) {
                var indexToReplace = parseInt(Math.random() * 100) % self.numberOfImagesInSlideShow; // index in imageIndicesForEncoding
                if (!_(replacedIndicesFromEncodingImages).contains(indexToReplace)) { // make sure we don't replace same index twice
                    var indexToReplaceWith = parseInt(Math.random() * 100) % self.numberOfImagesLoaded;
                    // find an index that hasn't been used in the encoding part and isn't in the retrieval set of indices
                    while (_(self.imageIndicesForEncoding).contains(indexToReplaceWith) && _(self.imageIndicesForRetrieval).contains(indexToReplaceWith)) {
                        indexToReplaceWith = parseInt(Math.random() * 100) % self.numberOfImagesInSlideShow;
                    }
                    replacedIndicesFromEncodingImages.push(indexToReplace);
                    self.imageIndicesForRetrieval[indexToReplace] = indexToReplaceWith;
                    i++;
                }
            }
            this.retrievalImagesGenerated = true;
        }
    };

    ImageBankManager.IMG_PATH = IMG_PATH;
    ImageBankManager.RETRIEVAL = RETRIEVAL;

    return ImageBankManager;
});