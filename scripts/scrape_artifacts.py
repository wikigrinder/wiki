#!/usr/bin/env python3
import json
from bs4 import BeautifulSoup

def parse_artifact(research_html):
    artifact = {}
    # Parse the research attribute HTML snippet
    snippet = BeautifulSoup(research_html, "html.parser")
    p_tags = snippet.find_all("p")
    if not p_tags:
        return artifact

    # The first <p> is assumed to contain the artifact name (after an <img> if present)
    first_b = p_tags[0].find("b")
    if first_b:
        # Remove any image tags so that only text remains
        for img in first_b.find_all("img"):
            img.decompose()
        artifact["name"] = first_b.get_text(strip=True)
    
    # Process the remaining paragraphs for other fields
    for p in p_tags[1:]:
        b_tag = p.find("b")
        if not b_tag:
            continue
        # Field name from the bold tag (remove trailing colon if any)
        field_name = b_tag.get_text(strip=True).rstrip(":").lower()
        # Get the full text of the paragraph; then remove the field name portion
        full_text = p.get_text(" ", strip=True)
        # Remove the field name and colon from the beginning if present
        value = full_text[len(b_tag.get_text(strip=True)):]
        if value.startswith(":"):
            value = value[1:]
        value = value.strip()
        
        # For fields that may occur multiple times (like Effect), accumulate into a list
        if field_name == "effect":
            if "effects" not in artifact:
                artifact["effects"] = []
            artifact["effects"].append(value)
        else:
            artifact[field_name] = value

    return artifact

def main():
    # Read the HTML file that contains both Quest and Lore artifacts
    with open("Artifacts_index.php", "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    artifacts = []
    
    # The file includes two <map> elements with names like "QuestArtifacts-map" and "LoreArtifacts-map"
    # We assume that each <area> element with a "research" attribute contains one artifact's details.
    for area in soup.find_all("area"):
        research = area.get("research")
        if research:
            artifact = parse_artifact(research)
            if artifact:
                artifacts.append(artifact)
    
    # Output the JSON array with pretty-print formatting
    print(json.dumps(artifacts, indent=2))

if __name__ == "__main__":
    main()
