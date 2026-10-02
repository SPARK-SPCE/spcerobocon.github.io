# How to use the components defined in `/src/components` with examples

This document details the process and reference for the HTML components like `navbar`, `footer` and `banner`. This document will be updated as more components are added to the codebase.

* [Component Documentation](#component-documentation)
  * [1. Navigation Bar (`components/navbar.html`)](#1-navigation-bar-componentsnavbarhtml)
  * [2. Site Footer (`components/footer.html`)](#2-site-footer-componentsfooterhtml)
  * [3. Scroll Banner (`components/banner.html`)](#3-scroll-banner-componentsbannerhtml)

## 1. Navigation Bar (`components/navbar.html`)

### Description
This component provides the main site navigation, including a logo, key navigation links, and a "Sponsor US" button. It uses a `dark` class for styling.

### Structure and Features
* **ID**: `navbar`
* **Class**: `dark`
* **Logo**: Links to the home page (`/`) and uses an `<img>` with an inline style for a grayscale/inverted effect.
* **Main Links**: Includes links for About Us, Projects, Achievements, Activities, Team, and Contact.
* **Sponsor Button**: A call-to-action button (`.btn-sponsor`) that pre-fills the `contact/` form with an example sponsorship message.

### Example Usage

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Previous text under <head>... -->
    <link rel="stylesheet" href="/src/styles/navbar.css" /> <!-- Import css file for navbar -->
    <!-- Rest of the text under <head> -->
  </head>

  <body>
    <div id="navbar-placeholder"></div>
    <main>
        <!-- main body code.. -->
    </main>
    <script src="/src/scripts/mobile-navbar.js"></script> <!-- Navbar for mobile layouts -->
    <script src="/src/scripts/componentLoader.js"></script> <!-- Import utility for component loading -->
    
    <script>
      loadComponent("navbar-placeholder", "/src/components/navbar.html");
    </script>
  </body>
</html>
```


## 2. Site Footer (`components/footer.html`)

### Description
A comprehensive footer component containing branding, structured links for club activities and work, social media connections, and a copyright notice.

### Structure and Features
* **ID**: `footer-new`
* **External Dependency**: Requires Font Awesome for social media icons, linked via a CDN: https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css

* **Footer Content**:
    * **Brand**: Displays the logo, name ("SPARK"), and tagline.  
    * **Club Links**: Includes About Us, Team, Contact, and Sitemap.
    * **Work Links**: Includes Projects, Achievements, Activities, and a "Sponsor Us" link with a pre-filled sponsorship enquiry message.
    * **Socials**: Icons linking to Instagram, GitHub, LinkedIn, YouTube, and Blog.
* **Footer Bottom**: Contains the text "No Copyrights Reserved".

### Example Usage

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Previous text under <head>... -->
    <link rel="stylesheet" href="/src/styles/footer.css" /> <!-- Import css file for footer -->
    <!-- Rest of the text under <head> -->
  </head>

  <body>
    <div id="footer-placeholder"></div>
    <main>
        <!-- main body code.. -->
    </main>
    <script src="/src/scripts/componentLoader.js"></script> <!-- Import utility for component loading -->
    
    <script>
      loadComponent("footer-placeholder", "/src/components/footer.html");
    </script>
  </body>
</html>
```


## 3. Scroll Banner (`components/banner.html`)

### Description
This component is designed to display a single, scrolling text link, typically used for site-wide announcements or page-wise notifications. It is built to be dynamically populated using placeholders.

### Customization and Placeholders
The banner uses three primary placeholders that must be replaced by a rendering engine (like a templating language) to display content:

* `{{link}}`: The URL the banner text should link to.
* `{{target}}`: The link's target attribute (e.g., _blank for a new tab).
    * Common target attribute values:
        * `_blank` - Opens the link in a new tab or window
        * `_self` - Opens the link in the same frame (default behavior)
        * `_parent` - Opens in the parent frame
        * `_top` - Opens in the full body of the window 
        * `framename` - Opens in a named iframe
* `{{text}}`: The actual text content that will scroll within the banner.

### Example Usage

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Previous text under <head>... -->
    <link rel="stylesheet" href="/src/styles/banner.css" /> <!-- Import css file for banner -->
    <!-- Rest of the text under <head> -->
  </head>

  <body>
    <div id="navbar-placeholder"></div>
    <div id="banner-placeholder"></div> <!-- Placeholder for banner UNDER NAVBAR! -->
    <main>
        <!-- main body code.. -->
    </main>
    <script src="/src/scripts/componentLoader.js"></script> <!-- Import utility for component loading -->
    
    <script>
      loadComponent("banner-placeholder", "/src/components/banner.html", {
        link: "https://spark.com/activities/origo/",
        text: "ORIGO Robotics Challenge'25 — View the Challenge Overview and Guidelines <u>here</u>",
        target: "_blank"
      });
    </script>
  </body>
</html>
```