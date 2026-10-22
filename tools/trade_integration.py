"""Native trade rows. ROOT is the giver and FROM the recipient (Vanilla README).

No selected fleet scope or deal identity is documented for tradable actions.
Do not substitute an arbitrary fleet for that missing context.
"""
from clausewitz import dump

def generate_technology_trade(root, techs, write):
    triggers = '''# Country scope: ROOT = giver, FROM = receiver, per tradable_actions/00_README.txt.
gft_trade_partners_valid = {
 is_country_type = default
 exists = FROM
 FROM = {
  is_country_type = default
  NOT = { is_same_value = ROOT }
 }
 has_communications = FROM
 NOT = { is_at_war_with = FROM }
}
'''
    actions = '# Native trade items. No GUI replacement or saved event target is used.\n'
    for key, tech in sorted(techs.items()):
        check = f'gft_trade_can_give_{key}'
        action = f'gft_trade_{key}'
        triggers += f'''
{check} = {{
 gft_trade_partners_valid = yes
 has_technology = {key}
 FROM = {{
  NOT = {{ has_technology = {key} }}
  {dump(tech['prerequisites'])}
  {dump(tech['potential'])}
 }}
}}
'''
        actions += f'''
{action} = {{
 fire_and_forget = yes
 potential = {{ {check} = yes }}
 possible = {{
  custom_tooltip = {{
   fail_text = gft_trade_technology_invalid
   {check} = yes
  }}
 }}
 on_traded_effect = {{
  if = {{
   limit = {{ {check} = yes }}
   FROM = {{ give_technology = {{ tech = {key} message = no }} }}
  }}
 }}
 # Initial tuning only. Native trade pricing handles the rest of the deal.
 ai_weight = {{ weight = {10 * tech['tier']} }}
}}
'''
    write('common/scripted_triggers/gft_trade_triggers.txt',triggers)
    write('common/tradable_actions/gft_technology_trade.txt',actions)
