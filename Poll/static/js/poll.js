/* method: POST
* Datos generales de la empresa
* form: 1
* */
$(document).ready(function () {
    var $form = $('#id_personal_BS');
    $form.submit(function (event) {
        event.preventDefault();
        var $formData = $(this).serialize();
        var $thisURL = $form.attr('data-url');
        $.ajax({
            method: 'POST',
            url: $thisURL,
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError,
        })
    });

    function handleFormSuccess(data, textStatus, jqXHR){
        console.log("Otra vez POST")
        plusSlides(1);
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

/* method: POST
* Datos del representante
* form: 2
* */
$(document).ready(function () {
    var $form_bm = $('#id_personal_BM');
    $form_bm.submit(function (event) {
        event.preventDefault();
        var $formData = $(this).serialize();
        var $thisURL = $form_bm.attr('data-url');
        $.ajax({
            method: 'POST',
            url: $thisURL,
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError,
        })
    });

    function handleFormSuccess(data, textStatus, jqXHR){
        console.log("POST 2")
        plusSlides(1);
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

/* method: POST
* ventas anuales
* form: 3
* */

$(document).ready(function () {
    var $form_sales = $('#id_sales');
    $form_sales.submit(function (event) {
        event.preventDefault();
        var $formData = $(this).serialize();
        var $thisURL = $form_sales.attr('data-url');
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
        plusSlides(1);
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

/* method: POST
* Dotacion de la empresa
* form: 4
* */

$(document).ready(function () {
    var $form_quantity = $('#id_quantity');
    $form_quantity.submit(function (event) {
        event.preventDefault();
        var $formData = $(this).serialize();
        var $thisURL = $form_quantity.attr('data-url');
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
        plusSlides(1);
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

/* method: POST
* procesos de la empresa
* form: 5
* */

$(document).ready(function () {
    var $form_quantity = $('#id_process');
    $form_quantity.submit(function (event) {
        event.preventDefault();
        var $formData = $(this).serialize();
        var $thisURL = $form_quantity.attr('data-url');
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
        plusSlides(1);
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
}