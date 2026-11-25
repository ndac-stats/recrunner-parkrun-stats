# Updating this Project

## Updating the Results
Due to parkrun's anti-bot measures, running the scripts via GitHub Actions was not viable (requesting websites return 405 and a page requiring human verification). Instead, the script can be run on a local device, and results pushed to the repository. This guide has been written assuming the use of [`uv`](https://docs.astral.sh/uv/).  
```bash
uv sync
uv run src/ndac_parkrun_results/main.py

git add data/results.json
git commit -m "chore: parkrunner results updated"
git push
```

## Updating the Website
The workflow defined at `.github/workflows/update-website.yml` is set to update the website whenever `data/results.json` is updated. It can also be manually triggered by going to `Actions → pages-build-deployment → Run workflow`.