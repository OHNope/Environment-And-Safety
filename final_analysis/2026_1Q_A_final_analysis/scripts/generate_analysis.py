from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Occurrence:
    paper_id: str
    year: int
    class_code: str
    quarter: str
    source_type: str
    topic: str
    count: int
    label: str
    path: str
    certainty: str = "definite"
    note: str = ""


TOPICS = {
    "plastic_recycling": {
        "label": "廃プラスチックリサイクル / MR・CR・TR",
        "bucket": "resource_waste",
    },
    "plastic_harm": {
        "label": "プラスチック環境影響（安定性・親油性・添加剤）",
        "bucket": "resource_waste",
    },
    "carbon_neutrality": {
        "label": "カーボンニュートラルと科学技術",
        "bucket": "sustainability_climate",
    },
    "tipping_point": {
        "label": "地球環境問題のティッピングポイント",
        "bucket": "sustainability_climate",
    },
    "dampness": {
        "label": "WHO dampness",
        "bucket": "sustainability_climate",
    },
    "climate_sustainability": {
        "label": "持続可能性 / SDGs / 気候変動対策",
        "bucket": "sustainability_climate",
    },
    "radiation_protection": {
        "label": "放射線防護三原則",
        "bucket": "radiation_energy",
    },
    "radiation_effects": {
        "label": "確定的影響 / 確率的影響",
        "bucket": "radiation_energy",
    },
    "energy_quality": {
        "label": "エネルギー形態とエネルギーの質",
        "bucket": "radiation_energy",
    },
    "hydrogen_ccs_fuelcell": {
        "label": "水素 / CCS / 燃料電池",
        "bucket": "radiation_energy",
    },
    "heat_engine_efficiency": {
        "label": "熱機関 / カルノー効率",
        "bucket": "radiation_energy",
    },
    "fusion_energy": {
        "label": "核融合 / 重水素・三重水素",
        "bucket": "radiation_energy",
    },
    "green_chemistry": {
        "label": "グリーンケミストリー / サステイナブルケミストリー",
        "bucket": "chemicals",
    },
    "pfas_cfc_novel_entities": {
        "label": "CFC / PFAS / Novel entities",
        "bucket": "chemicals",
    },
    "prtr_sds": {
        "label": "PRTR / SDS / 化学物質管理",
        "bucket": "chemicals",
    },
    "keystone_species": {
        "label": "キーストーン種 / 生物多様性",
        "bucket": "life_environment",
    },
    "ecological_footprint": {
        "label": "エコロジカル・フットプリント",
        "bucket": "life_environment",
    },
    "biomass_carbon_neutral": {
        "label": "バイオマスとカーボンニュートラル",
        "bucket": "life_environment",
    },
    "biorefinery_bioplastics": {
        "label": "バイオリファイナリー / バイオプラスチック",
        "bucket": "life_environment",
    },
    "true_false_general": {
        "label": "総合正誤問題",
        "bucket": "mixed",
    },
    "personal_action": {
        "label": "個人の省エネルギー・省資源実践",
        "bucket": "mixed",
    },
}


PAST_EXAM_OCCURRENCES = [
    Occurrence("2022_A_1Q", 2022, "A", "1Q", "final", "plastic_recycling", 1, "Q1", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_1Q", 2022, "A", "1Q", "final", "tipping_point", 1, "Q2", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_1Q", 2022, "A", "1Q", "final", "radiation_effects", 1, "Q3", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_1Q", 2022, "A", "1Q", "final", "radiation_protection", 1, "Q4", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_1Q", 2022, "A", "1Q", "final", "energy_quality", 1, "Q5", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_1Q", 2022, "A", "1Q", "final", "keystone_species", 1, "Q6", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_1Q", 2022, "A", "1Q", "final", "true_false_general", 1, "Q7", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "plastic_recycling", 1, "Q1", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "dampness", 1, "Q2", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "radiation_protection", 1, "Q3", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "radiation_effects", 1, "Q3", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "energy_quality", 1, "Q4", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "green_chemistry", 1, "Q5", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "keystone_species", 1, "Q6", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "true_false_general", 1, "Q7", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "personal_action", 1, "Q8", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2023_A_2Q", 2023, "A", "2Q", "final", "plastic_recycling", 1, "Q1", "source/problems/2023_environment_safety_A_2Q_recreated_questions.md"),
    Occurrence("2023_A_2Q", 2023, "A", "2Q", "final", "tipping_point", 1, "Q2", "source/problems/2023_environment_safety_A_2Q_recreated_questions.md"),
    Occurrence("2023_A_2Q", 2023, "A", "2Q", "final", "radiation_effects", 1, "Q3", "source/problems/2023_environment_safety_A_2Q_recreated_questions.md"),
    Occurrence("2023_A_2Q", 2023, "A", "2Q", "final", "radiation_protection", 1, "Q4", "source/problems/2023_environment_safety_A_2Q_recreated_questions.md"),
    Occurrence("2023_A_2Q", 2023, "A", "2Q", "final", "energy_quality", 1, "Q5", "source/problems/2023_environment_safety_A_2Q_recreated_questions.md"),
    Occurrence("2023_A_2Q", 2023, "A", "2Q", "final", "keystone_species", 1, "Q6", "source/problems/2023_environment_safety_A_2Q_recreated_questions.md"),
    Occurrence("2023_A_2Q", 2023, "A", "2Q", "final", "personal_action", 1, "Q7", "source/problems/2023_environment_safety_A_2Q_recreated_questions.md"),
    Occurrence("2023_A_2Q", 2023, "A", "2Q", "final", "true_false_general", 1, "Q8", "source/problems/2023_environment_safety_A_2Q_recreated_questions.md"),
    Occurrence("2024_A_1Q", 2024, "A", "1Q", "final", "plastic_harm", 1, "Q1", "source/problems/2024_environment_safety_A_1Q_final_questions.md"),
    Occurrence("2024_A_1Q", 2024, "A", "1Q", "final", "tipping_point", 1, "Q2", "source/problems/2024_environment_safety_A_1Q_final_questions.md"),
    Occurrence("2024_A_1Q", 2024, "A", "1Q", "final", "radiation_protection", 1, "Q3-1", "source/problems/2024_environment_safety_A_1Q_final_questions.md"),
    Occurrence("2024_A_1Q", 2024, "A", "1Q", "final", "radiation_effects", 1, "Q3-2", "source/problems/2024_environment_safety_A_1Q_final_questions.md"),
    Occurrence("2024_A_1Q", 2024, "A", "1Q", "final", "energy_quality", 1, "Q4", "source/problems/2024_environment_safety_A_1Q_final_questions.md"),
    Occurrence("2024_A_1Q", 2024, "A", "1Q", "final", "green_chemistry", 1, "Q5", "source/problems/2024_environment_safety_A_1Q_final_questions.md"),
    Occurrence("2024_A_1Q", 2024, "A", "1Q", "final", "prtr_sds", 1, "Q6", "source/problems/2024_environment_safety_A_1Q_final_questions.md"),
    Occurrence("2024_A_1Q", 2024, "A", "1Q", "final", "true_false_general", 1, "Q7", "source/problems/2024_environment_safety_A_1Q_final_questions.md"),
    Occurrence("2024_A_1Q", 2024, "A", "1Q", "final", "personal_action", 1, "Q8", "source/problems/2024_environment_safety_A_1Q_final_questions.md"),
    Occurrence("2025_A_1Q", 2025, "A", "1Q", "final", "plastic_harm", 1, "Q1", "source/problems/2025_environment_safety_A_1Q_recreated_questions.md"),
    Occurrence("2025_A_1Q", 2025, "A", "1Q", "final", "tipping_point", 1, "Q2", "source/problems/2025_environment_safety_A_1Q_recreated_questions.md"),
    Occurrence("2025_A_1Q", 2025, "A", "1Q", "final", "radiation_protection", 1, "Q3-1", "source/problems/2025_environment_safety_A_1Q_recreated_questions.md"),
    Occurrence("2025_A_1Q", 2025, "A", "1Q", "final", "radiation_effects", 1, "Q3-2", "source/problems/2025_environment_safety_A_1Q_recreated_questions.md"),
    Occurrence("2025_A_1Q", 2025, "A", "1Q", "final", "energy_quality", 1, "Q4", "source/problems/2025_environment_safety_A_1Q_recreated_questions.md"),
    Occurrence("2025_A_1Q", 2025, "A", "1Q", "final", "green_chemistry", 1, "Q5", "source/problems/2025_environment_safety_A_1Q_recreated_questions.md"),
    Occurrence("2025_A_1Q", 2025, "A", "1Q", "final", "prtr_sds", 1, "Q6", "source/problems/2025_environment_safety_A_1Q_recreated_questions.md"),
    Occurrence("2025_A_1Q", 2025, "A", "1Q", "final", "true_false_general", 1, "Q7a", "source/problems/2025_environment_safety_A_1Q_recreated_questions.md"),
    Occurrence("2025_A_1Q", 2025, "A", "1Q", "final", "personal_action", 1, "Q7b", "source/problems/2025_environment_safety_A_1Q_recreated_questions.md"),
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "plastic_recycling", 1, "Q1", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "dampness", 1, "Q2", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "radiation_protection", 1, "Q3-1", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "radiation_effects", 1, "Q3-2", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "energy_quality", 1, "Q4a", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "heat_engine_efficiency", 1, "Q4b", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "green_chemistry", 1, "Q5", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "biomass_carbon_neutral", 1, "Q6a", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "ecological_footprint", 1, "Q6b", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "true_false_general", 1, "Q7a", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "personal_action", 1, "Q7b", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
]


QUIZ_SUPPORT = [
    Occurrence("2026_A_quiz_plastic", 2026, "A", "1Q", "quiz", "plastic_recycling", 8, "MR/CR/TR, 85%, 25%, 中国, バーゼル条約, 廃プラスチック", "source/2026_A_1Q_quizzes/20260407_2026_A_1Q_plastic_recycling_quiz_questions.md"),
    Occurrence("2026_A_quiz_plastic", 2026, "A", "1Q", "quiz", "carbon_neutrality", 1, "カーボンニュートラルに対する科学の貢献", "source/2026_A_1Q_quizzes/20260407_2026_A_1Q_plastic_recycling_quiz_questions.md"),
    Occurrence("2026_A_quiz_energy", 2026, "A", "1Q", "quiz", "energy_quality", 3, "エネルギー保存、質、熱移動の方向性", "source/2026_A_1Q_quizzes/20260414_2026_A_1Q_energy_hydrogen_quiz_questions.md"),
    Occurrence("2026_A_quiz_energy", 2026, "A", "1Q", "quiz", "climate_sustainability", 2, "パリ協定、3E+S", "source/2026_A_1Q_quizzes/20260414_2026_A_1Q_energy_hydrogen_quiz_questions.md"),
    Occurrence("2026_A_quiz_energy", 2026, "A", "1Q", "quiz", "hydrogen_ccs_fuelcell", 5, "CCS、水素、燃料電池、白金触媒、コスト", "source/2026_A_1Q_quizzes/20260414_2026_A_1Q_energy_hydrogen_quiz_questions.md"),
    Occurrence("2026_A_quiz_sustainability", 2026, "A", "1Q", "quiz", "climate_sustainability", 10, "人口、緩和と適応、MDGs/SDGs、Our Common Future、政策と科学", "source/2026_A_1Q_quizzes/undated_2026_A_1Q_environment_sustainability_quiz_questions.md"),
    Occurrence("2026_A_quiz_green_chemistry", 2026, "A", "1Q", "quiz", "green_chemistry", 4, "12原則、定義、ライフサイクル", "source/2026_A_1Q_quizzes/undated_2026_A_1Q_green_chemistry_pfas_quiz_questions.md"),
    Occurrence("2026_A_quiz_green_chemistry", 2026, "A", "1Q", "quiz", "pfas_cfc_novel_entities", 6, "CAS、CFC、PFAS/PFOS、Novel entities", "source/2026_A_1Q_quizzes/undated_2026_A_1Q_green_chemistry_pfas_quiz_questions.md"),
    Occurrence("2026_A_quiz_life", 2026, "A", "1Q", "quiz", "ecological_footprint", 1, "Q1", "source/2026_A_1Q_quizzes/undated_2026_A_1Q_life_engineering_quiz_questions.md"),
    Occurrence("2026_A_quiz_life", 2026, "A", "1Q", "quiz", "keystone_species", 3, "生物多様性、キーストーン種、フラッグシップ種", "source/2026_A_1Q_quizzes/undated_2026_A_1Q_life_engineering_quiz_questions.md"),
    Occurrence("2026_A_quiz_life", 2026, "A", "1Q", "quiz", "prtr_sds", 3, "PRTR 515物質、トルエン、発がん性", "source/2026_A_1Q_quizzes/undated_2026_A_1Q_life_engineering_quiz_questions.md"),
    Occurrence("2026_A_quiz_life", 2026, "A", "1Q", "quiz", "biomass_carbon_neutral", 1, "Q9", "source/2026_A_1Q_quizzes/undated_2026_A_1Q_life_engineering_quiz_questions.md"),
    Occurrence("2026_A_quiz_life", 2026, "A", "1Q", "quiz", "biorefinery_bioplastics", 3, "バイオリファイナリー、SDGs、バイオマスプラスチック", "source/2026_A_1Q_quizzes/undated_2026_A_1Q_life_engineering_quiz_questions.md"),
    Occurrence("2026_A_quiz_zero_carbon", 2026, "A", "1Q", "quiz", "climate_sustainability", 3, "SDGs/MDGs、MPI、エネルギー貧困", "source/2026_A_1Q_quizzes/undated_2026_A_1Q_zero_carbon_energy_quiz_questions.md"),
    Occurrence("2026_A_quiz_zero_carbon", 2026, "A", "1Q", "quiz", "energy_quality", 2, "E=mc^2、太陽の質量欠損計算", "source/2026_A_1Q_quizzes/undated_2026_A_1Q_zero_carbon_energy_quiz_questions.md"),
    Occurrence("2026_A_quiz_zero_carbon", 2026, "A", "1Q", "quiz", "fusion_energy", 5, "DT 反応 17.6 MeV、質量欠損、1GW 炉の Li 消費、海水 Li 資源", "source/2026_A_1Q_quizzes/undated_2026_A_1Q_zero_carbon_energy_quiz_questions.md"),
]


def topic_rows(occurrences: list[Occurrence], *, distinct_by_paper: bool) -> list[dict]:
    grouped: dict[str, list[Occurrence]] = defaultdict(list)
    for occ in occurrences:
        grouped[occ.topic].append(occ)

    rows = []
    for topic, items in grouped.items():
        papers = sorted({item.paper_id for item in items})
        total = len(papers) if distinct_by_paper else sum(item.count for item in items)
        rows.append(
            {
                "topic": topic,
                "label": TOPICS[topic]["label"],
                "bucket": TOPICS[topic]["bucket"],
                "total": total,
                "papers": papers,
                "years": sorted({item.year for item in items}),
                "details": [asdict(item) for item in items],
            }
        )
    return sorted(rows, key=lambda row: (-row["total"], row["label"]))


def prediction_rows(a_finals: list[Occurrence], quiz_support: list[Occurrence]) -> list[dict]:
    total_papers = len({occ.paper_id for occ in a_finals})
    final_presence = {row["topic"]: row["total"] for row in topic_rows(a_finals, distinct_by_paper=True)}
    current_counts = {row["topic"]: row["total"] for row in topic_rows(quiz_support, distinct_by_paper=False)}
    rows = []
    for topic in sorted(set(final_presence) | set(current_counts)):
        final_count = final_presence.get(topic, 0)
        current_count = current_counts.get(topic, 0)
        final_ratio = final_count / total_papers if total_papers else 0
        if final_count and current_count:
            evidence = "A past + 2026 quiz"
        elif final_count:
            evidence = "A past only"
        elif topic == "fusion_energy":
            evidence = "2026 A quiz direct + B past pattern"
        elif current_count:
            evidence = "2026 A quiz only"
        else:
            evidence = "weak"

        if final_ratio >= 0.8:
            tier = "S"
        elif final_ratio >= 0.5 and current_count > 0:
            tier = "S"
        elif final_ratio >= 0.5:
            tier = "A"
        elif topic == "fusion_energy" and current_count >= 5:
            tier = "A"
        elif final_ratio >= 0.3 or current_count >= 3:
            tier = "B"
        else:
            tier = "C"
        rows.append(
            {
                "topic": topic,
                "label": TOPICS[topic]["label"],
                "final_exam_presence": final_count,
                "total_a_finals": total_papers,
                "final_ratio": round(final_ratio, 3),
                "current_support_items": current_count,
                "tier": tier,
                "evidence": evidence,
            }
        )
    tier_order = {"S": 0, "A": 1, "B": 2, "C": 3}
    return sorted(rows, key=lambda row: (tier_order[row["tier"]], -row["final_exam_presence"], -row["current_support_items"], row["label"]))


def bucket_rows(rows: list[dict]) -> list[dict]:
    grouped: dict[str, int] = defaultdict(int)
    for row in rows:
        grouped[row["bucket"]] += row["total"]
    return [{"bucket": bucket, "total": total} for bucket, total in sorted(grouped.items(), key=lambda item: (-item[1], item[0]))]


def write_topic_frequency(path: Path, rows: list[dict], scoreboard: list[dict]) -> None:
    lines = [
        "# A クラス頻度集計",
        "",
        "## 過去問のテーマ出現",
        "",
        "| テーマ | 出現答案 | 年度 |",
        "|---|---:|---|",
    ]
    for row in rows:
        lines.append(f"| {row['label']} | {row['total']} | {', '.join(map(str, row['years']))} |")

    lines.extend(
        [
            "",
            "## 2026 補正後スコア",
            "",
            "| ランク | テーマ | 過去問出現 | 2026 小テスト支持 | 根拠の型 |",
            "|---|---|---:|---:|---|",
        ]
    )
    for row in scoreboard:
        lines.append(f"| {row['tier']} | {row['label']} | {row['final_exam_presence']} / {row['total_a_finals']} | {row['current_support_items']} | {row['evidence']} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    task_dir = Path(__file__).resolve().parents[1]
    build_dir = task_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    final_rows = topic_rows(PAST_EXAM_OCCURRENCES, distinct_by_paper=True)
    quiz_rows = topic_rows(QUIZ_SUPPORT, distinct_by_paper=False)
    scoreboard = prediction_rows(PAST_EXAM_OCCURRENCES, QUIZ_SUPPORT)

    summary = {
        "dataset_note": "A クラス過去問と 2026 A 小テストを手動タグ付けした頻度集計。講義資料メモだけの根拠は数値スコアから外し、小テストまたは過去問で確認できるものを優先する。",
        "source_counts": {
            "a_final_occurrences": len(PAST_EXAM_OCCURRENCES),
            "current_support_occurrences": len(QUIZ_SUPPORT),
            "a_final_papers": sorted({occ.paper_id for occ in PAST_EXAM_OCCURRENCES}),
        },
        "a_final_exam_presence": final_rows,
        "a_final_question_slots": topic_rows(PAST_EXAM_OCCURRENCES, distinct_by_paper=False),
        "a_2026_quiz_pdf_support": quiz_rows,
        "bucket_presence": bucket_rows(final_rows),
        "prediction_scoreboard": scoreboard,
        "all_occurrences": [asdict(occ) for occ in PAST_EXAM_OCCURRENCES + QUIZ_SUPPORT],
    }

    (build_dir / "analysis_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["topic\tlabel\ta_final_exam_presence\ta_total_finals\tcurrent_support_items\ttier\tevidence"]
    for row in scoreboard:
        lines.append(f"{row['topic']}\t{row['label']}\t{row['final_exam_presence']}\t{row['total_a_finals']}\t{row['current_support_items']}\t{row['tier']}\t{row['evidence']}")
    (build_dir / "prediction_scoreboard.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_topic_frequency(build_dir / "topic_frequency.md", final_rows, scoreboard)


if __name__ == "__main__":
    main()
