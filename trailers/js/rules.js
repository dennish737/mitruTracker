// rule update functions

  function edit_rule(elem){
    var data= elem.value;
    //console.log(data);
    //alert('This alert box was called with the id click event =' + data);
    location.href = "edit_rule.php?rule=" + data;   
  }

  function add_vehicle(){
    //console.log(data);
    //alert('This alert box was called with the add click event');
    location.href = "add_rule.php";
  }

  function delete_delete (elem) {

  }

