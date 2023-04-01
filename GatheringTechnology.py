import os
import re
import pandas as pd
from tkinter import Tk, filedialog

def select_folder():
  root = Tk()
  root.withdraw()  # Tkウィンドウを非表示にする
  folder_path = filedialog.askdirectory(title="Select the folder containing the technology files")
  return folder_path

def select_output_file():
  root = Tk()
  root.withdraw()  # Tkウィンドウを非表示にする
  output_file = filedialog.asksaveasfilename(
    title="Select the output Excel file",
    defaultextension=".xlsx",
    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
    initialfile="output.xlsx"
  )
  return output_file

def read_files(folder_path):
  files_data = []

  for file in os.listdir(folder_path):
    if file.endswith(".txt"):
      with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
        files_data.append(f.read())

  return files_data

def extract_data(files_data):
  extracted_data = []

  for data in files_data:
    tech_blocks = data.split("}\n")

    for tech_block in tech_blocks:
      if not tech_block.startswith("#"):  # コメント化されたブロックを無視
        name_match = re.search(r"(tech_\w+)", tech_block)
        area_match = re.search(r"area\s*=\s*(\w+)", tech_block)
        tier_match = re.search(r"tier\s*=\s*(\d+)", tech_block)

        if name_match and area_match and tier_match:
          name = name_match.group(1)
          area = area_match.group(1)
          tier = int(tier_match.group(1))

          if tier != 0:
            extracted_data.append([name, area, tier])

  return extracted_data

def write_to_excel(extracted_data, output_file):
  df = pd.DataFrame(extracted_data, columns=["name", "area", "tier"])
  df = df.sort_values(by=["area", "tier", "name"])  # area, tier, nameの順でソート
  df.to_excel(output_file, index=False)

folder_path = select_folder()
output_file = select_output_file()

files_data = read_files(folder_path)
extracted_data = extract_data(files_data)
write_to_excel(extracted_data, output_file)
