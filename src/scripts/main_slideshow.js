(function () {
    const images = [
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        // "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg",
        "assets/img/placeholder.svg"
    ];

    const imgEl = document.getElementById("slideshow");
    const DELAY = 4000;
    const FADE = 300;

    // Start with first image
    let index = 0;
    imgEl.src = images[index];

    function nextImage() {
        const nextIndex = (index + 1) % images.length;
        const nextSrc = images[nextIndex];

        // Preload the next image to avoid flashes
        const pre = new Image();
        pre.onload = () => {
            imgEl.style.opacity = 0;
            setTimeout(() => {
                imgEl.src = nextSrc;
                imgEl.style.opacity = 1;
                index = nextIndex;
                setTimeout(nextImage, DELAY);
            }, FADE);
        };
        pre.src = nextSrc;
    }
    setTimeout(nextImage, DELAY);
})();