define('ImageBankManagerUnitTest', ['ImageBankManager', 'jquery', 'lodash'], function (ImageBankManager, $, _) {
    var imageBankManager = new ImageBankManager();
    imageBankManager.loadImages().then(function () {
        var imageFileNames = imageBankManager.getImageFileNames();

        // can generate random images
        imageBankManager.generateImagesForEncoding();
        var imagesForEncoding = imageBankManager.getImagesForList();
        if (imageFileNames.length > 10) {
            console.assert(imagesForEncoding.length === 10, 'Wrong number of images were generated for encoding');
            console.assert(_.uniq(imagesForEncoding).length === 10, 'There were duplicate values in imagesForEncoding');
        } else {
            console.error('Less than 10 images loaded');
            return;
        }

        // can replace half of the images for retrieval
        imageBankManager.generateImagesForRetrieval();
        var imagesForRetrieving = imageBankManager.getImagesForList(ImageBankManager.RETRIEVAL);
        console.assert(imagesForEncoding.length === imagesForRetrieving.length, 'Wrong number of images were generated for retrieval');
        console.assert(_.uniq(imagesForRetrieving).length === 10, 'There were duplicate values in imagesForRetrieving');
        var sameIndicesCount = 0, differentIndicesCount = 0;
        for (var i = 0; i < imagesForRetrieving.length; i++) {
            if (imagesForEncoding[i] === imagesForRetrieving[i])
                sameIndicesCount++;
            else
                differentIndicesCount++;
        }
        console.assert(sameIndicesCount === 5, 'Wrong number for same indices');
        console.assert(sameIndicesCount === differentIndicesCount, 'Number of same indices is different thank the number of different indices');

        console.log('finished unit test');
    });

});