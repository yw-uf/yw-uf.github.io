# Embodied Intelligence Lab · Yu Wang

Minimal lab website with four separate pages: PI (index.html), Research, Teaching, and Team, built for GitHub Pages. Each tab displays its content directly without subtabs or collapsed biographies. Lists use one column. Research has three themes with conceptual illustrations, full CV-based citations, and a Google Scholar link. Team and PI pages contain no portraits. No npm packages or Python dependencies required.

## Preview locally

For a preview server that runs independently of the chat terminal, run:

```powershell
powershell -File scripts/preview.ps1
```

The server runs hidden in the background until stopped or the computer restarts. Running the launcher again rebuilds the site and reuses the server if it is already running.

To run the server in a terminal instead:

```powershell
python scripts/build.py
python scripts/check_site.py
python -m http.server 8000 --directory _site
```

Open http://localhost:8000. Edit source files, then rerun the build to see changes.

## Maintain content

- `content/site.json`: people, biographies, publication citations and links, research descriptions, and news. Move a person to alumni by changing their `group` to `Alumni`; update their role and biography too.
- `content/research.json`: three research themes, selected recent papers, illustration paths, and sponsors.
- `scripts/build.py`: homepage, Yu Wang's profile, education, teaching, common header/footer, and page templates.
- `assets/style.css`: visual design and responsive layouts.
- `assets/research/`: generated conceptual illustrations and their prompts.
- `assets/sponsors/`: sponsor logos and source information.
- `assets/images/`: original imported assets retained for reference; excluded from the deployed site.
- `assets/site.js`: mobile navigation and publication search/filtering.

The build produces `_site/`, which is the only directory deployed. Relative URLs support both project sites and root-level GitHub Pages sites. All content is in the generated HTML, so navigation and reading work without JavaScript.

## Publish on GitHub

1. Review the CV-based roster and selected paper statuses in the content files.
2. Commit and push the source to `main` in `yw-uf/yw-uf.github.io`.
3. Open repository **Settings → Pages** and select **GitHub Actions** under **Build and deployment → Source**.
4. Run **Actions → Publish website → Run workflow** if the initial push happened before Pages was enabled.
5. Check the workflow's deployment URL and verify the live pages.

The live website is https://yw-uf.github.io/, hosted under Yu Wang's personal GitHub account `yw-uf` in repository `yw-uf.github.io`. The local Git remote points to https://github.com/yw-uf/yw-uf.github.io.git.

After the new site is live, add a link or migration notice to the Google Sites page and UF lab website. GitHub cannot configure redirects on those existing hosts; update them using their own editors.

## Migration sources

Imported October 3, 2026 from the user-supplied websites:

- https://sites.google.com/view/y-wang
- https://faculty.eng.ufl.edu/smart-autonomy-lab/people/
- https://faculty.eng.ufl.edu/smart-autonomy-lab/research/
- https://faculty.eng.ufl.edu/smart-autonomy-lab/publications/
- https://faculty.eng.ufl.edu/smart-autonomy-lab/lab-news/

The original import contains 42 publication entries and 13 news announcements, retained in the source data for reference. The roster displays 15 people, updated from the supplied CV, factual project descriptions, and explicit roster corrections. The undergraduate section shows “To be updated.”; its previous entries remain in the source data. Noah A. Touchton and Audley Tchatcheun appear under Alumni. Research highlights use recent work from the CV. News and the legacy publications archive are not generated as website pages. Recommendation letters are not included in the repository or build output.

Raw downloaded source pages stay in ignored `migration/sources/` for comparison. `scripts/import_content.py` is a one-time migration utility; running it again overwrites content edits. `migration/assets.json` records the original image URLs. The supplied CV stays outside the repository.



