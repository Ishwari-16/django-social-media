$.ajaxSetup({
      beforeSend: function beforeSend(xhr, settings) {
          function getCookie(name) {
             let cookieValue = null;


            if (document.cookie && document.cookie !== '') {
                  const cookies = document.cookie.split(';');

                   for (let i = 0; i < cookies.length; i++) {
                      const cookie = cookies[i].trim();
            
                      // If the cookie string starts with the name we want
                      if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                     }
                 }
           }

           return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    },
});      


$(document).on("click","js-toggle-modal", function(e){
      e.preventDefault()
      console.log("Hello I was clicked")
      //$(".js-model").toggleClass("hidden")
})