'use strict';

switch (location.host) {
    case 'daily.zhihu.com':
        zhihuDaily();
        break;
    case 'www.zhihu.com':
        zhihu();
        break;
}

function zhihuDaily() {
    $(() => {
        if (location.pathname.startsWith('/story')) {
            $('.question:last-child').not(':contains("查看知乎原文")').remove();
        }
    });
}

function zhihu() {
    $('<style>@media screen and (max-width:1120px){.zu-top{display:none;}}</style>').appendTo('html');
    $(window)
        .on('copy', () => {
            GM_setClipboard(getSelection().toString(), 'text');
        })
        .on('click', (event) => {
            let link = event.target;
            if (link.parentElement && link.parentElement.tagName === 'A') {
                link = link.parentElement;
            }
            const sign = 'link.zhihu.com/?target=';
            if (link.href && link.href.includes(sign)) {
                link.href = decodeURIComponent(link.href.substr(link.href.indexOf(sign) + sign.length));
            }
        });

    if (location.pathname.endsWith('/topic')) {
        $(window).on('scroll', (event)=> {
            event.stopImmediatePropagation();
        });

        $(()=> {
            const DAY_NOW = Math.round(Date.now() / 1000 / 60 / 60 / 24);
            const DayDiff = {
                record: {},
                load: () => {
                    for (let url of GM_listValues()) {
                        let diff = DAY_NOW - GM_getValue(url);
                        diff > 14 ? GM_deleteValue(url) : DayDiff.record[url] = diff;
                    }
                },
                search: (url) => {
                    url = url.match(/[0-9]+/).pop();
                    if (url in DayDiff.record) {
                        return DayDiff.record[url];
                    } else {
                        GM_setValue(url, DAY_NOW);
                        DayDiff.record[url] = 0;
                        return 0;
                    }
                }
            };
            DayDiff.load();

            let change;
            const observer = new MutationObserver(() => change = true);
            observer.observe(document.querySelector('div.zu-main-content'), {childList: true, subtree: true});

            setInterval(() => {
                if (change) {
                    $('.question_link').map((i, elem) => {
                        elem = $(elem);
                        let item = elem.closest('.feed-item');
                        if (DayDiff.search(elem.attr('href')) >= 7 ||
                            DayDiff.search(item.find('link').attr('href')) >= 1) {
                            item.fadeOut();
                        }
                    });
                    change = false;
                }
            }, 1000);
        });
    }
}