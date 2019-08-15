

 ///////////////////////////
  // Preloader
//   $(window).on('load', function () {

//     $("#loader").fadeOut("slow", function() {
//     // will fade out the whole DIV that covers the website.
//     $("#preloader").delay(1200).fadeOut("slow");
//     });

//   });


// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("myBtn").style.display = "block";
  } else {
    document.getElementById("myBtn").style.display = "none";
  }
}


