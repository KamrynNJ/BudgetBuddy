const addButton= document.querySelector('#add');

var counter = 1;
var limit = 10;
function addInput(boxes){
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.setAttribute("id", "boxes1");
          newdiv.innerHTML = "<select name='drop'><option value='Groceries'selected>Groceries</option><option value='Home'>Home and Utilites</option><option value='Debt'>Debt or Loans</option><option value='Tuition'>Tuition</option><option value='Health'> Health and Personal Care</option><option value='Entertainment'>Entertainment</option><option value='Other'>Other</option></select> <input id ='destext' type='text' name='describe' placeholder='add a description' value=''> <input type='number' placeholder='0.00' step='0.01' name='myInputs[]'>";
          document.getElementById("boxes").appendChild(newdiv);
          counter++;
     }
}
addButton.addEventListener("click",addInput);

/*Below this line is JavaScript for the Budget HTML*/
