# ☆ HTML Code Snippets ☆

> "The backbone of the modern web—clean, semantic, accessible, and structured!"

Welcome to the **HTML Code Snippets** directory! This collection contains reusable boilerplate templates, semantic HTML5 layouts, accessible form controls, structured data tables, and multimedia embed guides designed for modern web development, UI prototyping, and front-end engineering.

## ☆ Installation & Prerequisites

HTML is natively parsed and rendered by all modern web browsers. No compilers, runtimes, or external build chains are strictly required to start writing or testing code!

### Quick Setup & Tools

- **Modern Web Browser**: Google Chrome, Mozilla Firefox, Microsoft Edge, or Apple Safari.
- **Recommended Editors & Environments**:
  - **Visual Studio Code** (with extensions like *Live Server*, *HTML CSS Support*, and *Prettier*)
  - **Neovim** / **Sublime Text** / **Visual Studio 2022**
- **Lightweight Local Servers** (Optional for live-reloading or asset testing):
  ```bash
  # Using Python's built-in HTTP server
  python -m http.server 8000

  # Or using Node.js
  npx serve .
  ```

## ☆ Folder Structure

* **_Examples**: Introductory and reference HTML5 snippets demonstrating:
  - `01_boilerplate_and_semantics.html`: Document boilerplate, responsive viewport, metadata, and semantic landmarks (`<header>`, `<nav>`, `<main>`, `<article>`, `<aside>`, `<footer>`).
  - `02_text_and_lists.html`: Inline typographic formatting, code formatting, ordered/unordered lists, and description lists.
  - `03_forms_and_inputs.html`: Accessible forms with `<fieldset>`, `<legend>`, validation attributes, datalists, and various input types.
  - `04_tables.html`: Tabular data presentation with `<caption`, `<thead>`, `<tbody>`, `<tfoot>`, scoped headers, and cell spanning.
  - `05_multimedia_and_embeds.html`: Accessible images, `<figure>` & `<figcaption>`, native `<audio>` & `<video>`, inline SVGs, and sandboxed `<iframe>` elements.

## ☆ Usage

You can open any `.html` snippet directly in your browser by double-clicking it, or view it with VS Code's Live Server extension.

### Example Usage

Basic modern HTML5 semantic layout structure:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="A clean, semantic HTML5 template.">
    <title>Semantic Page Layout</title>
  </head>
  <body>
    <header>
      <h1>Site Title</h1>
      <nav>
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#about">About</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <article>
        <h2>Article Heading</h2>
        <p>Semantic HTML improves accessibility and search engine indexing.</p>
      </article>
    </main>

    <footer>
      <p>&copy; 2026 MelodyHSong. All rights reserved.</p>
    </footer>
  </body>
</html>
```

## ☆ License

This project is licensed under the MIT License. You are free to use, modify, and distribute this code in your own projects— just keep the headers intact!

---

*Always close your tags and don't forget your alt text! — MelodyHSong*
