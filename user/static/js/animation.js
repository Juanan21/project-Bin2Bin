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

    // container para que todo se mueva adecuado xp//
        ScrollReveal().reveal('post-gallery', {
        reset: false,
        interval: 350,
    });

    //para todas las imagenes //

    //clase  "image small"
        ScrollReveal().reveal('.small li', {
        origin: 'bottom',
        opacity: 0,
        duration: 600,
        reset: false,
        interval: 350,
    });
        ScrollReveal().reveal('.big', {
        origin: 'right',
        duration: 650,
        reset: false,
    });
    }
