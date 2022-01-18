<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
         pageEncoding="ISO-8859-1" %>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">

    <title>File Upload</title>
</head>
<body>
<h1>File Upload</h1>
<form method="post" action="/TravailTest_war_exploded/hello-servlet"
      enctype="multipart/form-data">
    Select file to upload: <input type="file" name="file" size="60"/><br/>
    <br/> <input type="submit" value="Upload"/>
    <input type="hidden" id="userName" name="userName" value="yona">
    <input type="hidden" id="token" name="token" value="yona">
</form>
</form>
<h2>
    <div method="get">
        <button onclick="sendRequest('/TravailTest_war_exploded/ShowRecordsServlet')" type="submit">Montrer les fichiers</button>
    </div>

</h2>
<h3>
    <div id="here_table"></div>
</h3>
<script >

    function sendRequest(url){
        sendExternalRequest(url).then((ans)=>{ //builds a dynamic table for the records in answer
                $("#here_table").append("<table id=\"my_table1\"></table>");
                var trvalue = '';
                $("#my_table1").empty();
                trvalue += '<tr><td><b>nom</b></td><td><b>extension</b></td><td><b>chemin</b></td><td><b>date</b></td><td><b>utilisateur</b></td></tr>';
                $.each(ans.data.objects.resultList, function(i, item){
                    trvalue+='<tr>';
                    let id = 0;
                    $.each(item, function(key, value){ //builds row for each record
                        if(key === 'path' ){
                            trvalue += '<td>' + '<a' + ' href=' + value + ' >' + value +'</a>'+ '</td>';
                        }
                        else if(key === 'date'){
                            trvalue += '<td>' + value.date.year + ':' + value.date.month + ':' + value.date.day + ':' + value.time.hour + ':' + value.time.minute + ':' + value.time.second + '</td>';
                        }
                        else if(key==='id'){
                            id = value;
                        }
                        else if(key !== 'driveId'){
                            trvalue += '<td>' + value + '</td>';
                        }
                    })
                    trvalue+='<td><button type="button" onclick="changeName('+ id.toString() +')">Editer le nom</button></td>';
                    trvalue+='</tr>';
                });
                $("#my_table1").append(trvalue); //append table to html
        })
    }

    function changeName(id){
        let nom = prompt("Entrer le nouveau nom !!");
        let data = {
            id: id,
            name: nom
        }
        //envoi de la demande de changement de nom au servlet
        sendExternalRequest('/TravailTest_war_exploded/Update_Record',true,data).then();
    }

    function sendExternalRequest(url, isJsonAns, data) {
        return new Promise(function (resolve, reject) {
            console.log(JSON.stringify(data));
            let request = $.ajax({
                type: 'GET',
                url,
                data: data,
                headers: {}
            });

            request.done(function (data, textStatus, headers) {

                let body;

                console.log("DATA ---> "+JSON.stringify(data));
                if (isJsonAns !== false) {
                    if (typeof data !== "object") {
                        body = JSON.parse(data);
                    } else
                        body = data;
                }

                resolve({status: (headers.status == 200), data: body, code: headers.status});
            });
        });
    }
</script>
</body>
</html>