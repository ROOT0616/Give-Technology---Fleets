"""Generate gift menus from a supplied target-version Vanilla common directory.

Usage: python tools/generate.py /path/to/vanilla
Vanilla is read only. No automatic download or guessed script hooks.
"""
from pathlib import Path
import collections
import json
import re
import sys
from clausewitz import Entry, parse, get, dump

ROOT = Path(__file__).resolve().parents[1]
VERSION = '3.0.0-beta.2'

def write(path, text, bom=False):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    cleaned = '\n'.join(line.rstrip() for line in text.splitlines()).rstrip() + '\n'
    target.write_text(cleaned, encoding='utf-8-sig' if bom else 'utf-8', newline='\n')

def event(ns, number, title, desc, body, immediate=''):
    return f'''country_event = {{
 id = {ns}.{number}
 title = {title}
 desc = {desc}
 picture = GFX_evt_fleet_neutral
 is_triggered_only = yes
 {('immediate = { ' + immediate + ' }') if immediate else ''}
 {body}
}}
'''

def option(name, effect='', trigger='', chance=''):
    return f'''option = {{
 name = {name}
 {('trigger = { ' + trigger + ' }') if trigger else ''}
 {('hidden_effect = { ' + effect + ' }') if effect else ''}
 {('ai_chance = { factor = ' + chance + ' }') if chance else ''}
}}'''

def call(ns, n):
    return f'country_event = {{ id = {ns}.{n} }}'

def sender_ok():
    # Conservative restriction: no unverified shared-fleet ownership hook.
    return 'is_country_type = default is_federation_leader = no is_galactic_custodian = no is_galactic_emperor = no'

def prerequisite_conditions(entries):
    """Preserve current Vanilla OR groups, including multiple groups in one list."""
    result = []
    for e in entries:
        if not e.op:
            result.append(Entry('has_technology', '=', e.key.strip('"')))
        elif e.key == 'OR' and isinstance(e.value, list):
            result.append(Entry('OR', '=', prerequisite_conditions(e.value)))
        else:
            raise ValueError('Unreviewed prerequisite syntax: ' + dump([e]))
    return result

def country_menu(ns, next_id):
    init = 'save_event_target_as = gft_donor\n'
    for i in range(1, 14):
        init += f'save_event_target_as = gft_country_{i}\n'
    for i in range(1, 14):
        exclude = ' '.join(f'NOT = {{ is_same_value = event_target:gft_country_{j} }}' for j in range(1, i))
        init += f'''random_country = {{ limit = {{
 gft_recipient_valid = yes {exclude}
 }} save_event_target_as = gft_country_{i} }}\n'''
    opts = []
    for i in range(1, 14):
        opts.append(option(f'gft_country_{i}', f'event_target:gft_country_{i} = {{ save_event_target_as = gft_recipient }} ' + call(ns, next_id),
            f'event_target:gft_country_{i} = {{ gft_recipient_valid = yes }}'))
    opts += [option('gft_refresh', call(ns, 1)), option('gft_close')]
    return event(ns, 1, 'gft_country_title', 'gft_country_desc', '\n'.join(opts), init)

def main(vanilla):
    techs = {}
    excluded = {}
    for path in sorted((vanilla / 'common/technology').glob('*.txt')):
        for entry in parse(path.read_text(encoding='utf-8-sig')):
            if not entry.key.startswith('tech_') or not isinstance(entry.value, list): continue
            if entry.key in techs or entry.key in excluded: raise ValueError('Duplicate technology ' + entry.key)
            body = entry.value
            area, tier = get(body, 'area'), get(body, 'tier')
            potential = get(body, 'potential', [])
            reason = None
            if area not in ('physics', 'society', 'engineering') or tier not in ('1','2','3','4','5'):
                reason = 'outside areas/tier 1-5'
            elif get(body, 'levels', '1') != '1': reason = 'repeatable'
            elif get(body, 'start_tech') == 'yes': reason = 'starting technology'
            elif get(body, 'weight') == '0': reason = 'event/special technology (base weight 0)'
            elif re.search(r'\b(root|from|fromfrom|prev|prevprev|event_target)\b', dump(potential), re.I):
                reason = 'context-dependent potential needs manual review'
            if reason:
                excluded[entry.key] = reason
            else:
                techs[entry.key] = {'area':area, 'tier':int(tier), 'potential':potential,
                    'prerequisites':prerequisite_conditions(get(body,'prerequisites',[])),
                    'source':path.relative_to(vanilla).as_posix()}
    if not techs: raise ValueError('No technology definitions found')
    triggers = '''# Country scope: candidate recipient; donor is a chain-local country target.
gft_recipient_valid = {
 exists = event_target:gft_donor
 is_country_type = default
 NOT = { is_same_value = event_target:gft_donor }
 has_communications = event_target:gft_donor
 NOT = { is_at_war_with = event_target:gft_donor }
 event_target:gft_donor = { is_country_type = default }
}

# Fleet scope. Special political fleet owners are excluded conservatively.
gft_fleet_valid = {
 exists = event_target:gft_donor
 is_ship_class = shipclass_military
 is_mobile = yes
 is_leased = no
 is_in_combat = no
 owner = { is_same_value = event_target:gft_donor }
 event_target:gft_donor = { SENDER_OK }
}
'''.replace('SENDER_OK', sender_ok())
    catalog = []
    groups = collections.defaultdict(list)
    for i, (key, tech) in enumerate(sorted(techs.items()), 20000):
        groups[(tech['area'],tech['tier'])].append((key,i))
        prerequisites = dump(tech['prerequisites'])
        triggers += f'''\n# Recipient country scope; copied potential is evaluated for the recipient.
gft_receive_{key} = {{
 gft_recipient_valid = yes
 NOT = {{ has_technology = {key} }}
 event_target:gft_donor = {{ has_technology = {key} }}
 {prerequisites}
 {dump(tech['potential'])}
}}
'''
        catalog.append({'id':key,'area':tech['area'],'tier':tech['tier'],'trade_action':'gft_trade_'+key,'offer_event':f'gft_tech_trade.{i}','source':tech['source']})

    ns = 'gft_tech_trade'
    events = 'namespace = gft_tech_trade\n# Generated by tools/generate.py; do not edit generated menus.\n' + country_menu(ns,2)
    group_options = []
    menu_events = ''
    for gi, ((area,tier), items) in enumerate(sorted(groups.items()), 10):
        pages = [items[n:n+12] for n in range(0,len(items),12)]
        menu_base = 10000 + gi * 100
        group_options.append(option(f'gft_{area}_{tier}',call(ns,menu_base)))
        for pi, page in enumerate(pages):
            opts = []
            for key, eid in page:
                opts.append(option(key, f'event_target:gft_recipient = {{ {call(ns,eid)} }}',
                    f'event_target:gft_recipient = {{ gft_receive_{key} = yes }}'))
            if pi: opts.append(option('gft_previous',call(ns,menu_base+pi-1)))
            if pi+1<len(pages): opts.append(option('gft_next',call(ns,menu_base+pi+1)))
            opts += [option('gft_back',call(ns,2)),option('gft_close')]
            menu_events += event(ns,menu_base+pi,f'gft_{area}_{tier}','gft_tech_desc','\n'.join(opts))
    group_options += [option('gft_back',call(ns,1)),option('gft_close')]
    events += event(ns,2,'gft_tech_title','gft_tech_desc','\n'.join(group_options)) + menu_events
    for row in catalog:
        key, eid = row['id'], int(row['offer_event'].split('.')[1])
        notify = f'event_target:gft_donor = {{ {call(ns,1002)} }}'
        grant = f'give_technology = {{ tech = {key} message = no }} {notify}'
        accept = option('gft_accept',f'if = {{ limit = {{ gft_receive_{key} = yes }} {grant} }}', f'gft_receive_{key} = yes','10')
        refuse = option('gft_decline',f'if = {{ limit = {{ exists = event_target:gft_donor }} event_target:gft_donor = {{ {call(ns,1003)} }} }}',chance='1')
        events += event(ns,eid,key,'gft_offer_tech_desc',accept+'\n'+refuse)
    events += event(ns,1002,'gft_accepted','gft_tech_accepted_desc',option('gft_close'))
    events += event(ns,1003,'gft_declined','gft_declined_desc',option('gft_close'))
    write('events/GFT_tech_trade_event.txt',events)
    write('common/scripted_triggers/gft_gift_triggers.txt',triggers)

    ns = 'gft_fleet_trade'
    events = 'namespace = gft_fleet_trade\n' + country_menu(ns,2)
    # Seed all slots from one eligible fleet. Remaining draws replace slots with
    # distinct fleets. Duplicate seed slots are hidden, avoiding undefined scopes.
    init = 'random_owned_fleet = { limit = { gft_fleet_valid = yes }\n'
    for i in range(1,11): init += f'save_event_target_as = gft_fleet_slot_{i}\n'
    init += '}\n'
    for i in range(2,11):
        exclude = ' '.join(f'NOT = {{ is_same_value = event_target:gft_fleet_slot_{j} }}' for j in range(1,i))
        init += f'random_owned_fleet = {{ limit = {{ gft_fleet_valid = yes {exclude} }} save_event_target_as = gft_fleet_slot_{i} }}\n'
    opts=[]
    for i in range(1,11):
        unique = ' '.join(f'NOT = {{ is_same_value = event_target:gft_fleet_slot_{j} }}' for j in range(1,i))
        trigger = f'''exists = event_target:gft_fleet_slot_{i}
 event_target:gft_recipient = {{ gft_recipient_valid = yes }}
 event_target:gft_fleet_slot_{i} = {{ gft_fleet_valid = yes {unique} }}'''
        effect = f'''event_target:gft_fleet_slot_{i} = {{ save_event_target_as = gft_offered_fleet }}
 event_target:gft_recipient = {{ {call(ns,3)} }}'''
        opts.append(option(f'gft_fleet_slot_{i}',effect,trigger))
    opts += [option('gft_refresh',call(ns,2)),option('gft_back',call(ns,1)),option('gft_close')]
    events += event(ns,2,'gft_fleet_title','gft_fleet_desc','\n'.join(opts),init)
    valid = '''gft_recipient_valid = yes exists = event_target:gft_offered_fleet
 event_target:gft_offered_fleet = { gft_fleet_valid = yes }'''
    transfer = '''event_target:gft_offered_fleet = {
 if = { limit = { exists = leader } leader = { unassign_leader = this } }
 set_owner = root
 set_controller = root
 } event_target:gft_donor = { country_event = { id = gft_fleet_trade.4 } }'''
    accept = option('gft_accept',f'if = {{ limit = {{ {valid} }} {transfer} }}',valid,'10')
    refuse = option('gft_decline',f'if = {{ limit = {{ exists = event_target:gft_donor }} event_target:gft_donor = {{ {call(ns,5)} }} }}',chance='1')
    events += event(ns,3,'gft_fleet_offer_title','gft_offer_fleet_desc',accept+'\n'+refuse)
    events += event(ns,4,'gft_accepted','gft_fleet_accepted_desc',option('gft_close'))
    events += event(ns,5,'gft_declined','gft_declined_desc',option('gft_close'))
    write('events/GFT_fleet_trade_event.txt',events)
    edicts=''
    # Old technology events remain for beta.1 saves/console testing, but have no edict entry.
    for key,ns in [('fleet','gft_fleet_trade')]:
        edicts+=f'''gft_{key}_trade_options_menu = {{
 length = 0
 icon = "GFX_edict_type_policy"
 potential = {{ is_ai = no is_country_type = default }}
 effect = {{ hidden_effect = {{ {call(ns,1)} }} }}
}}
'''
    write('common/edicts/GFT_campaigns.txt',edicts)
    from trade_integration import generate_technology_trade
    generate_technology_trade(ROOT, techs, write)
    write('docs/technology_catalog.json',json.dumps({'target':'4.5.2','version':VERSION,'included':catalog,'excluded':excluded},ensure_ascii=False,indent=2))
    print(f'Generated {len(catalog)} gift technologies; excluded {len(excluded)}. Vanilla files were read only.')

if __name__=='__main__': main(Path(sys.argv[1]).resolve())
