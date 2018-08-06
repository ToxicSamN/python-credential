
function getBaseUrl() {
    var re = new RegExp(/^.*\//);
    return re.exec(window.location.href);
}

$(document).ready(function () {
   $('#generate_id').click(function () {
        $.get((getBaseUrl()+'/credentialstore/NewClientId'), function (data, status) {
            $('#id_ClientId').prop('value', data.ClientId);
        });
    });
});
