import openpyxl

def read_excel(file_path):
  wb = openpyxl.load_workbook(file_path)
  ws = wb.active
  data = []
  for row in ws.iter_rows():
    data.append([cell.value for cell in row])
  return data

def create_output(data):
  template = '''  option = {{
    name = gft_tech_trade.1001.c
    trigger = {{
      has_global_flag = gft_technology_trade_{0}_global_flag
    }}
    allow = {{
      NOT = {{
        has_technology = {0}
      }}
      resource_stockpile_compare = {{
        resource = influence
        value >= 50
      }}
    }}
    add_resource = {{
      influence = -50
    }}
    give_technology = {{
      tech = {0}
    }}
    hidden_effect = {{
      remove_global_flag = gft_technology_trade_{0}_global_flag
      random_country = {{
        limit = {{
          is_same_empire = event_target:gft_technology_trade_0
        }}
        country_event = {{
          id = gft_tech_trade.1002
        }}
      }}
      add_trust = {{
        who = event_target:gft_technology_trade_0
        amount = 50
      }}
    }}
  }}
'''
  output = '''
# 研究取引 贈与 受け取り側
country_event = {
  id = gft_tech_trade.1001
  title = gft_tech_trade.1001.name
  desc = gft_tech_trade.1001.desc
  picture = GFX_evt_intelligence_report
  show_sound = event_activating_unknown_technology
  is_triggered_only = yes'''
  for tech_data in data:
    tech_name, area, tier = tech_data
    if tier != 0:  # tierが0でない場合のみ出力に追加
      output += template.format(tech_name)
  output += '''  option = {
    name = gft_tech_trade.1001.a
    hidden_effect = {'''
  for tech_data in data:
    tech_name, area, tier = tech_data
    if tier != 0:  # tierが0でない場合のみ出力に追加
      output += '''
      if = {{
        limit = {{
          has_global_flag = gft_technology_trade_{0}_global_flag
        }}
        remove_global_flag = gft_technology_trade_{0}_global_flag
      }}'''.format(tech_name)
  output += '''
      random_country = {
        limit = {
          is_same_value = event_target:gft_technology_trade_0
        }
        country_event = {
          id = gft_tech_trade.1003
        }
      }
    }
  }
  option = {
    name = gft_tech_trade.1001.b
    hidden_effect = {
'''
  for tech_data in data:
    tech_name, area, tier = tech_data
    if tier != 0:  # tierが0でない場合のみ出力に追加
      output += '''
      if = {{
        limit = {{
          has_global_flag = gft_technology_trade_{0}_global_flag
        }}
        remove_global_flag = gft_technology_trade_{0}_global_flag
      }}'''.format(tech_name)
  output += '''
      random_country = {
        limit = {
          is_same_value = event_target:gft_technology_trade_0
        }
        country_event = {
          id = gft_tech_trade.1003
        }
      }
    }
  }
}'''
  return output

def main():
  file_path = './output.xlsx'
  data = read_excel(file_path)
  output_text = create_output(data)

  with open('stellaris_event_mod_tool_2.txt', 'w', encoding='utf-8') as f:
    f.write(output_text)

if __name__ == "__main__":
  main()