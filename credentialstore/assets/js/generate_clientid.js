
$(document).ready(function () {
   $('#generate_id').click(function () {
        $.get('https://y0319t11888/credentialstore/NewClientId', function (data, status) {
            $('#id_ClientId').prop('value', data.ClientId);
        });
    });
});
