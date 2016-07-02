if (location.pathname.includes('News')) {
    var links = $('.list-group-item-info');
    for (var i = 0; i < links.length; i++) {
        var link = links[i];

        if (link.innerText.search(/·|？/) === -1) {
            ((link) => {
                GM_xmlhttpRequest({
                    method: 'GET',
                    url: link.href,

                    onload: (data) => {
                        var page = $(data.responseText.replace(/<img[^>]*>/g, ''));
                        var titles = page.find('.question-title').filter((i, elem) => elem.innerText);
                        titles.length === 1 && titles.text().includes('？') ? link.text = titles.text() : link.text += '✓';
                    }
                });
            })(link);
        }
    }
}