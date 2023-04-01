import openpyxl
from typing import Dict, List

def read_excel(file_path: str) -> List:
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    tech_data = []
    for row in sheet.iter_rows(min_row=1, values_only=True):
        tech_data.append(row)

    tech_data.sort(key=lambda x: (x[1], x[2], x[0]))
    return tech_data

def generate_option_name(idx: int) -> str:
    option_name = ""
    while idx >= 0:
        option_name = chr(ord("a") + (idx % 26)) + option_name
        idx = idx // 26 - 1
    return option_name

def create_output(tech_data: List) -> Dict[str, str]:
    output = {}
    areas = ['physics', 'society', 'engineering']

    event_id = 10
    for area in areas:
        area_output = ""

        techs_in_area = list(filter(lambda x: x[1] == area, tech_data))
        tiers_in_area = sorted(list(set([tech[2] for tech in techs_in_area])))

        for tier in tiers_in_area:
            if tier == 0:
                continue

            area_output += (
                f"country_event = {{\n"
                f"\tid = gft_tech_trade.{event_id}\n"
                f"\ttitle = gft_tech_trade.{event_id}.name\n"
                f"\tdesc = gft_tech_trade.{event_id}.desc\n"
                "\tpicture = GFX_evt_intelligence_report\n"
                "\tshow_sound = event_activating_unknown_technology\n"
                "\tis_triggered_only = yes\n"
            )

            techs_in_tier = list(filter(lambda x: x[2] == tier, techs_in_area))

            for idx, tech in enumerate(techs_in_tier):
                option_name = generate_option_name(idx)
                area_output += (
                    f"\t# {tech[0]}\n"
                    f"\toption = {{\n"
                    f"\t\tname = gft_tech_trade.{event_id}.{option_name}\n"
                    f"\t\ttrigger = {{\n"
                    f"\t\t\thas_technology = {tech[0]}\n"
                    f"\t\t}}\n"
                    f"\t\thidden_effect = {{\n"
                )

                for i in range(1, 14):
                    if i == 1:
                        condition = "if"
                    else:
                        condition = "else_if"
                    area_output += (
                        f"\t\t\t{condition} = {{\n"
                        f"\t\t\t\tlimit = {{\n"
                        f"\t\t\t\t\thas_country_flag = gft_technology_trade_{i}_country_flag\n"
                        f"\t\t\t\t}}\n"
                        f"\t\t\t\trandom_country = {{\n"
                        f"\t\t\t\t\tlimit = {{\n"
                        f"\t\t\t\t\t\tis_same_empire = event_target:gft_technology_trade_{i}\n"
                        f"\t\t\t\t\t}}\n"
                        f"\t\t\t\t\tcountry_event = {{\n"
                        f"\t\t\t\t\t\tid = gft_tech_trade.1001\n"
                        f"\t\t\t\t\t}}\n"
                        f"\t\t\t\t}}\n"
                        f"\t\t\t}}\n"
                    )

                area_output += "\t\t}\n\t}\n"

            area_output += (
                "\t# 戻る\n"
                f"\toption = {{\n"
                f"\t\tname = gft_tech_trade.9.p\n"
                "\t\thidden_effect = {\n"
                "\t\t\tcountry_event = {\n"
                "\t\t\t\tid = gft_tech_trade.9\n"
                "\t\t\t}\n"
                "\t\t}\n\t}\n"
            )

            area_output += (
                "\t# 閉じる\n"
                f"\toption = {{\n"
                f"\t\tname = gft_tech_trade.8.n\n"
                "\t\thidden_effect = {\n"
                "\t\t\tremove_global_flag = gft_technology_trade_now_global_flag\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_0\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_1\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_2\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_3\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_4\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_5\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_6\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_7\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_8\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_9\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_10\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_11\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_12\n"
                "\t\t\tclear_global_event_target = gft_technology_trade_13\n"
                "\t\t}\n\t}\n}\n"
            )

            event_id += 1

        output[area] = area_output
    return output


def main():
    file_path = "./output.xlsx"
    tech_data = read_excel(file_path)
    area_outputs = create_output(tech_data)

    with open("output.txt", "w", encoding="utf-8") as output_file:
        for area in area_outputs:
            output_file.write(f"# {area}\n{area_outputs[area]}\n")


if __name__ == "__main__":
    main()