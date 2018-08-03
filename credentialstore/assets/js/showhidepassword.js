/* js/showhidepassword.js */

function reveal()
{
    if(document.getElementById('show_password').checked)
        {document.getElementById("id_password").type='text';}
    else
        document.getElementById("id_password").type='password';
}