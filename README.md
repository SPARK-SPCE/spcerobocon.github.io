# Website Repository 

This repository contains the source code for a multi-page website with sections for **About**, **Achievements**, **Activities**, **Projects**, **Team**, and **Contact**. The website includes interactive features, animations, and modular assets.


---

## Directory Structure

```
C:.
├── assets
│   └── fonts
│   └── images
├───docs
├── src
│   ├── components
│   ├── data
│   │   ├── achievements
│   │   ├── activities
│   │   ├── projects
│   │   └── team
│   ├── pages
│   │   ├── about
│   │   ├── achievements
│   │   ├── activities
│   │   │   └── origo
│   │   ├── contact
│   │   ├───hof
│   │   ├── projects
│   │   └── team
│   ├── scripts
│   └── styles
├── test
└── utils
```

- **Each folder contains its own `index.html`**.
- **`test/`** is for testing small features, experimental code, or transitions.
- **`assets/`** contains CSS and image assets, organized by purpose.

---

## Current Status

- **Refactoring of codebase:** Done

  - Easier to maintain
  - Clear separation of JS and CSS
  - Component based system
  - Common footer in all pages
  - Mobile navbar now consistent
  - Proper CI/CD

---

## Development Guidelines

### Adding New Companies

- Add images to `/assets/images/companies/`.
- Update the main page HTML to reference these images.
- Avoid hardcoding paths multiple times; keep it consistent.

### Projects Management

- Maintain `.json` files in `src/data` neatly.
- Ensure new projs are added consistently.

### UI/UX Guidelines

- Improve UI where needed; remove anything that feels “cringe”.
- Maintain consistency with colors and layout, especially for spline scenes.
- Hidden watermarks have been masked with background colors—avoid disturbing this.

---

## Notes

- All images are in `/assets/images/`; refer only to these paths.
- Small experiments, UI prototypes, and feature tests should go in `test/`.
- Keep the repository modular and maintainable.

---

## Future Work

- Add more company logos and gallery photos.
- Maintain a black-and-white theme only and improve the overall UI.
- Try cleaning up the CSS to make it minimal
- Find better font, make it consistent site-wide.
