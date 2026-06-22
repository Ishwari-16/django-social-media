console.log("MAIN JS LOADED");

$(document).on("click", ".js-follow", function(e){
    e.preventDefault();

    alert("FOLLOW CLICKED");

    const btn = $(this);

    $.ajax({
        type: "POST",
        url: btn.data("url"),
        data: {
            username: btn.data("username"),
            action: btn.data("action")
        },
        success: function(data){
            alert("SUCCESS");
        },
        error: function(xhr){
            alert("ERROR " + xhr.status);
        }
    });
});