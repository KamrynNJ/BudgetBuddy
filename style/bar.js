var counter = document.getElementById("counter_input").value;

function showSavingsM1initial() {
  var x = document.getElementById("oneMonthSavingDisplay");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "none";
  }
}

function showSavingsM2initial() {
  var x = document.getElementById("twoMonthSavingDisplay");
  if (x.style.display === "block") {
    x.style.display = "none";
    counter=1;
  } else {
    x.style.display = "none";

  }
}

function showSavingsM6initial() {
  var x = document.getElementById("sixMonthSavingDisplay");
  counter=2;
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "none";

  }
}

function showSavingsM12initial() {
  var x = document.getElementById("twelveMonthSavingDisplay");
  counter=3;
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {

  }
}

showSavingsM1initial();
showSavingsM2initial();
showSavingsM6initial();
showSavingsM12initial();



function showSavingsM1() {
  var x = document.getElementById("oneMonthSavingDisplay");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function showSavingsM2() {
  var x = document.getElementById("twoMonthSavingDisplay");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function showSavingsM6() {
  var x = document.getElementById("sixMonthSavingDisplay");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function showSavingsM12() {
  var x = document.getElementById("twelveMonthSavingDisplay");
  counter=3;
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
