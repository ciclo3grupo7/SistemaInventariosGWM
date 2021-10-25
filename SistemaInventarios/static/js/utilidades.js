
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

