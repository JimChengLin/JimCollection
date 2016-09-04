'use strict';

// Hook
Element.prototype._addEventListener = Element.prototype.addEventListener;
Element.prototype.addEventListener = function (type, listener, userCapture) {
    this._addEventListener(type, listener, userCapture);
    if (this.tagName === 'DIV' && type.match(/(mousedown|mouseup|click)/)) {
        Page.clickElements.push(this);
    }
};

// Event
$(window)
    .on('click resize scroll', () => Page.escape())
    .on('click', (event) => Page.target = event.target);

var counter = 0;
var shouldBlur = true;
var interval = setInterval(() => {
    if (shouldBlur && counter < 1000 && !Page.target) {
        counter++;
        document.activeElement && document.activeElement.blur && document.activeElement.blur();
    } else {
        clearInterval(interval);
    }
}, 10);

$(() => {
    $('input, textarea').map((i, elem) => {
        elem._focus = elem.focus;
        elem.focus = $.noop;
    });
});

window ? register() : setTimeout(register);
function register() {
    addEventListener('keydown', (event) => {
        var isTab = (event.code === 'Tab');
        var isCommand = Page.isCommand(event);

        if (isTab && !doDefaultTab()) {
            event.preventDefault();
            event.stopImmediatePropagation();
            isCommand ? Page.escape() : document.activeElement.blur();
            document.body.click();
        } else if (isCommand) {
            event.stopImmediatePropagation();
        }

        function doDefaultTab() {
            return document.activeElement.tagName === 'INPUT' &&
                (!document.activeElement.type || document.activeElement.type === 'text') &&
                $(document.activeElement).closest('form').find('input[type="password"]').length;
        }
    }, true);

    addEventListener('keyup', (event) => {
        if (Page.isCommand(event)) {
            event.stopImmediatePropagation();
        }
    }, true);

    addEventListener('keypress', (event) => {
        if (Page.isCommand(event)) {
            event.preventDefault();
            event.stopImmediatePropagation();

            var char = String.fromCharCode(event.keyCode).toUpperCase();
            switch (char) {
                case 'F':
                    $('._hint').length ? Page.match(char) : Page.linkHint();
                    break;

                case 'J':
                    Page.scrollTop(200);
                    break;

                case 'K':
                    Page.scrollTop(-200);
                    break;

                case ' ':
                    Page.plus();
                    break;

                default:
                    Page.match(char);
            }
        }
    }, true);
}

$(`<style>
._click{box-shadow: inset 0 0 3px 0 black}
._plus{font-weight: bold}
._hint{
    background-color: rgba(173, 216, 230, 0.7);
    border-radius: 3px;
    box-shadow: 0 0 2px;
    color: black;
    font-family: consolas;
    font-size: 13px;
    position: fixed;
    z-index: 2147483648;
}</style>`).appendTo('html');

var Page = {
    target: null,
    clickElements: [],

    chars: '',
    hintMap: {},
    isPlus: false,

    linkHint: () => {
        Page.escape();

        var elements = getElements();
        var hints = getHints(elements);
        Page.hintMap = popupHints(elements, hints);

        function getElements() {
            var elements = $('a, button, select, input, textarea, [role="button"], [contenteditable], [onclick]');
            var clickElements = $(Page.clickElements);
            return purify(elements, clickElements.add(clickElements.find('div')));

            function purify(elements, clickElements) {
                const length = 16;

                function isDisplayed(element, isClickable) {
                    var style = getComputedStyle(element);
                    if (style.opacity === '0' || (isClickable && style.cursor.search(/pointer|default/) === -1)) {
                        return;
                    }

                    var rect = element.getClientRects()[0];
                    if (rect && rect.left >= 0 && rect.top >= 0 &&
                        rect.right <= innerWidth && rect.bottom <= innerHeight) {

                        element._left = rect.left;
                        element._top = rect.top;
                        var positions = [[element._left + 1, element._top + 1], [
                            Math.min(element._left + rect.width - 1, element._left + length),
                            Math.min(element._top + rect.height - 1, element._top + length)]];

                        for (i = 0; i < positions.length; i++) {
                            var targetElement = document.elementFromPoint(positions[i][0], positions[i][1]);
                            if (targetElement === element || element.contains(targetElement)) {
                                return true;
                            }
                        }
                    }
                }

                elements = elements.filter((i, elem) => isDisplayed(elem));
                clickElements = clickElements.filter((i, elem) => isDisplayed(elem, 'clickable'));

                var xTree = Tree.create(0, innerWidth);
                var yTree = Tree.create(0, innerHeight);

                elements = elements.get().reverse().filter(isExclusive);
                clickElements = clickElements.get().reverse().filter(isExclusive);

                function isExclusive(element) {
                    var overlapsX = $();
                    var overlapsY = $();

                    var leftTo = Math.min(element._left + length, xTree.to);
                    var topTo = Math.min(element._top + length, yTree.to);
                    Tree.search(xTree, element._left, leftTo, x => overlapsX = overlapsX.add(x));
                    Tree.search(yTree, element._top, topTo, y => overlapsY = overlapsY.add(y));

                    if (overlapsX.filter(overlapsY).length === 0) {
                        Tree.insert(xTree, element._left, leftTo, element);
                        Tree.insert(yTree, element._top, topTo, element);

                        overlapsY.map((i, elem) => {
                            if (Math.abs(element._top - elem._top) <= 5 &&
                                Math.abs(element._left - elem._left) <= innerWidth / 10) {
                                element._top = elem._top;
                                return false;
                            }
                        });
                        return true;
                    }
                }

                return $(elements).add(clickElements);
            }
        }

        function getHints(elements) {
            var hints = [];
            var Y = 'ABCDEGHILM';
            var X = '1234567890';
            var B = 'NOPQRSTUVWXYZ' + Y + X;
            var lengthB = B.length;

            var all = {};
            for (var i = 0; i < B.length; i++) {
                all[B.charAt(i)] = B;
            }

            for (i = 0; i < elements.length; i++) {
                var element = elements[i];

                var y = Y.charAt(Math.round(element._top / innerHeight * (Y.length - 1)));
                var x = X.charAt(Math.round(element._left / innerWidth * (X.length - 1)));

                if (all[y].length === 0) {
                    y = B.charAt(0);
                }
                if (!all[y].includes(x)) {
                    x = all[y].charAt(0);
                }

                all[y] = all[y].replace(x, '');
                if (all[y] === '') {
                    B = B.replace(y, '');
                }

                hints.splice(Math.round(hints.length * 0.618 % 1 * hints.length), 0, y + x);
            }

            var availableChars = [];
            var singletonChars = [];
            for (i = 0; i < B.length; i++) {
                var char = B.charAt(i);
                if (all[char].length === lengthB) {
                    availableChars.push(char);
                } else if (all[char].length === lengthB - 1) {
                    singletonChars.push(char);
                }
            }

            for (i = 0; i < hints.length; i++) {
                var startChar = hints[i].charAt(0);
                if (singletonChars.includes(startChar)) {
                    hints[i] = startChar;
                } else if (availableChars.length) {
                    hints[i] = availableChars.pop();
                    if ((all[startChar] += '.').length === lengthB - 1) {
                        singletonChars.push(startChar);
                    }
                }
            }

            var singletonChar;
            var availableChar = 'F';
            for (i = 0; i < elements.length && availableChar === 'F'; i++) {
                element = elements[i];

                if ((element.tagName === 'INPUT' &&
                    element.type.search(/(button|checkbox|file|hidden|image|radio|reset|submit)/i) === -1) ||
                    element.hasAttribute('contenteditable') || element.tagName === 'TEXTAREA') {
                    var hint = hints[i];
                    hints[i] = availableChar;
                    availableChar = hint;

                    startChar = hint.charAt(0);
                    if (availableChar.length > 1 && (all[startChar] += '.').length === lengthB - 1) {
                        singletonChar = startChar;
                    }
                }
            }

            for (i = 0; availableChar.length === 1 && i < hints.length; i++) {
                hint = hints[i];
                if (hint.length > 1) {
                    hints[i] = availableChar;
                    availableChar = hint;

                    startChar = hint.charAt(0);
                    if ((all[startChar] += '.').length === lengthB - 1) {
                        singletonChar = startChar;
                    }
                }
            }

            for (i = 0; singletonChar && i < hints.length; i++) {
                if (hints[i].startsWith(singletonChar)) {
                    hints[i] = singletonChar;
                    break;
                }
            }

            return hints;
        }

        function popupHints(elements, hints) {
            var map = {};

            for (var i = 0; i < elements.length; i++) {
                var element = elements[i];
                var hint = hints[i];
                map[hint] = element;

                var style = {
                    top: element._top,
                    left: element._left
                };

                $('<div class="_hint">' + hint + '</div>')
                    .css(style)
                    .appendTo('html');
            }
            return map;
        }
    },

    escape: () => {
        $('._hint').remove();
        Page.chars = '';
        Page.hintMap = {};
        Page.isPlus = false;
    },

    match: (char) => {
        var hints = $('._hint');
        if (hints.length) {
            Page.chars += char;

            var removeElements = [];
            hints = hints.filter((i, element) => {
                if (element.innerText.startsWith(char)) {
                    return element.innerText = element.innerText.substr(-1);
                } else {
                    removeElements.push(element);
                }
            });
            $(removeElements).remove();

            if (hints.length === 1) {
                var element = Page.hintMap[Page.chars];
                element.tagName === 'A' && Page.isPlus ? GM_openInTab(element.href, true) : Page.click(element);

                element = $(element).addClass('_click');
                setTimeout(() => element.removeClass('_click'), 500);
                Page.escape();
            }
        }
    },

    scrollTop: (offset) => {
        var target = $(((Page.target instanceof HTMLElement) && Page.target) || 'div');
        var targets = target.add(target.parentsUntil('body'))
                            .filter((i, elem) =>
                            elem.scrollHeight >= elem.clientHeight && getComputedStyle(elem).overflow !== 'hidden');

        for (var i = 0; i < targets.length; i++) {
            target = targets[i];
            var result = (target.scrollTop += offset);
            if (result !== offset) {
                Page.target = target;
                return;
            }
        }
        scrollBy(0, offset);
        Page.target = document.activeElement;
    },

    plus: ()=> {
        Page.isPlus = !Page.isPlus;
        $('._hint').toggleClass('_plus');
    },

    click: (element) => {
        if ((element.tagName === 'INPUT' &&
            element.type.search(/(button|checkbox|file|hidden|image|radio|reset|submit)/i) === -1) ||
            element.hasAttribute('contenteditable') || element.tagName === 'TEXTAREA') {
            element._focus ? element._focus() : element.focus();
            shouldBlur = false;
            if (element.setSelectionRange) {
                var len = element.value.length * 2;
                element.setSelectionRange(len, len);
            }
        }

        else if (element.tagName === 'A' || element.tagName === 'INPUT') {
            element.click();
        }

        else {
            var names = ['mousedown', 'mouseup', 'click', 'mouseout'];
            for (var i = 0; i < names.length; i++) {
                element.dispatchEvent(new MouseEvent(names[i], {bubbles: true}));
            }
        }
    },

    isCommand: (event) => {
        var element = document.activeElement;
        var isInput = element && !element.hasAttribute('readonly') && (element.tagName.match(/INPUT|TEXTAREA/) ||
            element.hasAttribute('contenteditable'));

        var char = String.fromCharCode(event.keyCode).toUpperCase();
        var isUseful = $('._hint').length || 'FJK'.includes(char);
        return !event.ctrlKey && !isInput && isUseful;
    }
};

var Tree = {
    create: (from, to) => {
        return {
            from: Math.floor(from),
            to: Math.floor(to)
        }
    },

    getLeft: (node) => {
        if (node.left) {
            return node.left
        } else {
            return node.left = Tree.create(node.from, Math.floor((node.from + node.to) / 2));
        }
    },

    getRight: (node) => {
        if (node.right) {
            return node.right
        } else {
            return node.right = Tree.create(Math.floor((node.from + node.to) / 2) + 1, node.to);
        }
    },

    insert: (node, from, to, value) => {
        from = Math.floor(from);
        to = Math.floor(to);

        if (node.from === from && node.to === to) {
            if (node.values) {
                return node.values.push(value);
            } else {
                return node.values = [value];
            }
        }

        var mid = Math.floor((node.from + node.to) / 2);
        if (from < mid) {
            Tree.insert(Tree.getLeft(node), from, Math.min(to, mid), value);
        }
        if (to > mid) {
            Tree.insert(Tree.getRight(node), Math.max(from, mid + 1), to, value);
        }
    },

    search: (node, from, to, outPipe) => {
        from = Math.floor(from);
        to = Math.floor(to);

        if (node.from === from && node.to === to) {
            return include(node, outPipe);
        }
        if (node.values && node.values.length) {
            outPipe(node.values);
        }

        var mid = Math.floor((node.from + node.to) / 2);
        if (from < mid) {
            Tree.search(Tree.getLeft(node), from, Math.min(to, mid), outPipe);
        }
        if (to > mid) {
            Tree.search(Tree.getRight(node), Math.max(from, mid + 1), to, outPipe);
        }

        function include(node, outPipe) {
            if (node.values && node.values.length) {
                outPipe(node.values);
            }
            if (node.left) {
                include(node.left, outPipe)
            }
            if (node.right) {
                include(node.right, outPipe)
            }
        }
    }
};