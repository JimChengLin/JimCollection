'use strict';

$(() => {
    $('iframe').remove();
    if (!location.href.includes('comment')) {
        var node = $('.ep-content-main');
        node.add(node.parentsUntil(document.body)).siblings().hide();
        node.find('.ep-share-tip, .ep-share-top, .ep-icon-tie')
            .add(node.find('.end-text:last').nextAll())
            .remove();
    } else {
        node = $('#hotReplies');
        node.add(node.parentsUntil(document.body)).siblings().remove();
    }
});