// scripts for contacts

  function edit_contact(elem){
    var data= elem.value;
    //console.log(data);
    //alert('This alert box was called with the id click event =' + data);
    location.href = "edit_contact.php?contact=" + data;   
  }

  function add_contact(){
    //console.log(data);
    //alert('This alert box was called with the add click event');
    location.href = "add_contact.php";
  }

  function delete_contact (elem) {

  }

