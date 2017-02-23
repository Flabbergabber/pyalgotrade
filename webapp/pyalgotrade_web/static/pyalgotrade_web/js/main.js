$(document).ready(function () {
    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            $(".loadingmodal").show();
        },
        complete: function () {
            $(".loadingmodal").hide();
        }
    });

    $('#btnLoad').click(function (e) {

        //Ici faire apparaitre le file input dialog
        var filename = "";
        //TODO modal dialog

        $.FileDialog({
            // MIME type of accepted files, e. g. image/jpeg
            accept: "*",
            // cancel button
            cancelButton: "Close",
            // drop zone message
            dragMessage: "Déposez vos fichiers ici.",
            // the height of drop zone in pixels
            dropheight: 200,
            // error message
            errorMessage: "An error occured while loading file",
            // whether it is possible to choose multiple files or not.
            multiple: false,
            // OK button
            okButton: "OK",
            // file reading mode.
            // BinaryString, Text, DataURL, ArrayBuffer
            readAs: "DataURL",
            // remove message
            removeMessage: "Remove&nbsp;file",
            // file dialog title
            title: "Load file(s)"
        })
            .on('files.bs.filedialog', function (ev) {
                // handle files choice when done
                var file = ev.files[0];
                //editor.setValue(atob(file.content),-1)

                var newString = file.content.replace("data:text/plain;base64,", "");
                console.log(file.content);
                editor.setValue(Base64.decode(newString), -1);
                /*
                 $.ajax({
                 type: "POST",
                 url: 'ajax/uploadFile/',
                 dataType: "json",
                 data: {fileName: file.content},
                 success: function(result) {
                 //Handle le retour du controller (texte)
                 console.log("btnLoad success")
                 var editor = ace.edit("editor");
                 editor.setValue(result.texte,-1);
                 }
                 });
                 */

            }).on('cancel.bs.filedialog', function (ev) {
            // DO SOMETHING
            console.log("User cancelled file upload.");
        });


    });

    $("#btnSave").click(function (e) {

        var codePython = ace.edit('editor').getValue();
        var fileName = "Strategy.py";

        var blob = new Blob([codePython], {
            type: "text/plain;charset=utf-8"
        });

        saveAs(blob, fileName);
    });

    $("#btnBeginBacktest").click(function(e) {
        e.preventDefault();

        // information to be sent to the server
        var strategy = editor.getValue();

        $.ajax({
            type: "POST",
            url: 'ajax/beginBacktest/',
            dataType: "json",
            data: {strategy: strategy},
            success: function(result) {
                $("#backtestResults").val(result.message);
            }
        });
    });

});

