/* Setup chat, dwww */
(function loadScrollReveal() {
  const script = document.createElement("script");
  script.src = "https://unpkg.com/scrollreveal";
  script.onload = iniciarAnimaciones;
  document.head.appendChild(script);
})();

/*-- Animación --*/
function iniciarAnimaciones() {
    //clase ".card"
    ScrollReveal().reveal('.card-publi', {
        origin: 'bottom',
        distance: '40px',
        duration: 700,
        interval: 130,
        reset: false
    });
  }