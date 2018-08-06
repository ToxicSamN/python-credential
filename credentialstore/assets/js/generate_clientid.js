
function getBaseUrl() {
    return window.location.origin?window.location.origin+'/':window.location.protocol+'/'+window.location.host+'/';
}

$(document).ready(function () {
   $('#generate_id').click(function () {
        $.get((getBaseUrl()+'credentialstore/NewClientId'), function (data, status) {
            $('#id_ClientId').prop('value', data.ClientId);
        });
    });
});
