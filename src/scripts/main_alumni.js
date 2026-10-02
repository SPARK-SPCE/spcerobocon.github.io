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

/* ===============================
   OUR HIGHLIGHTS
   (replaces "Startups from our Lab")
================================ */

const startupGrid = document.getElementById("startupGrid");
if (startupGrid) {
  // Change heading text
  const startupHeader = document.querySelector(".startup-header");
  if (startupHeader) startupHeader.textContent = "Our Highlights";

  const highlights = [
    { icon: "🥇", name: "AIR 4",            desc: "Best National Rank — DD Robocon 2015" },
    { icon: "🌐", name: "International Rank 2", desc: "IIT Bombay IRC 2018" },
    { icon: "📄", name: "Best Tech Report",  desc: "100/100 Score — DD Robocon 2020" },
    { icon: "🏆", name: "Podium Sweep",      desc: "Rank 1, 2 & 3 — FCRCE Roborift 2025" },
  ];

  highlights.forEach(h => {
    const wrapper = document.createElement("div");
    wrapper.style.cssText = "display:flex;flex-direction:column;align-items:center;gap:10px;padding:1.5rem;background:rgba(255,255,255,0.04);border-radius:12px;border:1px solid rgba(255,255,255,0.08);";
    wrapper.innerHTML = `
      <div style="font-size:2.5rem;">${h.icon}</div>
      <div style="color:white;font-size:1.1rem;font-weight:700;text-align:center;">${h.name}</div>
      <div style="color:#aaa;font-size:0.85rem;text-align:center;">${h.desc}</div>
    `;
    startupGrid.appendChild(wrapper);
  });
}
