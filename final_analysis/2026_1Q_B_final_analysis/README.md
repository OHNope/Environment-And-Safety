# 2026 1Q B 期末分析

このディレクトリは、`2026 1Q 環境安全論 B` の期末試験分析・予想・復習用資料をまとめるためのものである。

## ファイル構成

- [共通傾向分析](../common/overall_trend_analysis.md)
  - 利用可能な過去問全体の出題傾向を確認し、A/B クラスの共通点と差異を整理する。
- [B クラス期末分析](B_class_final_exam_analysis.md)
  - B クラスだけを対象に、試験構成、出題頻度、2026 年小テストによる補正を分析する。
- [B クラス予想問題集](B_class_predicted_question_bank_2026_1Q.md)
  - 2026 1Q B 期末の予想問題集。出題可能性に応じてランク分けしている。
- [模擬試験](mock_exams/README.md)
  - 3 セットの予想模擬試験。各セットは `questions.md` と `answers.md` に分けている。
- [B クラス高頻度暗記](B_class_high_frequency_memorization.md)
  - B クラスで特に暗記優先度が高い問題と解答例。
- [資源と廃棄物 第 1 回補足ノート](resource_waste_first_lecture_notes.md)
  - 第 1 回 `資源と廃棄物` の 講義資料末尾まとめと原 講義資料メモをもとにした補足ノート。
- [講義資料重点メモ](pdf_targeted_findings.md)
  - 提供された 2026 年 講義資料メモ から、予想に直接効く高価値ポイントだけを抽出したメモ。
- [構造化頻度分析 JSON](build/analysis_summary.json)
  - スクリプトで生成した構造化頻度分析。
- [予想スコア表 TSV](build/prediction_scoreboard.tsv)
  - 予想優先度を素早く確認するためのスコア表。
- [頻度分析生成スクリプト](scripts/generate_analysis.py)
  - 過去問・小テストのテーマを手動分類し、頻度分析を生成するスクリプト。

## データ範囲

- 過去問: [source/problems](../../source/problems/) 内の `2022-2025` 年 A/B 問題。
- 2026 年 B クラス小テスト: [source/2026_B_1Q_quizzes](../../source/2026_B_1Q_quizzes/)。
- 2026 年 B クラス講義資料メモ: 著作権配慮のため、元講義資料ファイルはリポジトリには含めない。

## 使い方

最初に [B クラス期末分析](B_class_final_exam_analysis.md) で全体像を確認し、次に [B クラス高頻度暗記](B_class_high_frequency_memorization.md) を暗記する。最後に [模擬試験](mock_exams/README.md) の 3 セットを、本命、小テスト寄せ、変化球の順に解く。各セットは先に `*_questions.md` を解き、その後 `*_answers.md` で確認する。
