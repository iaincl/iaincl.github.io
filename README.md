# Iain. (a thought café)

My personal site, built like a little café: projects are cups on a shelf, interests are pastries, and the menu is a receipt.

Live at **https://iaincl.github.io**

## Edit locally

```bash
python3 serve.py
```

Open http://localhost:4321 and press **✎ edit** (top right). Changes preview live, and **save** writes them to `content.json`.
The edit button only appears on localhost, so visitors never see it.

## Structure

- `index.html`: layout, styles and illustrations
- `content.json`: all the words (intro, projects, about, interests, contact)
- `img/`: illustrations and project screenshots
- `serve.py`: local preview server with the save endpoint

## Publish changes

```bash
git add -A && git commit -m "Update content" && git push
```

GitHub Pages redeploys automatically after each push.
