

$('generate_id').click(function(){
   $.get('http://y0319t11888/credentialstore/NewClientId', function(data, status){
      $('#id_ClientId').prop('value', data);
   });
});
