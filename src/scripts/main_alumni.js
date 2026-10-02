/* ===============================
   HEADER ANIMATION
================================ */
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.2 });

const header = document.querySelector("#people .people-header");
if (header) observer.observe(header);

/* ===============================
   INFINITE SLIDERS
   Tools & Technologies we use
================================ */

const DUPLICATE_COUNT = 4;
const ALT_TEXT = "Tool logo";

/* TOOLS / TECH WE USE */
const companyImages = [
  { src: "https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg", alt: "Python" },
  { src: "https://upload.wikimedia.org/wikipedia/commons/1/18/ISO_C%2B%2B_Logo.svg", alt: "C++" },
  { src: "https://upload.wikimedia.org/wikipedia/commons/3/32/OpenCV_Logo_with_text_svg_version.svg", alt: "OpenCV" },
  { src: "https://upload.wikimedia.org/wikipedia/commons/8/87/Arduino_Logo.svg", alt: "Arduino" },
  { src: "https://upload.wikimedia.org/wikipedia/en/c/cb/Raspberry_Pi_Logo.svg", alt: "Raspberry Pi" },
  { src: "https://upload.wikimedia.org/wikipedia/commons/2/21/Matlab_Logo.png", alt: "MATLAB" },
  { src: "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg", alt: "Linux" },
];

/* COMPETITIONS / EVENTS we've been part of */
const universityImages = [
  { src: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/IIT_Bombay_Logo.svg/240px-IIT_Bombay_Logo.svg.png", alt: "IIT Bombay" },
  { src: "https://upload.wikimedia.org/wikipedia/en/thumb/8/8b/VJTI_logo.png/220px-VJTI_logo.png", alt: "VJTI" },
  { src: "https://upload.wikimedia.org/wikipedia/en/thumb/9/9d/FCRCE-Logo.png/220px-FCRCE-Logo.png", alt: "FCRCE" },
];

function fillSlider(sliderId, images) {
  const slider = document.getElementById(sliderId);
  if (!slider) return;

  for (let i = 0; i < DUPLICATE_COUNT; i++) {
    images.forEach(item => {
      const img = document.createElement("img");
      img.src = typeof item === "string" ? item : item.src;
      img.alt = typeof item === "string" ? ALT_TEXT : item.alt;
      img.loading = "lazy";
      img.onerror = function() { this.style.display='none'; };
      slider.appendChild(img);
    });
  }
}

/* INIT SLIDERS */
fillSlider("companySlider", companyImages);
fillSlider("universitySlider", universityImages);
