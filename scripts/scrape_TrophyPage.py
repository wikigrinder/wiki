import json
from bs4 import BeautifulSoup

def parse_trophy_details(research_html):
    """
    Parse the trophy's HTML snippet (from the research attribute) to extract:
      - name (first bold text not matching a known field label)
      - requirement, cost, effects, formula, notes, and tips.
    """
    soup = BeautifulSoup(research_html, 'html.parser')
    trophy = {}

    # Known labels to ignore when finding the trophy name
    known_labels = {"Requirement", "Cost", "Effect", "Effects", "Formula", "Note", "Notes", "Tip", "Tips", "Alignments", "Requirements"}
    
    # Find trophy name from the first <b> tag not in known labels
    trophy_name = None
    for b in soup.find_all('b'):
        text = b.get_text(strip=True)
        if text not in known_labels:
            trophy_name = text
            break
    trophy['name'] = trophy_name if trophy_name else "Unknown Trophy"
    
    # Initialize other fields
    trophy['requirement'] = ""
    trophy['cost'] = ""
    trophy['effects'] = []
    trophy['formula'] = ""
    trophy['notes'] = []
    trophy['tips'] = []

    # Process each <p> tag to extract labeled fields
    p_tags = soup.find_all('p')
    for p in p_tags:
        bold = p.find('b')
        if bold:
            label = bold.get_text(strip=True).rstrip(":")
            # Get the full text and remove the label part
            full_text = p.get_text(separator=" ", strip=True)
            if full_text.startswith(label):
                value = full_text[len(label):].lstrip(": ").strip()
            else:
                value = full_text
            # Store value based on label (case-insensitive)
            if label.lower() == "requirement":
                trophy['requirement'] = value
            elif label.lower() == "cost":
                trophy['cost'] = value
            elif label.lower() in {"effect", "effects"}:
                trophy['effects'].append(value)
            elif label.lower() == "formula":
                trophy['formula'] = value
            elif label.lower() in {"note", "notes"}:
                trophy['notes'].append(value)
            elif label.lower().startswith("tip"):
                trophy['tips'].append(value)
    return trophy

def parse_trophies(html_content):
    """
    Parse all <area> tags in the HTML file and extract trophy details.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    trophies = []
    for area in soup.find_all('area'):
        research_html = area.get('research')
        if research_html:
            trophy = parse_trophy_details(research_html)
            trophies.append(trophy)
    return trophies

def main():
    input_file = "../../not-a-wiki/TrophyPage/index.php"
    with open(input_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    trophies = parse_trophies(html_content)
    # Output the JSON array with indentation for readability
    print(json.dumps(trophies, indent=4))

if __name__ == "__main__":
    main()