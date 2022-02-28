// Upload async

$(document).ready(function (e) {
    $('#upload').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('file').files.length

        if(ins == 0) {
            $('#msg').html('<span style="color:red">Selectionner un fichier</span>');
            return;
        }

        for (var x = 0; x < ins; x++) {
            form_data.append("first_choice", document.getElementById('file').files[x]);
        }

        $.ajax({
            url: 'upload', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) { // display success response
                $('#msg').html('');
                $.each(response, function (key, data) {
                    if(key !== 'message') {
                        $('#msg').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg').append(data + '<br/>');
                    }
                })
            },
            error: function (response) {
                $('#msg').html(response.message); // display error response
            }
        });
    });

    $('#transform').on('click', function () {
        var form_data = new FormData();
    });
});

