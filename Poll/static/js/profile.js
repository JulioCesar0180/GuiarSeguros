$(function () {
    $("#button_update_manager").click(function () {
        $("#modal_update_manager").addClass("is-active");
    });
    $("#cancel-manager").click(function () {
        $("#modal_update_manager").removeClass("is-active");
    });
    $("#close_manager").click(function () {
        $("#modal_update_manager").removeClass("is-active");
    })
});

$(document).ready(function () {
    var $form_manager = $('#form_update_manager');
    $form_manager.submit(function (event) {
        event.preventDefault();
        var $formData = $(this).serialize();
        var $thisURL = $form_manager.attr('data-url');
        console.log($thisURL);
        $.ajax({
            method: 'POST',
            url: $thisURL,
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError,
        })
    });
    function handleFormSuccess(data, textStatus, jqXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);
        $("#modal_update_manager").removeClass("is-active");
        location.reload();
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

$(function () {
    $("#button_update_user").click(function () {
        $("#modal_update_user").addClass("is-active");
    });
    $("#cancel-user").click(function () {
        $("#modal_update_user").removeClass("is-active");
    });
    $("#close_user").click(function () {
        $("#modal_update_user").removeClass("is-active");
    })
});

$(document).ready(function () {
    var $form_user = $('#form_update_user');
    $form_user.submit(function (event) {
        event.preventDefault();
        var $formData = $(this).serialize();
        var $thisURL = $form_user.attr('data-url');
        console.log($thisURL);
        $.ajax({
            method: 'POST',
            url: $thisURL,
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError,
        })
    });
    function handleFormSuccess(data, textStatus, jqXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);
        $("#modal_update_user").removeClass("is-active");
        location.reload();
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});


$(function () {
    $("#button_change_password").click(function () {
        console.log("HEllo");
        $("#modal_change_password").addClass("is-active");
    });
    $("#cancel_change_password").click(function () {
        $("#modal_change_password").removeClass("is-active");
    });
    $("#close_change_password").click(function () {
        $("#modal_change_password").removeClass("is-active");
    })
});