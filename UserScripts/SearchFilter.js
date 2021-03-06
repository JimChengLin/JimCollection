'use strict';

main();
function main() {
    var href = location.href;
    var mapMain = {};
    var mapBackup = {};

    var update;
    var setting;
    var isEngine;
    if (isEngine = (href.includes('google') && href.includes('q='))) {
        setting = {childList: true, subtree: true};
        update = function () {
            var rc = $('.srg > .g > .rc');
            var links = rc.find('.r > a');
            var abstracts = rc.find('.s .st');
            for (var i = 0; i < links.length; i += 1) {
                var link = links[i];
                if (link.hasAttribute('onmousedown')) {
                    link.removeAttribute('onmousedown');
                }

                var abstract = $(abstracts[i]);
                mapMain[link] = abstract.find('span').length ? '' : '-';
                mapMain[link] += abstract.text();

                var emList = abstract.find('em');
                mapBackup[link] = emList.length ?
                    '-' + emList.first().text() + '...' + emList.last().text() : extract(mapMain[link]);
            }
        };
    }

    function commit() {
        update();
        GM_setValue('mapMain', JSON.stringify(mapMain));
        GM_setValue('mapBackup', JSON.stringify(mapBackup));
    }

    if (isEngine) {
        commit();
        var change;
        var observer = new MutationObserver(() => change = true);
        observer.observe(document.body, setting);
        setInterval(() => {
            if (change) {
                commit();
                change = false;
            }
        }, 1000);
    }

    else if (top === self) {
        var record = GM_getValue('mapMain');
        if (record) {
            mapMain = JSON.parse(record);
            mapBackup = JSON.parse(GM_getValue('mapBackup'));
        }
        var hrefHttp = href.replace('https:', 'http:');
        var hrefHttps = hrefHttp.replace('http:', 'https:');
        $(() => {
            for (var map of [mapMain, mapBackup]) {
                for (var sign of [hrefHttp, hrefHttps]) {
                    if (sign in map && clean(map[sign])) {
                        return;
                    }
                }
            }
        });
    }
}

function clean(abstract) {
    var marks = abstract
        .substr(abstract.indexOf('-') + 1)
        .split('...')
        .map(purify)
        .filter(Boolean);

    var open = xPath(findElement(marks.shift()));
    if (marks.length) {
        var close = xPath(findElement(marks.pop()));
    }

    var path = open && close && (open !== close) ? intersection(open, close) : open || close;
    if (!path) {
        return false;
    }
    path = estimate(path);

    var element = document.evaluate(path).iterateNext();
    if (enoughText(element)) {
        element.scrollIntoView();
        return true;
    }
}

function findElement(mark) {
    var result = null;

    function travel(element) {
        var children = element.children;
        for (var i = 0; i < children.length; i++) {
            var child = children[i];
            travel(child);
        }

        if (result === null &&
            element.tagName.search(/(SCRIPT|STYLE)/) === -1 && purify(getText(element)).includes(mark)) {
            result = element;
        }
    }

    travel(document.body);
    return result;
}

function xPath(node) {
    if (!(node && node.nodeType === 1)) {
        return '';
    }

    var count = 0;
    var siblings = node.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {
        var sibling = siblings[i];
        if (sibling.tagName === node.tagName) {
            count += 1;
        }
        if (sibling === node) {
            break;
        }
    }

    var suffix = count > 1 ? '[' + count + ']' : '';
    return xPath(node.parentNode) + '/' + node.tagName + suffix;
}

function purify(text) {
    return text.replace(/[^a-zA-Z\u4E00-\u9FFF]/g, '').toLowerCase();
}

function extract(abstract) {
    var marks = abstract
        .split(/[^a-zA-Z\u4E00-\u9FFF]/)
        .sort((a, b) => a.length - b.length);
    return '-' + marks.pop() + '...' + marks.pop();
}

function intersection(a, b) {
    var big, small;
    if (a.length > b.length) {
        big = a;
        small = b;
    } else {
        big = b;
        small = a;
    }

    for (var i = 0; i < small.length; i++) {
        if (small[i] !== big[i]) {
            break;
        }
    }

    small = small.substr(0, i);
    return small.substr(0, small.lastIndexOf('/'));
}

function estimate(xPath) {
    var breakPoints = [];
    var match;
    var re = /(DIV|ARTICLE|SECTION)/g;
    while ((match = re.exec(xPath))) {
        breakPoints.push(match.index);
    }

    if (breakPoints.length === 0) {
        return xPath;
    } else {
        var anchor = breakPoints[Math.round((breakPoints.length - 1) / 3)];
        var close = xPath.indexOf('/', anchor);
        if (close !== -1) {
            return xPath.substr(0, close);
        } else {
            return xPath;
        }
    }
}

function getText(element) {
    if ($(element).is(':visible') && element.innerText) {
        return element.innerText;
    } else {
        return '';
    }
}

function enoughText(element) {
    return purify(getText(element)).length > purify(getText(document.body)).length / 5;
}