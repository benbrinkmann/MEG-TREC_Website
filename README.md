# MEG-TREC Website

Static website for the MEG Translational Research Consortium (MEG-TREC), formerly the MEG Texas Consortium. Hosted on GitHub Pages. The page structure is adapted from the Northwoods Cabin site.

## File Structure

```
MEG-TREC_Website/
├── index.html      # Home: overview, focus areas, most recent meeting
├── about.html      # Mission, history, activities
├── board.html      # Board members
├── meetings.html   # Annual meetings (newest first)
├── meg.html        # Educational resource: MEG principles and techniques
├── style.css       # Shared stylesheet (colors and fonts set in :root)
├── site.js         # Shared script: mobile menu, fade-ins, sidebar highlighting
├── images/
│   ├── dipole-map.png   # 3D dipole field map (home page)
│   ├── meg-system.jpg   # MEG system photo (add; drawing shows until then)
│   └── board/           # Board headshots, see images/board/README.md
├── tools/
│   └── make_dipole_map.py  # Regenerates images/dipole-map.png
├── .nojekyll       # Tells GitHub Pages to serve files as is
└── README.md
```

No build step is needed; every page is plain HTML.

## Common Edits

- **Navigation or footer:** these blocks are repeated in every HTML file. Change all five files when adding a page or link.
- **Colors and fonts:** edit the tokens at the top of `style.css`.
- **Board members:** copy one `<article class="member">` block in `board.html`.
- **Meetings:** copy one `<article class="meeting">` block to the top of the list in `meetings.html`, and update the "Annual Meeting" section on `index.html`.
- **Education page references:** numbered `<sup class="ref">` links in `meg.html` point to items `ref1`, `ref2`, etc. in the reference list at the bottom of that page.

## Items to Fill In

- Contact email for the consortium (none is listed yet).
- Dates and location of the next annual meeting.
- MEG system photo saved as `images/meg-system.jpg`, with a photo credit in the caption on `index.html`.
- Board headshots in `images/board/` (file names listed in that folder's README).
- A logo, if one exists; the site currently uses a text wordmark and an inline SVG favicon.

## Deployment on GitHub Pages

1. In the repository, open **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**, branch `main`, folder `/ (root)`.
3. The site will be published at `https://benbrinkmann.github.io/MEG-TREC_Website/`.
4. A custom domain can be added on the same settings page.

## Local Preview

Open `index.html` in a browser, or run `python3 -m http.server` in this folder and visit `http://localhost:8000`.

## Content Sources

- Le Bonheur Children's Hospital, 4th Annual MEG-TREC meeting page
- UF Health Norman Fixel Institute, "Highlights from MEG-TREC 2025"
- MEG-TREC 2025 meeting site (Google Sites)
