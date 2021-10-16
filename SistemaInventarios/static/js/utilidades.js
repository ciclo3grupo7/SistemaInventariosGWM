function fijar_consultarDato(document, claseMod, ruta, campoId,
                              modalClassBody, modalIdSeccion) {
    //alert("hola1")
    $(document).ready(function(){
        $(claseMod).click(function(){
            //alert("hola2");
            //alert("campoId: "+campoId);
            var id = $(this).data(campoId);
            //alert("id: "+id);
            $.ajax({
                url: ruta,
                type: 'post',
                //{llave: valor} esto es igual a decir {'llave': valor}
                //data es el valor que se transmile como datos de entrada de formulario al decorador /ajaxfile como request.form
                data: {'id': id},
                success: function(data){ 
                    // "success" es la funcion que se ejecuta jsonify() en el decorador /ajaxfile
                    // "data" es el diccionario que retorna jsonify()
                    // "data" contiene {'htmlresponse': render_template('response.html',employeelist=employeelist)} el render con el html.
                    //alert("success Ajax");
                    //console.log("entro success Ajax");
                    //console.log("data");
                    //console.log(data);
                    $(modalClassBody).html(data); 
                    $(modalClassBody).append(data.htmlresponse);
                    $(modalIdSeccion).modal('show'); 
                }
            });
        });
    });
}

function fijar_saltoModal(document, claseMod, ruta, campoId,
                              modalClassBody, modalIdSeccion) {
    $(document).ready(function(){
        $(claseMod).click(function(){
            var id = $(this).data(campoId);
            $.ajax({
                url: ruta,
                type: 'post',
                data: {'id': id},
                success: function(data){ 
                    $(modalClassBody).html(data); 
                    $(modalClassBody).append(data.htmlresponse);
                    $(modalIdSeccion).modal('show'); 
                }
            });
        });
    });
}

