function isNumeric(str) {
    if (typeof str != "string") return false // we only process strings!  
    return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
           !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail
  }
function handleInput(e) {
    const nextVal = 
      e.target.value.substring(0, e.target.selectionStart) +
      (e.data ?? '') +
      e.target.value.substring(e.target.selectionEnd)
    ;
    if(!/^(\d{0,7}|\d{3}-?\d{0,4}|)$/.test(nextVal)) {
        e.preventDefault();
    }
    return;
}
function removeHandler() {
    this.parentNode.remove();
}
function addRow() {
    const elm = document.querySelector("tbody").insertRow();
    const volElm = elm.insertCell();
    const massElm = elm.insertCell();
    const floatsElm = elm.insertCell();
    const volInp = document.createElement("input");
    const massInp = document.createElement("input");
    const floatsInp = document.createElement("input");
    volElm.appendChild(volInp);
    volInp.onbeforeinput = handleInput;
    volInp.value = 1;
    volInp.type = "number";
    massElm.appendChild(massInp);
    massInp.onbeforeinput = handleInput;
    massInp.value = 1;
    massInp.type = "number";
    floatsElm.appendChild(floatsInp);
    floatsInp.type = "checkbox";
    const remElm = elm.insertCell();
    remElm.textContent = "Remove";
    remElm.onclick = removeHandler;
    remElm.classList.add("remover");
}