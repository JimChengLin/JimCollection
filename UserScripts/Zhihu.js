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
        if (location.pathname === '/') {
            $('.wrap:contains("读读日报")').remove();
        } else if (location.pathname.startsWith('/story')) {
            let target = $('.question:last-child').not(':contains("查看知乎原文")');
            if (target) {
                target.remove();
            }
        }
    });
}

function zhihu() {
    $('<style>@media screen and (max-width:1120px){.zu-top{display:none;}}</style>').appendTo('html');
    $(window).on('copy', () => {
        GM_setClipboard(getSelection().toString(), 'text');
    });

    $(()=> {
        let change = true;
        let observer = new MutationObserver(() => change = true);
        observer.observe(document.querySelector('a'), {childList: true, subtree: true});
        setInterval(() => {
            if (change) {
                $('a.external').map((i, elem) => {
                    let sign = 'link.zhihu.com/?target=';
                    if (elem.href && elem.href.includes(sign)) {
                        elem.href = decodeURIComponent(elem.href.substr(elem.href.indexOf(sign) + sign.length));
                    }
                });
            }
        }, 1000);
    });

    if (location.pathname.endsWith('/topic')) {
        $(window).on('scroll', (event) => {
            $('._hint').remove();
            event.stopImmediatePropagation();
        });
        let day = () => Date.now() / 1000 / 60 / 60 / 24;
        let DayDiff = {
            record: {},
            load: () => {
                for (let url of GM_listValues()) {
                    let diff = day() - GM_getValue(url);
                    DayDiff.record[url] = diff;
                    if (diff > 14) {
                        GM_deleteValue(url);
                    }
                }
            },
            search: (url) => {
                let diff;
                if (url in DayDiff.record) {
                    diff = DayDiff.record[url];
                    if (diff > 14) {
                        GM_setValue(url, day() - 1);
                    }
                } else {
                    diff = 0;
                    GM_setValue(url, day());
                }
                return diff;
            }
        };
        DayDiff.load();

        $(() => {
            let change = true;
            let observer = new MutationObserver(() => change = true);
            observer.observe(document.querySelector('div.zu-main-content'), {childList: true, subtree: true});
            setInterval(() => {
                if (change) {
                    $('.feed-item > link:not(._checked)').map((i, elem) => {
                        elem = $(elem);
                        elem.addClass('_checked');
                        if (DayDiff.search(elem.attr('href')) > 0.5) {
                            elem.closest('.feed-item').find('.expandable, .zm-item-meta').fadeOut();
                        }
                    });
                    change = false;
                }
            }, 1000);
        });
    }
}