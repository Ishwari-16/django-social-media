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

$(document).on("click", ".js-follow", function(e){
    e.preventDefault();

    const $btn = $(this);

    $.ajax({
        type: "POST",
        url: $btn.data("url"),
        data: {
            action: $btn.attr("data-action"),
            username: $btn.attr("data-username")
        },

        success: function(data){

            $(".js-follow-text").text(data.wording);

            if($btn.attr("data-action") === "follow"){
                $btn.attr("data-action","unfollow");
            } else {
                $btn.attr("data-action","follow");
            }
        },

        error: function(xhr){
            console.log(xhr.responseText);
        }
    });
});
    
success:(data) => {
    $btn.find(".js-follow-text").text(data.wording);

    if(action == "follow") {
        $btn.attr("data-action", "unfollow");
    } else {
        $btn.attr("data-action", "follow");
    }
}