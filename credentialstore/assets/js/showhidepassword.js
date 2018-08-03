/* js/showhidepassword.js */

$('#show_password').prop('checked', false);
$('#id_password').prop('type', 'password');

function reveal()
{
    if(document.getElementById('show_password').checked)
        {document.getElementById("id_password").type='text';}
    else
        document.getElementById("id_password").type='password';
}