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

    function getChart(id) {
        var allCharts = AmCharts.charts;
        for (var i = 0; i < allCharts.length; i++) {
            if (id == allCharts[i].div.id) {
                return allCharts[i];
            }
        }
    }

    $("#ddlCsv").change(function(){
        //this.value
        var inputReg = new RegExp("^[a-zA-Z]{3,4}_[0-9]{2,3}[PCpc]{1}[0-9]{8}$");
        if(inputReg.test(this.value)){ //Valid input select
            console.log("Requesting chart values for: " + this.value);

            $.ajax({
                type: "POST",
                url: 'ajax/requestChartData/',
                dataType: "json",
                data: {selectedData: this.value},
                success: function(result) {
                    if(result != null){
                        var myChart = getChart("chartdiv");
                        myChart.dataSets[0].dataProvider = result;
                        myChart.validateData();
                    }
                }
            });
        }
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

                //Output les BUY/SELL dans le "Log"
                var history = result.message["buySellHistory"];
                var logOutput = "";

                var myChart = getChart("chartdiv");
                var currentData = [];

                $.each(history, function (i, value) {

                    if(value["buysell"] == "BUY") {
                        currentData.push({
                            date: value["date"],
                            type: "text",
                            backGroundColor: "#CC0000",
                            graph: "g1",
                            //description: value["price"],
                            text: "Buy @ " + value["price"],
                            showAt: "high"

                        });
                    } else { // == "SELL"
                        currentData.push({
                            date: value["date"],
                            type: "text",
                            backGroundColor: "#CC0000",//"#00CC00",
                            graph: "g1",
                            //description: value["price"],
                            text: "Sell @ " + value["price"],
                            showAt: "high"
                        });
                    }

                    var buysell = value["buysell"];
                    var date = value["date"];
                    var instrument = value["instrument"];
                    var price = value["price"]

                    logOutput += " > " + buysell + " - " + price + " - " + instrument
                        + " - " + date + " \n";
                });
                //Output to chart
                myChart.dataSets[0].stockEvents = currentData;
                myChart.validateNow(true, true);

                //Output to log
                $("#backtestLog").val(logOutput);

                var statusMessagesSeperated = '';
                $.each(result.statusmessages, function (index, value) {
                    statusMessagesSeperated += value  + "<br>";
                });

                //Mettre les valeurs initiales et finales dans le result
                $("#backtestResults").val(result.results);

                alertModal("Strategy execution result", statusMessagesSeperated);
            }
        });
    });

    function alertModal(title, body) {
        // Display error message to the user in a modal
        $('#alert-modal-title').html(title);
        $('#alert-modal-body').html(body);
        $('#alert-modal').modal('show');
    }


    //Loading des chart data (dropdown #ddlCsv)
    $.ajax({
        type: "GET",
        url: 'ajax/loadChartDataCsv/',
        dataType: "json",
        //data:{},
        success: function(result) {
            //Ici on popule le dropdown pour le chart data
            var html = "";
            for (var i = 0; i < result.length ; i++){
                var current = result[i];
                var file = current.file;
                var title = current.title;
                html += "<option value='"+ file +"'>"+ title +"</option>";
            }
            $("#ddlCsv").append(html);
        }
    });
});

