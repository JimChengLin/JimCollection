'use strict';

var prevWord;
var audio = new AudioContext();
addEventListener('mouseup', translate);

function translate(event) {
    var prevPopup = document.querySelector('._popup');
    if (prevPopup) {
        document.body.removeChild(prevPopup);
    }

    var selection = getSelection();
    if (selection.anchorNode.nodeType === 3) {
        var word = selection.toString();
        if (word && word !== prevWord) {
            prevWord = word;
            request();
        }
    }

    function request() {
        var ts = Date.now();
        var requestLink = 'http://fanyi.youdao.com/openapi.do?type=data&doctype=json&version=1.1&relatedUrl=' +
            encodeURIComponent('http://fanyi.youdao.com/#') +
            '&keyfrom=fanyiweb&key=null&translate=on' +
            '&q=' + word +
            '&ts=' + ts;

        GM_xmlhttpRequest({
            method: 'GET',
            url: requestLink,
            onload: (res) => displayPopup(event.clientX, event.clientY, res.response)
        });
    }
}

function displayPopup(x, y, response) {
    var popup = document.createElement('div');
    popup.classList.add('_popup');

    var map = JSON.parse(response);
    'basic' in map ? word() : sentence();

    function word() {
        var query = map['query'];
        var basic = map['basic'];

        var header = document.createElement('div');
        var span = document.createElement('span');
        span.innerText = query;
        span.style.color = 'black';
        header.appendChild(span);

        var phonetic = basic['phonetic'];
        if (phonetic) {
            var phoneticElement = document.createElement('span');
            phoneticElement.innerText = '[' + phonetic + ']';
            phoneticElement.style.color = 'darkBlue';
            phoneticElement.style.cursor = 'pointer';
            phoneticElement.addEventListener('mouseup', (event) => event.stopPropagation());
            header.appendChild(phoneticElement);

            var soundUrl = 'https://dict.youdao.com/dictvoice?type=2&audio=' + query;
            GM_xmlhttpRequest({
                method: 'GET',
                url: soundUrl,
                responseType: 'arraybuffer',

                onload: (res) => {
                    audio.decodeAudioData(res.response, (buffer) => {
                        phoneticElement.addEventListener('mouseup', () => {
                            var source = audio.createBufferSource();
                            source.buffer = buffer;
                            source.connect(audio.destination);
                            source.start(0);
                        });
                        header.appendChild(document.createTextNode('✓'));
                    });
                }

            });
        }

        header.style.margin = '0px';
        header.style.padding = '0px';
        popup.appendChild(header);

        var hr = document.createElement('hr');
        hr.style.margin = '0px';
        popup.appendChild(hr);

        var ul = document.createElement('ul');
        basic['explains'].map((explain) => {
            var li = document.createElement('li');
            li.appendChild(document.createTextNode(explain));
            ul.appendChild(li);
        });

        ul.style.listStyle = 'none';
        ul.style.margin = '0px';
        ul.style.padding = '0px';
        ul.style.textAlign = 'left';
        popup.appendChild(ul);
    }

    function sentence() {
        popup.appendChild(document.createTextNode(map['translation']));
    }

    popup.style.left = x + popup.offsetWidth > innerWidth ? x - popup.offsetWidth + 'px' : x + 'px';
    popup.style.top = y + popup.offsetHeight > innerHeight ? y - popup.offsetHeight + 'px' : y + 'px';
    document.body.appendChild(popup);
}

document.body.innerHTML += `<style>._popup {
    background: lightblue;
    border-radius: 5px;
    box-shadow: 0 0 5px;
    color: black;
    font-size: 13px;
    max-width: 200px;
    padding: 5px;
    position: fixed;
    z-index: 1024;
}</style>`;