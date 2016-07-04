$('<style>@media screen and (max-width:1120px){.zu-top{display:none;}}</style>').appendTo('html');
$(window)
    .on('copy', () => {
        GM_setClipboard(getSelection().toString(), 'text');
    })
    .on('click', (event) => {
        var link = event.target;
        if (link.parentElement && link.parentElement.tagName === 'A') {
            link = link.parentElement;
        }
        var sign = 'link.zhihu.com/?target=';
        if (link.href && link.href.includes(sign)) {
            link.href = decodeURIComponent(link.href.substr(link.href.indexOf(sign) + sign.length));
        }
    });