import json
import re
import argparse
from bs4 import BeautifulSoup

def parse_legacies(html):
    soup = BeautifulSoup(html, "html.parser")
    legacies = []
    # list of expected factions (both normal and elite)
    factions = [f.lower() for f in ["Fairy", "Elven", "Angel", "Goblin", "Undead", "Demon", "Titan", "Druid", "Faceless", "Dwarven", "Drow", "Dragon", "Archon", "Djinn", "Makers"]]

    # Find all faction section headers (<h6> with an id)
    for h6 in soup.find_all('h6'):
        faction = h6.get('id')
        if not faction or faction.lower() not in factions:
            continue  # skip unrelated h6 sections

        # Initialize a pointer over the siblings until we hit next h6 or an <hr> marker.
        section_elements = []
        current = h6.find_next_sibling()
        while current and current.name not in ['h6', 'hr']:
            if current.name == 'p':
                section_elements.append(current)
            current = current.find_next_sibling()

        # --- Process the lineage for this faction ---
        # We assume that the lineage block comes first (before any perk blocks)
        lineage_tags = []
        i = 0
        while i < len(section_elements):
            text = section_elements[i].get_text().strip()
            # A perk block is usually marked by "Level <number>"
            if re.match(r'^Level\s+\d+', text):
                break
            lineage_tags.append(section_elements[i])
            i += 1

        if lineage_tags:
            lineage = {
                "faction": faction,
                "artifact_type": "lineage"
            }
            # The first tag should include the lineage name (often with an image)
            name_text = lineage_tags[0].get_text().strip()
            lineage["name"] = re.sub(r'\s+', ' ', name_text)
            # Loop over the tags to capture cost and effect(s)
            for tag in lineage_tags:
                txt = tag.get_text().strip()
                if txt.startswith("Cost"):
                    m = re.search(r'Cost\W*:\s*(.*)', txt)
                    if m:
                        lineage["cost"] = m.group(1).strip()
                elif txt.startswith("Effect"):
                    m = re.search(r'Effect\W*:\s*(.*)', txt)
                    if m:
                        lineage.setdefault("effects", []).append(m.group(1).strip())
            legacies.append(lineage)

        # --- Process the perks for this faction ---
        # Each perk block begins with a <p> whose text starts with "Level <number>"
        while i < len(section_elements):
            tag = section_elements[i]
            text = tag.get_text().strip()
            level_match = re.match(r'^Level\s+(\d+)', text)
            if level_match:
                perk = {
                    "faction": faction,
                    "artifact_type": "perk",
                    "level": int(level_match.group(1))
                }
                i += 1
                # Check if the next tag contains a perk name (look for an image tag or typical naming)
                if i < len(section_elements):
                    next_tag = section_elements[i]
                    if next_tag.find('img'):
                        perk_name = next_tag.get_text().strip()
                        perk["name"] = re.sub(r'\s+', ' ', perk_name)
                        i += 1
                    else:
                        perk["name"] = f"{faction} Perk (Level {perk['level']})"
                # Continue reading following tags until the next "Level" marker (or end of section)
                while i < len(section_elements):
                    curr_tag = section_elements[i]
                    curr_text = curr_tag.get_text().strip()
                    if re.match(r'^Level\s+\d+', curr_text):
                        break
                    if curr_text.startswith("Requirement"):
                        m = re.search(r'Requirement\W*:\s*(.*)', curr_text)
                        if m:
                            perk["requirement"] = m.group(1).strip()
                    elif curr_text.startswith("Effect"):
                        m = re.search(r'Effect\W*:\s*(.*)', curr_text)
                        if m:
                            perk.setdefault("effects", []).append(m.group(1).strip())
                    elif curr_text.startswith("Formula"):
                        m = re.search(r'Formula\W*:\s*(.*)', curr_text)
                        if m:
                            perk.setdefault("formula", []).append(m.group(1).strip())
                    elif curr_text.startswith("Challenge"):
                        m = re.search(r'Challenge\W*:\s*(.*)', curr_text)
                        if m:
                            perk["challenge"] = m.group(1).strip()
                    elif curr_text.startswith("Note"):
                        m = re.search(r'Note\W*:\s*(.*)', curr_text)
                        if m:
                            perk.setdefault("notes", []).append(m.group(1).strip())
                    elif curr_text.startswith("Ascension Penalty Reduction Formula"):
                        m = re.search(r'Ascension Penalty Reduction Formula\W*:\s*(.*)', curr_text)
                        if m:
                            perk["ascension_penalty_reduction_formula"] = m.group(1).strip()
                    elif curr_text.startswith("Tier 4 Formula"):
                        m = re.search(r'Tier 4 Formula\W*:\s*(.*)', curr_text)
                        if m:
                            perk["tier_4_formula"] = m.group(1).strip()
                    elif curr_text.startswith("Tier 7 Formula"):
                        m = re.search(r'Tier 7 Formula\W*:\s*(.*)', curr_text)
                        if m:
                            perk["tier_7_formula"] = m.group(1).strip()
                    i += 1
                legacies.append(perk)
            else:
                i += 1

    return legacies

def main():

    try:
        input_file = "../../not-a-wiki/Lineages/index.php"
        with open(input_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        legacies = parse_legacies(html_content)
        # Output the JSON array with indentation for readability
        print(json.dumps(legacies, indent=2))
    except FileNotFoundError:
        print(f"Error: File not found at {input_file}")
        return


if __name__ == "__main__":
    main()
