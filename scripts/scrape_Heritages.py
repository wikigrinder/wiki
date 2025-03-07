import json
import argparse
from bs4 import BeautifulSoup

def parse_heritages(html):
    soup = BeautifulSoup(html, "html.parser")
    heritages = []

    # Define sets for regular heritage IDs and advanced heritage IDs
    regular_ids = {
        "FRH", "ELH", "ANH", "GBH", "UDH", "DMH", "TTH",
        "DDH", "FCH", "DNH", "DWH", "MCH", "DGH", "ARH", "DJH", "MKH"
    }
    advanced_ids = {
        "FRAH", "ELAH", "ANAH", "GBAH", "UDAH", "DMAH",
        "TTAH", "DDAH", "FCAH", "DNAH", "DWAH", "DGAH"
    }

    # Find each <p> tag with an id attribute (each marks the start of an entry)
    for p_tag in soup.find_all("p", id=True):
        tag_id = p_tag["id"].strip()
        # Only process IDs that are in our defined sets
        if tag_id not in regular_ids and tag_id not in advanced_ids:
            continue

        # Determine if this is an advanced heritage (or a perk)
        advanced = tag_id in advanced_ids

        # Extract the heritage name from the <b> tag inside the <p>
        b_tag = p_tag.find("b")
        name = b_tag.get_text(strip=True) if b_tag else p_tag.get_text(strip=True)

        entry = {
            "name": name,
            "advanced": advanced
        }
        # Set a "type": if the name includes "Advanced" mark it as advanced heritage;
        # if it contains "Badge" mark it as a perk; otherwise regular heritage.
        if "Advanced" in name:
            entry["type"] = "advanced heritage"
        elif "Badge" in name:
            entry["type"] = "perk"
        else:
            entry["type"] = "heritage"

        # Derive the faction name by removing "Advanced" (if present) and taking the first word.
        words = name.split()
        if words[0] == "Advanced":
            faction = words[1]
        else:
            faction = words[0]
        entry["faction"] = faction.lower()

        # Initialize a dictionary for additional details (e.g., cost, requirements, effect, formula)
        details = {}
        for sibling in p_tag.find_next_siblings():
            # Stop when reaching a <br/> tag or a new entry (indicated by a <p> tag with an id)
            if sibling.name == "br":
                break
            if sibling.name == "p" and sibling.has_attr("id"):
                break
            if sibling.name == "p":
                text = sibling.get_text(separator=" ", strip=True)
                if ":" in text:
                    key, value = text.split(":", 1)
                    details[key.strip().lower()] = value.strip()
        entry.update(details)
        heritages.append(entry)
    
    return heritages


def main():

    try:
        input_file = "../../not-a-wiki/Heritages/index.php"
        with open(input_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        parsed_heritages = parse_heritages(html_content)
        # Output the JSON array with indentation for readability
        print(json.dumps(parsed_heritages, indent=2))
    except FileNotFoundError:
        print(f"Error: File not found at {input_file}")
        return


if __name__ == "__main__":
    main()