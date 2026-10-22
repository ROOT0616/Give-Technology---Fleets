"""Write UTF-8 BOM localization, with identical keys in all supported languages."""
from generate import write

TEXT = {
 'english': {
  'edict_gft_technology_trade_options_menu':'Give Technology',
  'edict_gft_technology_trade_options_menu_desc':'Offer an eligible technology you own as an immediate, free gift. The recipient may decline.',
  'edict_gft_fleet_trade_options_menu':'Give Fleet',
  'edict_gft_fleet_trade_options_menu_desc':'Offer a military fleet as a permanent, free gift. Shared political fleets are excluded conservatively; see README.',
  'gft_country_title':'Choose a recipient',
  'gft_country_desc':'Choose a contacted regular empire at peace with you. Up to 13 random candidates are shown. Refresh to draw again. No payment is collected.',
  'gft_tech_title':'Choose a technology field and tier',
  'gft_tech_desc':'Only technologies you own and the recipient lacks are shown, with recipient eligibility and prerequisites satisfied. Empty pages can be skipped. Repeatable, starting and special event technologies are excluded.',
  'gft_fleet_title':'Choose a fleet',
  'gft_fleet_desc':'Up to 10 mobile, unleased military fleets outside combat are shown. Federation presidents, the Custodian and the Emperor cannot send fleets in this beta. An assigned commander stays with the donor. The recipient may refuse.',
  'gft_fleet_offer_title':'A permanent fleet gift',
  'gft_offer_tech_desc':'[gft_donor.GetName] offers the technology shown above, free of charge. Acceptance grants it immediately. Eligibility is checked again on acceptance.',
  'gft_offer_fleet_desc':'[gft_donor.GetName] offers permanent ownership of [gft_offered_fleet.GetName], free of charge. The fleet must still belong to the donor and be eligible when you accept.',
  'gft_accepted':'Gift accepted', 'gft_declined':'Gift declined',
  'gft_tech_accepted_desc':'Your technology gift was accepted.',
  'gft_fleet_accepted_desc':'Your fleet gift was accepted. Ownership and control have been transferred.',
  'gft_declined_desc':'The recipient declined your offer, or the gift was no longer eligible.',
  'gft_accept':'Accept the gift', 'gft_decline':'Decline / dismiss invalid offer',
  'gft_previous':'Previous page', 'gft_next':'Next page', 'gft_refresh':'Refresh candidates',
  'gft_back':'Back', 'gft_close':'Close',
 },
 'japanese': {
  'edict_gft_technology_trade_options_menu':'技術の贈与',
  'edict_gft_technology_trade_options_menu_desc':'自国が保有する対象技術を無償で贈与します。相手国は拒否できます。',
  'edict_gft_fleet_trade_options_menu':'艦隊の贈与',
  'edict_gft_fleet_trade_options_menu_desc':'軍事艦隊の所有権を無償で恒久移転します。共有艦隊保護のための制限はREADMEを参照してください。',
  'gft_country_title':'贈与先の選択',
  'gft_country_desc':'通信確立済みで交戦していない通常帝国から選択してください。候補はランダムに最大13か国です。「候補を再抽選」で入れ替えられます。対価は徴収されません。',
  'gft_tech_title':'技術分野・ティアの選択',
  'gft_tech_desc':'自国が保有し、相手国が未保有で、前提技術と受領条件を満たす技術を表示します。空のページは次へ進めてください。反復技術・開始時の技術・イベント用の特殊技術は対象外です。',
  'gft_fleet_title':'贈与する艦隊の選択',
  'gft_fleet_desc':'移動可能・貸与中ではない・戦闘中ではない軍事艦隊から最大10個を表示します。このベータ版では連邦議長・銀河守護者・銀河皇帝からの送付を制限しています。配属司令官は贈与元に残ります。相手国は拒否できます。',
  'gft_fleet_offer_title':'艦隊の恒久贈与の申し出',
  'gft_offer_tech_desc':'[gft_donor.GetName]から、上記の技術を無償で贈与する申し出がありました。受諾すると即時に取得します。受諾時に条件を再確認します。',
  'gft_offer_fleet_desc':'[gft_donor.GetName]から[gft_offered_fleet.GetName]の所有権を無償で恒久移転する申し出がありました。受諾時にも贈与元の所有であり、移転条件を満たす必要があります。',
  'gft_accepted':'贈与が受諾された', 'gft_declined':'贈与が成立しなかった',
  'gft_tech_accepted_desc':'技術の贈与が受諾されました。',
  'gft_fleet_accepted_desc':'艦隊の贈与が受諾され、所有権と制御権が移転しました。',
  'gft_declined_desc':'相手国が拒否したか、贈与の条件を満たさなくなりました。',
  'gft_accept':'贈与を受け入れる', 'gft_decline':'辞退する／無効な申し出を閉じる',
  'gft_previous':'前のページ', 'gft_next':'次のページ', 'gft_refresh':'候補を再抽選',
  'gft_back':'戻る', 'gft_close':'閉じる',
 },
 'simp_chinese': {
  'edict_gft_technology_trade_options_menu':'赠送科技',
  'edict_gft_technology_trade_options_menu_desc':'无偿赠送已掌握的适用科技。接收方可以拒绝。',
  'edict_gft_fleet_trade_options_menu':'赠送舰队',
  'edict_gft_fleet_trade_options_menu_desc':'无偿永久转让军事舰队。为保护共享舰队而设置的限制请参阅README。',
  'gft_country_title':'选择接收方',
  'gft_country_desc':'选择已建立通讯且未与你交战的常规帝国。随机显示最多13个候选，可刷新。不收取任何费用。',
  'gft_tech_title':'选择科技领域与等级',
  'gft_tech_desc':'仅显示本国已掌握、对方未掌握且满足前置科技及接收条件的科技。空页可跳过。排除循环科技、初始科技及事件专用科技。',
  'gft_fleet_title':'选择舰队',
  'gft_fleet_desc':'最多显示10支可移动、非租借且未在战斗中的军事舰队。此测试版禁止联邦主席、银河监管人和银河皇帝赠送舰队。指挥官留在赠送方。接收方可以拒绝。',
  'gft_fleet_offer_title':'永久赠送舰队的提议',
  'gft_offer_tech_desc':'[gft_donor.GetName]愿意无偿赠送上方所示科技。接受后立即获得科技。接受时将再次检查条件。',
  'gft_offer_fleet_desc':'[gft_donor.GetName]愿意无偿永久转让[gft_offered_fleet.GetName]。接受时该舰队必须仍归赠送方所有且符合条件。',
  'gft_accepted':'赠送已被接受', 'gft_declined':'赠送未能完成',
  'gft_tech_accepted_desc':'对方接受了你赠送的科技。',
  'gft_fleet_accepted_desc':'对方接受了你赠送的舰队。所有权和控制权已转移。',
  'gft_declined_desc':'对方拒绝了提议，或赠送条件已不再满足。',
  'gft_accept':'接受赠送', 'gft_decline':'拒绝／关闭无效提议',
  'gft_previous':'上一页', 'gft_next':'下一页', 'gft_refresh':'刷新候选',
  'gft_back':'返回', 'gft_close':'关闭',
 }
}

def main():
    import json
    from generate import ROOT
    catalog = json.loads((ROOT/'docs/technology_catalog.json').read_text(encoding='utf-8'))
    for lang, values in TEXT.items():
        values['gft_trade_technology_invalid'] = {
          'english':'The giver must still own this technology. The recipient must lack it and meet its prerequisites and eligibility conditions.',
          'japanese':'送付国が技術を保有し、受領国が未保有で、前提技術と受領条件を満たす必要があります。',
          'simp_chinese':'赠送方必须掌握该科技，接收方必须未掌握且满足前置科技与接收条件。'
        }[lang]
        for row in catalog['included']:
            values[row['trade_action']] = '$'+row['id']+'$'
            values[row['trade_action']+'_desc'] = {
              'english':'Transfer this technology immediately when this trade deal is accepted. Resources and other trade items may be included in the same proposal.',
              'japanese':'取引成立時にこの技術を即時に付与します。同じ提案に資源などの取引項目を組み合わせられます。',
              'simp_chinese':'交易被接受时立即转让此科技。可在同一提议中组合资源等其他交易项目。'
            }[lang]
        for i in range(1,14): values[f'gft_country_{i}'] = f'[gft_country_{i}.GetName]'
        for i in range(1,11): values[f'gft_fleet_slot_{i}'] = f'[gft_fleet_slot_{i}.GetName]'
        area_names = {
          'english': ['Physics','Society','Engineering'],
          'japanese': ['物理学','社会学','工学'],
          'simp_chinese': ['物理学','社会学','工程学']
        }[lang]
        for area,name in zip(('physics','society','engineering'),area_names):
            for tier in range(1,6): values[f'gft_{area}_{tier}'] = f'{name} / {tier}'
        lines=[f'l_{lang}:'] + [f' {key}:0 "{value}"' for key,value in values.items()]
        write(f'localisation/GFT_l_{lang}.yml','\n'.join(lines),bom=True)

if __name__ == '__main__': main()
