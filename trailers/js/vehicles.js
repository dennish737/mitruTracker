  // vehicle update scripts
  function edit_vehicle(elem){
    var data= elem.value;
    //console.log(data);
    //alert('This alert box was called with the id click event =' + data);
    location.href = "edit_vehicle.php?vehicle=" + data;   
  }

  function add_vehicle(){
    // location.href = "add_vehicle.php";
    //console.log(data);
    //alert('This alert box was called with the add click event');
    location.href = "add_vehicle.php";
  }

  function delete_delete (elem) {

  }

