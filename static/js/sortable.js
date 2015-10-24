

$(document).bind('DOMSubtreeModified', function () {
    var currPos1;
    var currPos2;
    $(".sortable").sortable({
        items: "> .ui-state-default",
        revert: true,
        axis: "y",
        cursor: "move",
        stop: function (event, ui) {
            positions = $(this).sortable("toArray");
            $.ajax({
                data: {
                    positions: positions
                },
                beforeSend: function () {
                    $('.indicator').css('display', 'block');
                    $(this).prop('disabled', true)
                },
                type: 'GET',
                url: '/update_priority/',
                success: function () {
                    $('.indicator').css('display', 'none');
                }
            });
        }
    });
});