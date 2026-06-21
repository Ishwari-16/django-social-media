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
    const action = $btn.attr("data-action")
    $.ajax({
            type:'POST',
            url:$(this).data("url"),
            data:{
                action:action,
                username: $(this).data("username"),
            },
            success:(data) => {
                $(".js-follow-text").text(data.wording)
                if(action == "follow") {
                    //Change wording to unfollow
                    console.log("DEBUG", "unfollow")
                    $(this).attr("data-action", "unfollow")
                }else {
                    // The opposite
                    console.log("DEBUG", "follow")
                    $(this).attr("data-action", "follow")
                }
            },
            error:(error) => {
                console.warn(error)
            
            }
    });
})
