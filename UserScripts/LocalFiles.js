if (location.pathname.includes('Movies')) {
    var count = 0;
    var markLink = 'http://movie.douban.com/subject_search?search_text=';

    var names = $('a > [data-type="name"]');
    for (var i = 0; i < names.length; i++) {
        var name = names[i];

        ((name) => {
            GM_xmlhttpRequest({
                method: 'GET',
                url: markLink + name.innerText.replace(/\/.+/, ''),

                onload: (data) => {
                    var page = $(data.responseText.replace(/<img[^>]*>/g, ''));
                    $(name).parent().find('[data-type="mark"]')
                           .text(page.find('.rating_nums').first().text());
                    if (++count === names.length) {
                        sort();
                    }
                }
            });
        })(name);
    }

    function sort() {
        var links = $('a');
        links.sort((a, b) => -($(a).find('[data-type="mark"]').text() - $(b).find('[data-type="mark"]').text()));
        links.detach();
        $('.list-group').append(links);
    }
}

else if (location.pathname.includes('News')) {
    var links = $('.list-group-item-info');
    for (i = 0; i < links.length; i++) {
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