
function generateClientId()
{
    const api = 'https://localhost/credentialstore/NewClientId';
    const clientId = document.getElementById('id_ClientId');
    var request = new XMLHttpRequest();
    request.open('GET', api, true);
    request.onload = parse_data(request);
    request.send();
}

function parse_data(request) {
    var data = JSON.parse(request.response);
    if (request.status >= 200 && request.status < 400) {
        clientId.value = data.ClientId;
    }
}