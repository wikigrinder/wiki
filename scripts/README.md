# Scripts to generate sources

These are the scripts you can use to generate the sources in the `json` folder.
The purpose of these is so you can modify the scripts as needed to enhance the structure of JSON data to make creating the new website easier.

# Requirements
- Python
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/): `pip install beautifulsoup4`

# How to run the script

Each script assumes the not-a-wiki repo is cloned and in the same directory as the wikigrinder repo.

With that in mind, if you are in the `scripts` you can run the following command for each script:

- scrape_TrophyPage.py: ` python scrape_TrophyPage.py > ../json/trophies.json`
- scrape_Artifacts.py:  `python scrape_Artifacts.py > ../json/artifacts.json`
- scrape_Legacies.py: `python .\scrape_Legacies.py > ../json/legacies.json`
- ??

# Known Issues
- effect on artifacts needs work

# Improvements
- add a parent label to each file (e.g. for trophies.json the array should be inside an element called trophies)