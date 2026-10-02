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
================================ */

const DUPLICATE_COUNT = 4;
const ALT_TEXT = "Alumni logo";

/* COMPANY LOGOS */ 
const companyImages = [
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
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg"

  

];

/* UNIVERSITY LOGOS */
const universityImages = [
  "assets/images/companies/Aalto.png",
  "assets/img/placeholder.svg",
  "assets/images/companies/Delft.png",
  "assets/img/placeholder.svg",
  "assets/images/companies/IISc.png",
  "assets/images/companies/IITM.svg",
  "assets/img/placeholder.svg",
  "assets/images/companies/Northeastern.png",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/images/companies/qut.png",
  "assets/images/companies/RWTH.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/images/companies/wisconsin-madison.png",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg",
  "assets/img/placeholder.svg"
];

function fillSlider(sliderId, images) {
  const slider = document.getElementById(sliderId);
  if (!slider) return;

  for (let i = 0; i < DUPLICATE_COUNT; i++) {
    images.forEach(src => {
      const img = document.createElement("img");
      img.src = src;
      img.alt = ALT_TEXT;
      img.loading = "lazy";
      slider.appendChild(img);
    });
  }
}

/* INIT SLIDERS */
fillSlider("companySlider", companyImages);
fillSlider("universitySlider", universityImages);

/* ===============================
   STARTUPS (UNCHANGED)
================================ */

const startupGrid = document.getElementById("startupGrid");
if (startupGrid) {
  const startups = [
    {
      src: "assets/img/placeholder.svg",
      link: "https://www.nmotion.in/",
      name: "NAWE ROBOTICS"
    },
    {
      src: "assets/img/placeholder.svg",
      link: "https://www.grafito.in/",
      name: "GRAFITO INNOVATIONS"
    }
  ];

  startups.forEach(startup => {
    const wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.flexDirection = "column";
    wrapper.style.alignItems = "center";
    wrapper.style.gap = "10px";

    const a = document.createElement("a");
    a.href = startup.link;
    a.target = "_blank";

    const img = document.createElement("img");
    img.src = startup.src;
    img.alt = startup.name;

    a.appendChild(img);

    const caption = document.createElement("div");
    caption.textContent = startup.name;
    caption.style.color = "white";
    caption.style.fontSize = "1rem";
    caption.style.textAlign = "center";

    wrapper.appendChild(a);
    wrapper.appendChild(caption);
    startupGrid.appendChild(wrapper);
  });
}
