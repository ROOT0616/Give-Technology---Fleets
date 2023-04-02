import re
import os

def read_event_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content

def extract_event_details(event_content):
    title_pattern = r"title\s*=\s*(gft_tech_trade\.\d+\.name)"
    desc_pattern = r"desc\s*=\s*(gft_tech_trade\.\d+\.desc)"
    option_pattern = r"name\s*=\s*(gft_tech_trade\.\d+\.[a-z]+)"
    technology_pattern = r"has_technology\s*=\s*(tech_[\w_]+)"

    title = re.search(title_pattern, event_content).group(1)
    desc = re.search(desc_pattern, event_content).group(1)
    options = re.findall(option_pattern, event_content)
    technologies = re.findall(technology_pattern, event_content)

    return title, desc, options, technologies

def is_ignored_option(option):
    ignored_options = ["gft_tech_trade.9.p", "gft_tech_trade.8.n"]
    return option in ignored_options

def create_output(title, desc, options, technologies):
    output = []
    output.append(f"{title}:0 \"研究取引 贈与 物理学tier1\"")

    tech_index = 0
    for option in options:
        if not is_ignored_option(option):
            output.append(f"{option}:0 \"§Y${technologies[tech_index]}$§!\"")
            tech_index += 1

    return "\n".join(output)

def save_output(output_text, file_path):
    with open(file_path, "w", encoding="utf-8-sig") as file:
        file.write(output_text)

def main():
    event_file_path = "./GFT_tech_trade_event_1.txt"
    output_file_path = "GFT_l_japanese_1.yml"

    event_content = read_event_file(event_file_path)
    title, desc, options, technologies = extract_event_details(event_content)
    output_text = create_output(title, desc, options, technologies)
    
    save_output(output_text, output_file_path)
    print(f"Output saved to {output_file_path}")

if __name__ == "__main__":
    main()
