# 2026 1Q A 期末分析

このディレクトリは、`2026 1Q 環境安全論 A` の期末試験対策を、B クラス分析と同じ構造で整理したものである。

## 読む順番

1. [共通傾向](../common/overall_trend_analysis.md)
2. [A クラス期末分析](A_class_final_exam_analysis.md)
3. [講義資料重点メモ](pdf_targeted_findings.md)
4. [予想問題集](A_class_predicted_question_bank_2026_1Q.md)
5. [高頻度暗記](A_class_high_frequency_memorization.md)
6. [模擬試験](mock_exams/README.md)

## ファイル構成

| ファイル | 内容 |
|---|---|
| [A_class_final_exam_analysis.md](A_class_final_exam_analysis.md) | A クラス過去問、2026 小テスト、講義資料メモを統合した出題分析 |
| [A_class_predicted_question_bank_2026_1Q.md](A_class_predicted_question_bank_2026_1Q.md) | ランク別の予想問題集 |
| [A_class_high_frequency_memorization.md](A_class_high_frequency_memorization.md) | 直前暗記用の要点 |
| [pdf_targeted_findings.md](pdf_targeted_findings.md) | 講義資料メモと小テストの対応関係、および期末に効く論点 |
| [mock_exams/](mock_exams/README.md) | A クラス用の模擬試験 |
| [scripts/generate_analysis.py](scripts/generate_analysis.py) | 過去の期末試験、2026 年小テスト、講義資料メモの手動タグを集計するスクリプト |
| [build/analysis_summary.json](build/analysis_summary.json) | スクリプト生成の構造化集計 |
| [build/prediction_scoreboard.tsv](build/prediction_scoreboard.tsv) | 予想優先度の一覧 |
| [build/topic_frequency.md](build/topic_frequency.md) | 頻度表を読むためのマークダウン版 |

## データ範囲

- A クラス過去問: `source/problems/` 内の 2022-2025 年資料。
- 2026 A 小テスト: `source/2026_A_1Q_quizzes/`。
- 2026 A 講義資料メモ: 著作権配慮のため、元講義資料ファイルはリポジトリには含めない。ランク判断では、過去問または小テストで確認できる内容を優先する。
- A/B 共通傾向: `final_analysis/common/overall_trend_analysis.md`。

## 2026 A 講義資料メモと小テストの対応

| 講義資料メモ | 対応小テスト | 主な論点 |
|---|---|---|
| `資源・廃プラスチック系` | `20260407_2026_A_1Q_plastic_recycling_quiz_*` | MR / CR / TR、バーゼル条約、廃プラスチック、CCS / CCUS |
| `持続可能性系` | `undated_2026_A_1Q_environment_sustainability_quiz_*` | 持続可能性、人口、地球温暖化、SDGs、Our Common Future |
| `グリーンケミストリー系` | `undated_2026_A_1Q_green_chemistry_pfas_quiz_*` | グリーンケミストリー、CFC、PFAS / PFOS、ライフサイクル |
| 2026 年講義資料メモ | `undated_2026_A_1Q_zero_carbon_energy_quiz_*` | MDGs / SDGs、MPI、質量エネルギー等価、太陽エネルギー、DT 核融合、リチウム資源 |

## 集計の再生成

```bash
python3 final_analysis/2026_1Q_A_final_analysis/scripts/generate_analysis.py
```

生成物は `build/` に出力される。

## 現時点の結論

2026 A は、2024・2025 の A 期末テンプレートを土台にしつつ、2026 年小テストにより次の補正が入る。小テストだけで支持される分野は、項目数が多くても A 過去問反復テーマと同列には置かない。

- Q1 は `安定性 / 親油性 / 添加剤` だけでなく、`MR / CR / TR`、`85%`、`25%`、`中国`、`バーゼル条約`、`廃プラスチック` まで準備する。
- Q5 は従来のグリーンケミストリー説明に加え、CFC、PFAS / PFOS、ライフサイクル、新規化学物質リスクを入れる。
- Q6 は PRTR / SDS だけでなく、エコロジカル・フットプリント、キーストーン種、バイオマス、バイオリファイナリーも候補に残る。
- 放射線は小テストがなくても過去問での安定度が高く、最優先暗記対象である。
- 新規ゼロカーボンエネルギー小テストにより、核融合は A 級の変化球候補へ上がった。ただし A 過去問固定テーマではなく、`2026 A 小テスト直撃 + B 過去問に既存テンプレートあり` として扱う。特に `DT 反応 17.6 MeV`、`E=mc^2`、`1GW 炉の Li 消費量`、海水中リチウム資源の概算は、計算問題または正誤問題として警戒する。
- 環境サステナビリティ系は 2026 A 小テストでは強いが、A 過去問の固定大問ではない。ティッピングポイントを本命にしつつ、SDGs、Our Common Future、緩和 / 適応、CO2 削減後の気温持続を正誤・短答補強として準備する。
