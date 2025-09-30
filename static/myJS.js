function alertfun()
{
  $(".alert").fadeTo(3000, 500).slideUp(500, function(){
  $(".alert").slideUp(500); 
  });
}

$(document).on('click', '.confirm-delete', function(){
    return confirm('Are you sure you want to delete this?');
})