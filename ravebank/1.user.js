// ==UserScript==
// @name     Rave bank
// @version  1
// @grant    none
// ==/UserScript==

var magic = function()
{
setInterval(function()
{
  if(document.location.href == 'http://rave-bank.level-up.2020.tasks.cyberchallenge.ru/' || document.location.href == 'http://rave-bank.level-up.2020.tasks.cyberchallenge.ru/sign-in')
    document.location.href = 'http://rave-bank.level-up.2020.tasks.cyberchallenge.ru/sign-up';
}, 500);

if(document.location.href == 'http://rave-bank.level-up.2020.tasks.cyberchallenge.ru/sign-up')
{
  var ael = EventTarget.prototype.addEventListener;
  var els = [];
  EventTarget.prototype.addEventListener = function(which, f)
  {
    ael.call(this, which, f);
    if(which == 'input')
      els.push([this, which, f]);
  };
  var it = +(localStorage["sleirs"] || 0);
  localStorage["sleirs"] = it + 1;
  var int = setInterval(function()
  {
    document.querySelector("input[formcontrolname=username]").value = document.querySelector("input[formcontrolname=password]").value = 'sleirs0'+it;
    for(var i = 0; i < els.length; i++)
      els[i][2].call(els[i][0], { type: 'input', target: els[i][0], isTrusted: true, isComposing: false, inputType: "insertText", data: "1", detail: 0, layerX: 0, layerY: 0, pageX: 0, pageY: 0 });
    clearInterval(int);
  }, 10);
}
}

var elt = document.createElement('script');
elt.innerHTML = '('+magic+')()';
document.body.appendChild(elt);
