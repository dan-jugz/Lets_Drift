

 ///////////////////////////
  // Preloader
  $(window).on('load', function () {

    $("#loader").fadeOut("slow", function() {
    // will fade out the whole DIV that covers the website.
    $("#preloader").delay(1200).fadeOut("slow");
    });

  });