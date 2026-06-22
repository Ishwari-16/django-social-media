
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

$(document).on("click", ".js-toggle-modal", function(e){
      e.preventDefault();
      $("#post-modal").toggleClass("hidden");
      $("#post-modal").toggleClass("flex");
})
    .on("click", ".js-submit", function(e){
        e.preventDefault()
        console.log("Submit me?")
        const text= $(".js-post-text").val().trim()
        const $btn = $(this)

        if(!text.length){
            return false; 
        }

        $btn.prop("disabled", true).text("Posting!")
        $.ajax({
            type:'POST',
            url:$(".js-post-text").data("post-url"),
            data:{
                text:text
            },
        success:(dataHtml) => {
            $("#post-modal").addClass("hidden");
            $("#posts-container").prepend(dataHtml);
            $btn.prop("disabled",false).text("Post");
            $(".js-post-text").val('')
        },
        error:(error) => {
            console.warn(error)
            $btn.prop("disabled", false).text("Error");
        }
    });
})
.on("click", ".js-follow", function(e){
    e.preventDefault();

    const $btn = $(this);

    $.ajax({
        type: "POST",
        url: $btn.data("url"),
        data: {
            action: $btn.attr("data-action"),
            username: $btn.data("username"),
        },

        success: function(data){

            if(data.wording === "Unfollow"){
                $btn.attr("data-action", "unfollow");
                $btn.find(".js-follow-text").html(
                    "<i class='bx bx-user-minus mr-2'></i>Unfollow"
                );
            } else {
                $btn.attr("data-action", "follow");
                $btn.find(".js-follow-text").html(
                    "<i class='bx bx-user-plus mr-2'></i>Follow"
                );
            }

            console.log("SUCCESS", data);
        },

        error: function(error){
            console.log(error);
        }
    });
})