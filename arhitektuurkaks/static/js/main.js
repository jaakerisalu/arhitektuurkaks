function initDescriptionListener() {
    $('.get-description').on('click', function(e) {
        e.stopPropagation();

        $.getJSON("api/?id=" + $(this).attr("data-id"), function(data) {
            console.log(data);
            var $panel = $("#description");
            if (!$panel.hasClass("visible")) {
                $panel.addClass("visible");
            }
            $panel.find("#description-title").html(data.name);
            $panel.find("#description-content").html(data.description);
        });
        return false;
    });
}
