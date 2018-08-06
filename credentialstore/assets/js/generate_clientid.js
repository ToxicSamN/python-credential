
function generateClientId()
{
    const api = 'https://localhost/credentialstore/NewClientId';
    const clientId = document.getElementById('id_ClientId');
    var request = new XMLHttpRequest();
    request.open('GET', api, true);
    request.onload = function() {
        var data = JSON.parse(this.response);
        if (request.status >= 200 && request.status < 400) {
            clientId.value = data.ClientId;
            console.log(data.ClientId);
        }
    }
}