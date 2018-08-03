/* js/showhidepassword.js */

function reveal()
{
    if(document.getElementById('show_password').checked)
        {document.getElementById("password").type='text';}
    else
        document.getElementById("password").type='password';
}