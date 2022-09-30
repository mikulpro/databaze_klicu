// zadat do konzole na https://portal.ujep.cz/portal/studium/prohlizeni.html

data = 'type=mistnost&varName=G230413suggestor&mistnostSearchBudova=CP&mistnostSearchPracoviste=%25&mistnostKapacitaOd=0&mistnostKapacitaDo=999&mistnostJenPlatne=A&search=true&porLo=cs'
// url našeptávače
url = 'https://portal.ujep.cz/StagPortletsJSR168/StagSuggest'

var myAjax = jQuery.ajax({
    type: "POST",
    url: url,
    timeout: 20000, // By Konzerva-Timeout pro dohledavace
    contentType: "application/x-www-form-urlencoded; charset=UTF-8",
    data: data,
    success: function(msg, textStatus) {
        console.log(msg),
        console.log(textStatus)
    },
    error: function(request, textStatus, errorThrown) {
      request.abort();
},})