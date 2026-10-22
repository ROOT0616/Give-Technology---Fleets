# 4.5.2互換性・重複調査

## beta.2追記：交易画面への移行

前回調査では`common/tradable_actions`の確認が不足していた。同ディレクトリの`00_README.txt`には「資源等と並べて取引へ追加する行」を定義できること、全条件と成立時effectでROOT=送付国、FROM=受領国となることが明記されている。`00_tradable_actions.txt`にも`trade_action_share_empire_data`や`trade_action_bulwark_technology`などの実定義がある。

beta.2では、この仕組みにより467技術を通常の交易項目として実装した。`fire_and_forget = yes`、`potential`、`possible`、`on_traded_effect`、`ai_weight`は提供Vanillaの文書・実定義を根拠とする。技術の布告入口は撤去し、イベントやglobal targetを介さず受領国に付与する。技術の対価は通常の同一取引提案で指定できる設計だが、UI・価格・同時交換の実機動作は未確認。

一方、カスタム取引の文書には選択済みfleetやdeal IDの引き渡しがない。標準の「Borrow Fleet」欄はengineが処理する。`on_fleet_contract_started`はfleetをROOT、借用国をFROM、所有国をFROMFROMに渡すが、契約との一意な対応が得られず、同じ相手との別契約まで恒久化する実装は採用しない。成立後の別メニューで艦隊を選ぶ方式も、契約時に対象を確定できないため、現時点では追加しない。**艦隊の交易画面への移行は未完了。** 既存の布告方式を維持する。

GUI override・Vanilla定義override・replace_pathは引き続きない。以下は主にbeta.1時点の調査記録で、操作方法と現行仕様はREADMEを優先する。

ユーザーの追加指定により、艦隊は「成立前の対象指定」が必須。成立後に選択する代替案は採用しない。現在の公開script接続で不可能と断定したのではなく、安全な実装方法を確認できていない状態として残す。

調査日：2026-10-23。更新元：[ROOT0616/Give-Technology---Fleets](https://github.com/ROOT0616/Give-Technology---Fleets)、`master`の`2fe572643cd229df1d85b184bec0262f581b75f6`（2.0.1 / 3.7.*）。引き継ぎ先の旧チャットには依頼文以外の調査結果・添付はありませんでした。

## 対象版の根拠

- [Stellaris公式・4.5.2公開告知](https://steamcommunity.com/games/281990/announcements/detail/668378128507209902)：2026-10-06公開、Cygnus、checksum 9776。調査日の[公式告知一覧](https://steamcommunity.com/app/281990/announcements/?l=english)でも確認。
- [Paradox Interactive公式プレスリリース](https://news.cision.com/paradox-interactive/r/willpower-expansion-for-stellaris-to-launch-on-november-23,c4413029)：2026-10-21付。4.6 Corona BorealisはWillpowerとともに11月23日予定。したがって今回の対応対象に含めない。
- 実装調査ではユーザー提供の`Vanilla_common.zip`、`Vanilla_events.zip`、`Vanilla_interface.zip`、`Vanilla_localisation.zip`を最優先した。Vanilla localizationの`main_1_l_english.yml:1076`には4.5 Cygnusの開始案内がある。ZIP内に実行ファイルのbuild/checksum情報はないため、9776の実機ファイルであることまで独立検証していない。
- 元ZIPは変更していない。別ディレクトリへ展開して参照した。ハッシュは[source_archives.json](source_archives.json)に記録。VanillaのZIPや実ファイルは配布物・PRへ含めない。

## 重複の確認

| 対象 | 提供Vanillaの根拠 | 確認結果 |
|---|---|---|
| 研究協定の締結・破棄 | `common/diplomatic_actions/00_actions.txt:1958`、`:2185` | 既存機能 |
| 取引内の研究協定 | `localisation/english/main_1_l_english.yml:2279–2280`、`TRADE_ITEM_RESEARCH_AGREEMENT(_DESC)` | 相手国既知技術への研究速度補正。即時の取得ではない |
| 艦隊借用 | 同ファイル`:2212`、`:2226–2227`、`TRADE_CATEGORY_TRANSFER_FLEET` / `tc_transfer_fleet(_desc)` | 一定年数の借用 |
| 貸与中の表示・返却 | 同ファイル`:1394–1396`、`FLEET_TIP_OWNERSHIP_STATUS_LEASED_OUT` / `FLEET_TIP_LEASE_DAYS_BEFORE_RETURN` | 所有権の恒久移転と異なる |
| 取引GUI | `interface/trade_view.gui`の`trade_categories_list`、`trade_items_list`、`trade_deal_length`。外交側は`interface/diplomacy_view.gui` | 項目一覧はGUIに個別列挙されておらずengine生成を含む。未知のscript側取引hookを仮定しない |
| 傭兵貸与 | `events/overlord_enclaves_events.txt`の`is_leased`、`ordered_controlled_fleet`等 | 軍事支援としては近いが、自国艦隊の無償・恒久譲渡とは異なる |

確認した範囲では完全な機能重複ではない。「現在のバニラで使える軍事支援や研究支援」と「このMODの即時技術付与・恒久所有権移転」を分ける。全engine内部・全DLCの条件を網羅した断定はしない。

## 更新元で確認した問題

- `descriptor.mod`は2.0.1、対応表記は3.7.*。Launcher用外部`.mod`とREADMEはなかった。
- 固定技術参照401件のうち、`tech_leviathan_transgenesis`、`tech_lithoid_transgenesis`、`tech_plantoid_transgenesis`は提供Vanillaのトップレベル技術定義にない。別名を推測して置換しない。
- 技術選択肢の表示名を英語・日本語の旧localizationと比較すると、いずれかの言語で実際の技術条件と異なる選択肢が327件あった。たとえば`.10.a`は実際には`tech_administrative_ai`だが、英語は`tech_space_science_1`を表示していた。
- 全プレイヤー共通のglobal event targetとglobal flagを使用。技術側の6か月global lockには、古い申し出と次の取引が重なる可能性がある。艦隊側は期限なしglobal lockで、完了経路に依存していた。実機で再現した事実ではなくコード構造上の問題。
- 艦隊受領の日本語説明に技術用の対象名`gft_technology_trade_0`が混在。`gft_fleet_trade.1.n`のlocalizationが重複し、艦隊キャンセルのキーも不一致だった。
- 艦隊受諾では`set_owner`を実行するが、受諾直前の所有者・貸与状態・戦闘状態の確認や司令官解除がなかった。

## 更新後の処理とscope

| 処理 | scopeの経路 |
|---|---|
| 入口 | 布告のcountry → `gft_tech_trade.1`または`gft_fleet_trade.1`。`gft_donor`をイベントチェーン内に保存 |
| 国選択 | donor country → `random_country`（候補country）→ donor countryへ復帰。候補を`gft_country_1…13`に保存し、選択された国を`gft_recipient`として保存 |
| 技術選択 | donor country → recipient countryで`gft_receive_<technology>`を評価 → donor countryへ復帰。recipient countryで技術別受領イベントを起動 |
| 技術受諾 | ROOTはrecipient country。donorの実在・保有、両国の通信/和平、recipientの未保有・前提条件・potentialを再確認し、recipientに`give_technology` |
| 艦隊選択 | donor country → `random_owned_fleet`（fleet）→ donorへ復帰。候補を保存し、選択したfleetを`gft_offered_fleet`に保存 |
| 艦隊受諾 | ROOTはrecipient country。fleet scopeで`owner`と貸与/戦闘条件を確認。`leader`へ移って解除後fleetへ戻り、`set_owner = root`、`set_controller = root` |
| 通知 | recipient country → 保存済みdonor countryで結果イベント。グローバル取引状態を残さない |

国候補は最初に同じcountry型のdonorで初期化し、自国を候補条件で除外する。艦隊候補は有効な1艦隊で全枠を初期化してから異なる艦隊で置換し、重複枠を非表示にする。未確認の対象参照クリアeffectを追加せず、再抽選時の古い候補の残存を防ぐ設計。

## 実在を確認した主な構文

- 布告`potential` / `effect` / `length`：`common/edicts/99_README_EDICTS.txt`、実定義`00_edicts.txt`等。`length = 0`の入口は旧MODの構造を保持。0日の即時再実行性は実機未確認。
- countryの`is_at_war_with` / `has_communications`：`common/diplomatic_actions/00_actions.txt`等。
- 技術の`potential` / `prerequisites`：`common/technology/*.txt`から抽出。現行には複数のORグループもあり、単なる前提キーの羅列に変換しない。
- countryの`give_technology = { tech = … message = no }`：`events/apocalypse_events.txt`等。
- fleetの`is_leased`：`events/overlord_enclaves_events.txt`、特に`enclave.2070`周辺の`ordered_controlled_fleet`。
- fleetの`is_ship_class` / `is_mobile`：`events/first_contact_dlc_events.txt`等。`is_in_combat`：`events/gray_goo_events.txt`等。
- fleetの`set_owner`：`events/anomaly_events_1.txt:837`等。fleetの`set_controller`：`events/ambition_events.txt:1089`、`:1122`等。
- fleet → leaderの`unassign_leader = this`：`events/anomaly_events_4.txt:3033–3034`。
- `save_event_target_as` / 対象を通じたイベント起動：提供events全体で確認。独立した複数チェーンでの保存・復帰・ネットワーク同期は実機テスト対象。

## 互換性と未確認事項

Vanilla overrideはなし。追加定義は布告2件とscripted trigger469件、イベント522件。GUIファイルは変更しない。既存namespaceを保持するため、旧版や派生MODとの同時使用は不可。

3.7から4.5.2への大規模互換性変更なのでmajorを3へ進め、実機未検証を`beta.1`として明示。旧取引用global stateのmigrationは実装しない。旧メニュー・旧申し出があるセーブへの途中更新は非対応。新規ゲーム推奨。

静的検証は[static_validation.json](static_validation.json)を参照。ゲーム本体のparser、イベント対象の複数ウィンドウ間の挙動、艦隊転送後の設計・補充・command limit・leader・アップグレード・特殊艦隊、技術取得時の各DLC固有処理、AI、セーブ/ロード、マルチプレイは未確認。次は[runtime_test_plan.md](runtime_test_plan.md)に従い4.5.2実機で検証する。
