'use strict';

if (location.pathname.startsWith('/story')) {
    $(() => {
        $('.question:last-child').not(':contains("查看知乎原文")').remove();
    });
} else {
    $('<style>@media screen and (max-width: 1120px){.zu-top{display:none;}}</style>').appendTo('html');
    $(window)
        .on('copy', () => {
            GM_setClipboard(getSelection().toString(), 'text');
        })
        .on('click', (event) => {
            var link = event.target;
            if (link.parentElement && link.parentElement.tagName === 'A') {
                link = link.parentElement;
            }
            const sign = 'link.zhihu.com/?target=';
            if (link.href && link.href.includes(sign)) {
                link.href = decodeURIComponent(link.href.substr(link.href.indexOf(sign) + sign.length));
            }
        });

    if (location.pathname.endsWith('/topic')) {
        $(ZhihuFilter);
    }
}

function ZhihuFilter() {
    const DAY_NOW = Math.round(Date.now() / 60 / 60 / 24);

    var dayDiff = {
        init: () => {
            this.record = {};
            for (let url of GM_listValues()) {
                let diff = DAY_NOW - GM_getValue(url);
                diff > 21 ? GM_deleteValue(url) : this.record[url] = diff;
            }
        },

        search: (url) => {
            if (url in this.record) {
                return this.record[url];
            } else {
                GM_setValue(url, DAY_NOW);
                return this.record[url] = 0;
            }
        }
    };
    dayDiff.init();

    var change;
    var observer = new MutationObserver(() => change = true);
    observer.observe(document.body, {childList: true, subtree: true});

    setInterval(() => {
        if (change) {
            $('.question_link').map((i, element)=> {
                element = $(element);
                if (dayDiff.search(element.attr('href')) > 7) {
                    return element.hide();
                }
                let item = element.closest('.feed-item');
                let link = item.find('link');
                if (link) {
                    if (dayDiff.search(link.attr('href')) > 1) {
                        element.hide();
                    }
                }
            });
            change = false;
        }
    }, 1000);
}