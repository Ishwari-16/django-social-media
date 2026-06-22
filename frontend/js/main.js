console.log("MAIN JS LOADED");
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

console.log("MAIN JS LOADED");
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

    console.log("FOLLOW BUTTON CLICKED");

    const $btn = $(this);
    const action = $btn.attr("data-action");

    $.ajax({
        type:'POST',
        url:$btn.data("url"),
        data:{
            action:action,
            username:$btn.data("username"),
        },
        success:(data) => {
            $btn.find(".js-follow-text").text(data.wording);

            if(action === "follow"){
                $btn.attr("data-action","unfollow");
            } else {
                $btn.attr("data-action","follow");
            }
        },
        error:(error) => {
            console.warn(error);
        }
    });
})