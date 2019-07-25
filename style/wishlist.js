const addButton= document.querySelector('#add');

var counter = document.getElementById("counter_input").value;
counter++;
var limit = 10;
function addInput(boxes){
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.setAttribute("id", "boxes1");
          newdiv.innerHTML = "<input id ='destext' type='text' name='describe["+counter+"]' placeholder='Add Item Name' value=''> <input type='number' placeholder='0.00' step='0.01' name='myInputs["+counter+"]'>";
          document.getElementById("boxes").appendChild(newdiv);
          document.getElementById("counter_input").value=counter;
          counter++;
     }
}
addButton.addEventListener("click",addInput);

/*Below this line is JavaScript for the Budget HTML*/
