"""Static cross-reference checks. Passing does NOT certify engine compatibility."""
from pathlib import Path
import collections
import hashlib
import json
import re
import sys
from clausewitz import parse, get, dump, walk
from generate import ROOT, VERSION, prerequisite_conditions

def main(vanilla):
    techs = {e.key:e.value for p in (vanilla/'common/technology').glob('*.txt')
             for e in parse(p.read_text(encoding='utf-8-sig'))
             if e.key.startswith('tech_') and isinstance(e.value,list)}
    catalog = json.loads((ROOT/'docs/technology_catalog.json').read_text(encoding='utf-8'))
    included = {row['id']:row for row in catalog['included']}
    errors = []
    def check(condition, message):
        if not condition: errors.append(message)
    definitions, calls, all_nodes, loc_refs = {}, [], [], set()
    for p in sorted((ROOT/'events').glob('*.txt')):
        tree = parse(p.read_text(encoding='utf-8-sig'))
        for entry in tree:
            if entry.key != 'country_event': continue
            body = entry.value
            eid = get(body,'id')
            check(eid not in definitions, 'Duplicate event ' + str(eid))
            definitions[eid] = body
            check(get(body,'is_triggered_only')=='yes', 'Non-triggered event ' + eid)
            for n in walk(body):
                all_nodes.append(n)
                if n.key in ('title','desc','name') and isinstance(n.value,str):
                    loc_refs.add(n.value.strip('"'))
                if n.key=='country_event' and isinstance(n.value,list): calls.append(get(n.value,'id'))
    check(not(set(calls)-definitions.keys()), 'Unresolved event calls: ' + str(set(calls)-definitions.keys()))
    entry_points={'gft_tech_trade.1','gft_fleet_trade.1'}
    reachable=set(entry_points)
    while True:
        new=reachable | {get(n.value,'id') for eid in reachable for n in walk(definitions[eid]) if n.key=='country_event' and isinstance(n.value,list)}
        if new==reachable: break
        reachable=new
    check(reachable==definitions.keys(), 'Unreachable events: '+str(definitions.keys()-reachable))
    triggers=[e for p in (ROOT/'common/scripted_triggers').glob('*.txt')
              for e in parse(p.read_text(encoding='utf-8'))]
    trigger_map={e.key:e.value for e in triggers}
    check(len(trigger_map)==len(triggers),'Duplicate scripted triggers')
    all_nodes += list(walk(triggers))
    trades=parse((ROOT/'common/tradable_actions/gft_technology_trade.txt').read_text(encoding='utf-8'))
    trade_map={e.key:e.value for e in trades}
    check(len(trade_map)==len(trades),'Duplicate trade action')
    for row in catalog['included']:
        key=row['id']; action=row['trade_action']
        check(action in trade_map,'Missing native trade row '+key)
        body=trade_map[action]
        check(get(body,'fire_and_forget')=='yes','Trade is not instant '+key)
        condition='gft_trade_can_give_'+key
        check(get(get(body,'potential',[]),condition)=='yes','Missing trade visibility '+key)
        possible=get(get(body,'possible',[]),'custom_tooltip',[])
        check(get(possible,condition)=='yes','Missing trade acceptance check '+key)
        guard=get(get(body,'on_traded_effect',[]),'if',[])
        check(get(get(guard,'limit',[]),condition)=='yes','Missing trade effect guard '+key)
        recipient=get(guard,'FROM',[])
        check(get(get(recipient,'give_technology',[]),'tech')==key,'Trade gift in wrong scope or wrong tech '+key)
        check(not any(n.key in ('country_event','save_event_target_as') for n in walk(body)), 'Trade has a second approval or shared target '+key)
        native_condition=trigger_map[condition]
        check(get(native_condition,'has_technology')==key,'Missing trade giver ownership '+key)
        native_receiver=get(native_condition,'FROM',[])
        original=techs[key]
        for required in get(original,'potential',[])+prerequisite_conditions(get(original,'prerequisites',[])):
            check(required in native_receiver,'Wrong trade recipient condition '+key)
        loc_refs.update((action,action+'_desc'))
    all_nodes += list(walk(trades))
    # The old technology event graph is intentionally retained for existing beta.1 windows.
    # Its explicit entry point is console/legacy, not a current edict.
    edict_tree=parse((ROOT/'common/edicts/GFT_campaigns.txt').read_text(encoding='utf-8'))
    check([e.key for e in edict_tree]==['gft_fleet_trade_options_menu'],'Technology edict was not removed')
    references={n.value for n in all_nodes if n.key=='has_technology'}
    grants=[]
    for row in catalog['included']:
        key=row['id']; body=definitions[row['offer_event']]
        grant_nodes=[n.value for n in walk(body) if n.key=='give_technology']
        check(len(grant_nodes)==1 and get(grant_nodes[0],'tech')==key,'Wrong gift '+key)
        check(get(body,'title')==key,'Wrong offer label '+key)
        accept=next(e.value for e in body if e.key=='option')
        check(get(get(accept,'trigger',[]),'gft_receive_'+key)=='yes','Missing acceptance eligibility '+key)
        guarded=get(get(accept,'hidden_effect',[]),'if',[])
        check(get(get(guarded,'limit',[]),'gft_receive_'+key)=='yes','Missing effect-time recheck '+key)
        grants += [get(n,'tech') for n in grant_nodes]
        check(key in techs, 'Unknown tech '+key)
        original=techs[key]
        check(get(original,'levels','1')=='1','Repeatable included '+key)
        check(get(original,'weight')!='0','Weight zero included '+key)
        check(get(original,'start_tech')!='yes','Starting tech included '+key)
        generated=trigger_map['gft_receive_'+key]
        original_potential=get(original,'potential',[])
        for condition in original_potential:
            check(condition in generated, 'Missing potential '+key)
        for prerequisite in prerequisite_conditions(get(original,'prerequisites',[])):
            check(prerequisite in generated,'Missing prerequisite / OR group '+key)
    check(not(references-techs.keys()),'Unknown tech references: '+str(references-techs.keys()))
    check(collections.Counter(grants)==collections.Counter(included.keys()),'Catalog/grant mismatch')
    texts='\n'.join(p.read_text(encoding='utf-8-sig') for folder in ['events','common'] for p in (ROOT/folder).rglob('*.txt'))
    check(not re.search(r'(?:set|has|remove)_global_flag|save_global_event_target_as|set_timed_global_flag',texts),'Global transaction state remains')
    check(not re.search(r'@[a-zA-Z_]',texts),'Unresolved file-local Vanilla variable')
    for n in all_nodes:
        if n.key.startswith('gft_') and not (n.key in trade_map and isinstance(n.value,list)):
            check(n.key in trigger_map,'Unknown scripted trigger '+n.key)
    # Check script hooks against supplied Vanilla usage, excluding generated IDs.
    vanilla_text='\n'.join(p.read_text(encoding='utf-8-sig') for folder in ['common','events'] for p in (vanilla/folder).rglob('*.txt'))
    vanilla_keys={m.group(1) for m in re.finditer(r'\b([A-Za-z_][\w.]*)\s*(?:=|[<>])',vanilla_text)}
    structural={'id','title','desc','name','picture','is_triggered_only','immediate','option','trigger','hidden_effect','ai_chance','factor','limit','message','tech'}
    used_keys={n.key for n in all_nodes if n.op and not n.key.startswith(('gft_','event_target:'))}
    check(not(used_keys-vanilla_keys-structural),'Hooks absent from supplied Vanilla: '+str(used_keys-vanilla_keys-structural))
    languages={}
    for p in (ROOT/'localisation').glob('*.yml'):
        raw=p.read_bytes()
        check(raw.startswith(b'\xef\xbb\xbf'),'Missing BOM '+p.name)
        text=raw.decode('utf-8-sig')
        lang=text.splitlines()[0].rstrip(':')
        keys=re.findall(r'^ ([\w.]+):\d+\s+".*"$',text,re.M)
        check(len(keys)==len(set(keys)),'Duplicate loc key '+p.name)
        check(len(keys)==len([l for l in text.splitlines()[1:] if l.strip()]),'Malformed localization '+p.name)
        languages[lang]=set(keys)
        check(not(loc_refs-set(keys)-techs.keys()),'Missing localization '+p.name+': '+str(loc_refs-set(keys)-techs.keys()))
        vanilla_loc_keys={m.group(1) for vp in (vanilla/'localisation'/lang.removeprefix('l_')).rglob('*.yml')
                         for m in re.finditer(r'^\s*([\w.]+):',vp.read_text(encoding='utf-8-sig'),re.M)}
        check(not(set(keys)&vanilla_loc_keys),'Vanilla localization override '+p.name)
        check(not(included.keys()-vanilla_loc_keys),'Missing native technology names '+p.name)
    check(len(languages)==3,'Expected three languages')
    check(len({tuple(sorted(x)) for x in languages.values()})==1,'Language key mismatch')
    for p in [ROOT/'descriptor.mod',ROOT/'GiveTechnologyFleets.mod']:
        meta=parse(p.read_text(encoding='utf-8'))
        check(get(meta,'version')=='"'+VERSION+'"','Version mismatch '+p.name)
        check(get(meta,'supported_version')=='"4.5.2"','Target mismatch '+p.name)
        check(not any(n.key=='replace_path' for n in meta),'replace_path present')
    custom_ids=set(trigger_map)|{e.key for e in parse((ROOT/'common/edicts/GFT_campaigns.txt').read_text(encoding='utf-8'))}
    custom_ids |= set(trade_map)
    original_ids={e.key for folder in ['common/scripted_triggers','common/edicts','common/tradable_actions'] for p in (vanilla/folder).rglob('*.txt') for e in parse(p.read_text(encoding='utf-8-sig'))}
    check(not(custom_ids&original_ids),'Vanilla definition override: '+str(custom_ids&original_ids))
    report={'status':'PASS' if not errors else 'FAIL','kind':'static only; not a Stellaris engine run',
      'target':'4.5.2','version':VERSION,'technology_definitions':len(techs),'gift_technologies':len(included),
      'excluded_technologies':len(catalog['excluded']),'events':len(definitions),'reachable_events':len(reachable),
      'scripted_triggers':len(trigger_map),'native_trade_actions':len(trade_map),'languages':{k:len(v) for k,v in languages.items()},
      'vanilla_overrides':sorted(custom_ids&original_ids),'errors':errors}
    (ROOT/'docs/static_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return bool(errors)

if __name__=='__main__': sys.exit(main(Path(sys.argv[1]).resolve()))
