const addButton= document.querySelector('#add');

function addItem(){
    var ul = document.getElementById("expenses");
    var text = document.getElementById("destext");
    var li = document.createElement("li");
    li.setAttribute('id',text.value);
    li.appendChild(document.createTextNode(text.value));
    ul.appendChild(li);
}
addButton.addEventListener("click",addItem);
