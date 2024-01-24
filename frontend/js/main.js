var baseUrl = "https://t4agg6lkng.execute-api.us-west-2.amazonaws.com/Prod";

function generateLogo() {
    console.log("generateLogo v1")
    var form = document.getElementById("logoInputs");
    
    var formData = {};

    for (var i = 0; i < form.elements.length; i++) {
        console.log(i);
        const element = form.elements[i];

        console.log(element);
        formData[element.id] = element.value;
    }

    console.log(formData);

    // Use ajax to send variables as json object to API 
    $.ajax({
        type: "POST",
        data: JSON.stringify(formData),
        url: baseUrl + "/gen-logo-image",
        headers: {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        crossDomain: true,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            console.log(data);
            alert('OK');
        },
        error: function (xhr, status, error) {
            alert('ERROR');
        }
    });

}