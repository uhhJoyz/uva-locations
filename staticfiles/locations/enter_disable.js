document.getElementById("form").onkeydown = function (e) {
  var key = e.key || 0;
  if (key == "Enter") {
    e.preventDefault();
  }
};
