'use strict';

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
    $(()=> {
        const DAY_NOW = Math.round(Date.now() / 1000 / 60 / 60 / 24);
        const dayDiff = {
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

        let change;
        const observer = new MutationObserver(() => change = true);
        observer.observe(document.querySelector('div.zu-main-content > div'), {childList: true, subtree: true});

        setInterval(() => {
            if (change) {
                $('.question_link').map((i, element) => {
                    element = $(element);
                    let item = element.closest('.feed-item');
                    if (dayDiff.search(element.attr('href')) > 7 ||
                        dayDiff.search(item.find('link').attr('href')) > 1) {
                        item.remove();
                    }
                });
                change = false;
            }
        }, 1000);
    });
}