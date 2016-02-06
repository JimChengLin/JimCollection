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
            if (link.href.includes(sign)) {
                link.href = decodeURIComponent(link.href.substr(link.href.indexOf(sign) + sign.length));
            }
        });
}