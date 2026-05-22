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
    "recycling_plastics": {
        "label": "プラスチックリサイクル / MR・CR・TR",
        "bucket": "resource_materials",
    },
    "plastic_harm": {
        "label": "プラスチック環境影響（安定性・親油性・添加剤）",
        "bucket": "resource_materials",
    },
    "environmental_assessment": {
        "label": "環境影響評価（科学性・民主性・制度）",
        "bucket": "assessment_policy",
    },
    "renewable_assessment": {
        "label": "再生可能エネルギー事業と環境アセスメント",
        "bucket": "assessment_policy",
    },
    "energy_quality": {
        "label": "エネルギー形態とエネルギーの質",
        "bucket": "energy",
    },
    "heat_engine_efficiency": {
        "label": "熱機関 / カルノー効率",
        "bucket": "energy",
    },
    "sustainability_essay": {
        "label": "持続可能社会に関する総合論述",
        "bucket": "sustainability",
    },
    "fusion_energy_calc": {
        "label": "DT 核融合エネルギー計算",
        "bucket": "nuclear_radiation",
    },
    "nuclear_vs_fusion_safety": {
        "label": "核分裂 vs 核融合の安全性",
        "bucket": "nuclear_radiation",
    },
    "radiation_protection": {
        "label": "放射線防護 / 自然放射線",
        "bucket": "nuclear_radiation",
    },
    "radiation_effects": {
        "label": "確定的影響 / 確率的影響",
        "bucket": "nuclear_radiation",
    },
    "green_chemistry": {
        "label": "グリーンケミストリー / 持続可能な化学",
        "bucket": "chemicals_materials",
    },
    "materials_safety_elements": {
        "label": "元素戦略 / 材料安全の正誤問題",
        "bucket": "chemicals_materials",
    },
    "prtr_sds": {
        "label": "PRTR / SDS / 化学物質管理",
        "bucket": "chemicals_materials",
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
    "mpi_energy_poverty": {
        "label": "MPI / エネルギー貧困",
        "bucket": "life_environment",
    },
    "tipping_point": {
        "label": "地球環境 tipping point",
        "bucket": "climate",
    },
    "dampness": {
        "label": "WHO dampness",
        "bucket": "climate",
    },
    "true_false_general": {
        "label": "総合正誤問題（A クラスで頻出）",
        "bucket": "mixed",
    },
    "personal_action": {
        "label": "個人の省エネルギー・省資源実践問題",
        "bucket": "mixed",
    },
}


PAST_EXAM_OCCURRENCES = [
    Occurrence("2022_A_final", 2022, "A", "1Q", "final", "recycling_plastics", 1, "Q1", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_final", 2022, "A", "1Q", "final", "tipping_point", 1, "Q2", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_final", 2022, "A", "1Q", "final", "radiation_effects", 1, "Q3", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_final", 2022, "A", "1Q", "final", "radiation_protection", 1, "Q4", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_final", 2022, "A", "1Q", "final", "energy_quality", 1, "Q5", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_final", 2022, "A", "1Q", "final", "keystone_species", 1, "Q6", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_final", 2022, "A", "1Q", "final", "true_false_general", 1, "Q7", "source/problems/2022_environment_safety_A_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "recycling_plastics", 1, "Q1", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "dampness", 1, "Q2", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "radiation_protection", 1, "Q3", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "radiation_effects", 1, "Q3", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "energy_quality", 1, "Q4", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "green_chemistry", 1, "Q5", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "keystone_species", 1, "Q6", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "true_false_general", 1, "Q7", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2022_A_2Q", 2022, "A", "2Q", "final", "personal_action", 1, "Q8", "source/problems/2022_environment_safety_A_2Q_final_questions.md"),
    Occurrence("2023_A_2Q", 2023, "A", "2Q", "final", "recycling_plastics", 1, "Q1", "source/problems/2023_environment_safety_A_2Q_recreated_questions.md"),
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
    Occurrence("2025_A_2Q", 2025, "A", "2Q", "final", "recycling_plastics", 1, "Q1", "source/problems/2025_environment_safety_A_2Q_interpreted_questions.md"),
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
    Occurrence("2022_B_1Q", 2022, "B", "1Q", "final", "recycling_plastics", 1, "Q1", "source/problems/2022_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2022_B_1Q", 2022, "B", "1Q", "final", "energy_quality", 1, "Q3", "source/problems/2022_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2022_B_1Q", 2022, "B", "1Q", "final", "sustainability_essay", 1, "Q4", "source/problems/2022_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2022_B_1Q", 2022, "B", "1Q", "final", "fusion_energy_calc", 1, "Q5-1", "source/problems/2022_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2022_B_1Q", 2022, "B", "1Q", "final", "mpi_energy_poverty", 1, "Q5-2", "source/problems/2022_environment_safety_B_1Q_final_questions.md", "probable", "Question notes say 'MIA?' and answer reconstruction interprets it as MPI."),
    Occurrence("2022_B_1Q", 2022, "B", "1Q", "final", "keystone_species", 1, "Q6", "source/problems/2022_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2022_B_1Q", 2022, "B", "1Q", "final", "materials_safety_elements", 1, "Q7", "source/problems/2022_environment_safety_B_1Q_final_questions.md", "probable", "Question notes say the small quiz was likely reused directly."),
    Occurrence("2023_B_1Q", 2023, "B", "1Q", "final", "recycling_plastics", 1, "Q1", "source/problems/2023_environment_safety_B_1Q_recreated_questions.md"),
    Occurrence("2023_B_1Q", 2023, "B", "1Q", "final", "environmental_assessment", 1, "Q2", "source/problems/2023_environment_safety_B_1Q_recreated_questions.md"),
    Occurrence("2023_B_1Q", 2023, "B", "1Q", "final", "energy_quality", 1, "Q3", "source/problems/2023_environment_safety_B_1Q_recreated_questions.md"),
    Occurrence("2023_B_1Q", 2023, "B", "1Q", "final", "sustainability_essay", 1, "Q4", "source/problems/2023_environment_safety_B_1Q_recreated_questions.md"),
    Occurrence("2023_B_1Q", 2023, "B", "1Q", "final", "fusion_energy_calc", 1, "Q5-1", "source/problems/2023_environment_safety_B_1Q_recreated_questions.md"),
    Occurrence("2023_B_1Q", 2023, "B", "1Q", "final", "nuclear_vs_fusion_safety", 1, "Q5-2", "source/problems/2023_environment_safety_B_1Q_recreated_questions.md"),
    Occurrence("2023_B_1Q", 2023, "B", "1Q", "final", "keystone_species", 1, "Q6", "source/problems/2023_environment_safety_B_1Q_recreated_questions.md"),
    Occurrence("2023_B_1Q", 2023, "B", "1Q", "final", "materials_safety_elements", 1, "Q7", "source/problems/2023_environment_safety_B_1Q_recreated_questions.md"),
    Occurrence("2024_B_1Q", 2024, "B", "1Q", "final", "recycling_plastics", 1, "Q1", "source/problems/2024_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2024_B_1Q", 2024, "B", "1Q", "final", "environmental_assessment", 1, "Q2", "source/problems/2024_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2024_B_1Q", 2024, "B", "1Q", "final", "energy_quality", 1, "Q3", "source/problems/2024_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2024_B_1Q", 2024, "B", "1Q", "final", "sustainability_essay", 1, "Q4", "source/problems/2024_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2024_B_1Q", 2024, "B", "1Q", "final", "fusion_energy_calc", 1, "Q5-1", "source/problems/2024_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2024_B_1Q", 2024, "B", "1Q", "final", "nuclear_vs_fusion_safety", 1, "Q5-2", "source/problems/2024_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2024_B_1Q", 2024, "B", "1Q", "final", "prtr_sds", 1, "Q6", "source/problems/2024_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2024_B_1Q", 2024, "B", "1Q", "final", "materials_safety_elements", 1, "Q7", "source/problems/2024_environment_safety_B_1Q_final_questions.md"),
    Occurrence("2024_B_2Q", 2024, "B", "2Q", "final", "recycling_plastics", 1, "Q1", "source/problems/2024_environment_safety_B_2Q_final_questions.md"),
    Occurrence("2024_B_2Q", 2024, "B", "2Q", "final", "renewable_assessment", 1, "Q2", "source/problems/2024_environment_safety_B_2Q_final_questions.md"),
    Occurrence("2024_B_2Q", 2024, "B", "2Q", "final", "energy_quality", 1, "Q3", "source/problems/2024_environment_safety_B_2Q_final_questions.md"),
    Occurrence("2024_B_2Q", 2024, "B", "2Q", "final", "heat_engine_efficiency", 1, "Q4", "source/problems/2024_environment_safety_B_2Q_final_questions.md"),
    Occurrence("2024_B_2Q", 2024, "B", "2Q", "final", "sustainability_essay", 1, "Q5", "source/problems/2024_environment_safety_B_2Q_final_questions.md"),
    Occurrence("2024_B_2Q", 2024, "B", "2Q", "final", "fusion_energy_calc", 1, "Q6A", "source/problems/2024_environment_safety_B_2Q_final_questions.md"),
    Occurrence("2024_B_2Q", 2024, "B", "2Q", "final", "nuclear_vs_fusion_safety", 1, "Q6B", "source/problems/2024_environment_safety_B_2Q_final_questions.md"),
    Occurrence("2024_B_2Q", 2024, "B", "2Q", "final", "materials_safety_elements", 1, "Q7", "source/problems/2024_environment_safety_B_2Q_final_questions.md"),
    Occurrence("2025_B_2Q", 2025, "B", "2Q", "final", "recycling_plastics", 1, "Q1", "source/problems/2025_environment_safety_B_2Q_questions.md"),
    Occurrence("2025_B_2Q", 2025, "B", "2Q", "final", "renewable_assessment", 1, "Q2", "source/problems/2025_environment_safety_B_2Q_questions.md"),
    Occurrence("2025_B_2Q", 2025, "B", "2Q", "final", "energy_quality", 1, "Q3-1", "source/problems/2025_environment_safety_B_2Q_questions.md"),
    Occurrence("2025_B_2Q", 2025, "B", "2Q", "final", "heat_engine_efficiency", 1, "Q3-2", "source/problems/2025_environment_safety_B_2Q_questions.md"),
    Occurrence("2025_B_2Q", 2025, "B", "2Q", "final", "sustainability_essay", 1, "Q4", "source/problems/2025_environment_safety_B_2Q_questions.md"),
    Occurrence("2025_B_2Q", 2025, "B", "2Q", "final", "fusion_energy_calc", 1, "Q5-1", "source/problems/2025_environment_safety_B_2Q_questions.md"),
    Occurrence("2025_B_2Q", 2025, "B", "2Q", "final", "mpi_energy_poverty", 1, "Q5-2", "source/problems/2025_environment_safety_B_2Q_questions.md"),
    Occurrence("2025_B_2Q", 2025, "B", "2Q", "final", "keystone_species", 1, "Q6-1", "source/problems/2025_environment_safety_B_2Q_questions.md"),
    Occurrence("2025_B_2Q", 2025, "B", "2Q", "final", "biomass_carbon_neutral", 1, "Q6-2", "source/problems/2025_environment_safety_B_2Q_questions.md"),
    Occurrence("2025_B_2Q", 2025, "B", "2Q", "final", "materials_safety_elements", 1, "Q7", "source/problems/2025_environment_safety_B_2Q_questions.md"),
]


QUIZ_SUPPORT = [
    Occurrence("2026_B_quiz_plastic_recycling", 2026, "B", "1Q", "quiz", "recycling_plastics", 8, "MR/CR/TR, recycling rates, export destination, Basel Convention, waste plastics amendment", "source/2026_B_1Q_quizzes/20260410_2026_B_1Q_plastic_recycling_quiz_questions.md"),
    Occurrence("2026_B_quiz_plastic_recycling", 2026, "B", "1Q", "quiz", "sustainability_essay", 1, "science contribution to carbon neutrality", "source/2026_B_1Q_quizzes/20260410_2026_B_1Q_plastic_recycling_quiz_questions.md"),
    Occurrence("2026_B_quiz_materials_energy", 2026, "B", "1Q", "quiz", "materials_safety_elements", 8, "items 4,6,11,12,14,15,16 + element strategy cluster", "source/2026_B_1Q_quizzes/20260501_2026_B_1Q_materials_energy_quiz_questions.md"),
    Occurrence("2026_B_quiz_materials_energy", 2026, "B", "1Q", "quiz", "green_chemistry", 2, "items 5 and 10", "source/2026_B_1Q_quizzes/20260501_2026_B_1Q_materials_energy_quiz_questions.md"),
    Occurrence("2026_B_quiz_materials_energy", 2026, "B", "1Q", "quiz", "energy_quality", 4, "items 1,2,3,10", "source/2026_B_1Q_quizzes/20260501_2026_B_1Q_materials_energy_quiz_questions.md"),
    Occurrence("2026_B_quiz_materials_energy", 2026, "B", "1Q", "quiz", "sustainability_essay", 2, "items 8 and 10", "source/2026_B_1Q_quizzes/20260501_2026_B_1Q_materials_energy_quiz_questions.md"),
    Occurrence("2026_B_quiz_environment_assessment", 2026, "B", "1Q", "quiz", "environmental_assessment", 17, "purpose, role, science/democracy, history, law, screening", "source/2026_B_1Q_quizzes/20260508_2026_B_1Q_environment_assessment_quiz_questions.md"),
    Occurrence("2026_B_quiz_environment_assessment", 2026, "B", "1Q", "quiz", "renewable_assessment", 8, "renewables, target projects, linear case, future reform", "source/2026_B_1Q_quizzes/20260508_2026_B_1Q_environment_assessment_quiz_questions.md"),
    Occurrence("2026_B_quiz_energy_heat", 2026, "B", "1Q", "quiz", "energy_quality", 6, "energy conservation vs exergy, heat engine limits, fuel cell and PV", "source/2026_B_1Q_quizzes/undated_2026_B_1Q_energy_heat_engines_quiz_questions.md"),
    Occurrence("2026_B_quiz_energy_heat", 2026, "B", "1Q", "quiz", "heat_engine_efficiency", 4, "Carnot efficiency and turbine inlet temperature", "source/2026_B_1Q_quizzes/undated_2026_B_1Q_energy_heat_engines_quiz_questions.md"),
    Occurrence("2026_B_quiz_life", 2026, "B", "1Q", "quiz", "ecological_footprint", 1, "Q1", "source/2026_B_1Q_quizzes/undated_2026_B_1Q_life_engineering_quiz_questions.md"),
    Occurrence("2026_B_quiz_life", 2026, "B", "1Q", "quiz", "keystone_species", 2, "Q2-Q4 biodiversity and keystone/flagship", "source/2026_B_1Q_quizzes/undated_2026_B_1Q_life_engineering_quiz_questions.md"),
    Occurrence("2026_B_quiz_life", 2026, "B", "1Q", "quiz", "prtr_sds", 3, "Q5-Q7 PRTR count, emission ranking, carcinogenicity", "source/2026_B_1Q_quizzes/undated_2026_B_1Q_life_engineering_quiz_questions.md"),
    Occurrence("2026_B_quiz_life", 2026, "B", "1Q", "quiz", "biomass_carbon_neutral", 1, "Q9", "source/2026_B_1Q_quizzes/undated_2026_B_1Q_life_engineering_quiz_questions.md"),
    Occurrence("2026_B_quiz_life", 2026, "B", "1Q", "quiz", "biorefinery_bioplastics", 3, "Q10-Q12", "source/2026_B_1Q_quizzes/undated_2026_B_1Q_life_engineering_quiz_questions.md"),
    Occurrence("2026_B_quiz_radiation", 2026, "B", "1Q", "quiz", "radiation_protection", 10, "shielding, time-distance-shielding, natural radiation, body isotopes", "source/2026_B_1Q_quizzes/undated_2026_B_1Q_radiation_safety_quiz_questions.md"),
]


def topic_rows(occurrences: list[Occurrence], *, distinct_by_paper: bool) -> list[dict]:
    summary: dict[str, dict] = {}
    grouped: dict[str, list[Occurrence]] = defaultdict(list)
    for occ in occurrences:
        grouped[occ.topic].append(occ)

    for topic, items in grouped.items():
        papers = sorted({item.paper_id for item in items})
        years = sorted({item.year for item in items})
        total = len(papers) if distinct_by_paper else sum(item.count for item in items)
        summary[topic] = {
            "topic": topic,
            "label": TOPICS[topic]["label"],
            "bucket": TOPICS[topic]["bucket"],
            "total": total,
            "papers": papers,
            "years": years,
            "details": [
                {
                    "paper_id": item.paper_id,
                    "year": item.year,
                    "class_code": item.class_code,
                    "quarter": item.quarter,
                    "source_type": item.source_type,
                    "count": item.count,
                    "label": item.label,
                    "path": item.path,
                    "certainty": item.certainty,
                    "note": item.note,
                }
                for item in items
            ],
        }
    return sorted(summary.values(), key=lambda row: (-row["total"], row["label"]))


def prediction_rows(b_finals: list[Occurrence], quiz_support: list[Occurrence]) -> list[dict]:
    final_papers = {occ.paper_id for occ in b_finals}
    total_papers = len(final_papers)
    final_presence = {row["topic"]: row["total"] for row in topic_rows(b_finals, distinct_by_paper=True)}
    quiz_counts = {row["topic"]: row["total"] for row in topic_rows(quiz_support, distinct_by_paper=False)}
    topics = sorted(set(final_presence) | set(quiz_counts))
    rows = []
    for topic in topics:
        final_count = final_presence.get(topic, 0)
        quiz_count = quiz_counts.get(topic, 0)
        final_ratio = final_count / total_papers if total_papers else 0.0
        if final_ratio == 1.0:
            tier = "S"
        elif final_ratio >= 0.8 and quiz_count > 0:
            tier = "S"
        elif final_ratio >= 0.4 and quiz_count >= 8:
            tier = "A"
        elif final_ratio >= 0.6 and quiz_count > 0:
            tier = "A"
        elif final_ratio >= 0.4 or quiz_count >= 6:
            tier = "B"
        else:
            tier = "C"
        rows.append(
            {
                "topic": topic,
                "label": TOPICS[topic]["label"],
                "final_exam_presence": final_count,
                "total_b_finals": total_papers,
                "final_ratio": round(final_ratio, 3),
                "quiz_support_items": quiz_count,
                "tier": tier,
            }
        )
    return sorted(rows, key=lambda row: (row["tier"], -row["final_exam_presence"], -row["quiz_support_items"], row["label"]))


def bucket_rows(rows: list[dict]) -> list[dict]:
    grouped: dict[str, int] = defaultdict(int)
    for row in rows:
        grouped[row["bucket"]] += row["total"]
    return [{"bucket": bucket, "total": total} for bucket, total in sorted(grouped.items(), key=lambda item: (-item[1], item[0]))]


def main() -> None:
    task_dir = Path(__file__).resolve().parents[1]
    build_dir = task_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    all_past = PAST_EXAM_OCCURRENCES
    b_finals = [occ for occ in all_past if occ.class_code == "B"]
    a_finals = [occ for occ in all_past if occ.class_code == "A"]

    summary = {
        "dataset_note": (
            "This is a curated manual tagging of each past exam question and 2026 B-class quiz cluster. "
            "Frequencies are separated into past-final frequency and current-quiz support so A/B are not mixed."
        ),
        "source_counts": {
            "past_exam_occurrences": len(all_past),
            "b_final_occurrences": len(b_finals),
            "a_final_occurrences": len(a_finals),
            "quiz_support_occurrences": len(QUIZ_SUPPORT),
            "b_final_papers": sorted({occ.paper_id for occ in b_finals}),
        },
        "overall_past_exam_presence": topic_rows(all_past, distinct_by_paper=True),
        "overall_past_exam_slots": topic_rows(all_past, distinct_by_paper=False),
        "overall_bucket_presence": bucket_rows(topic_rows(all_past, distinct_by_paper=True)),
        "b_final_exam_presence": topic_rows(b_finals, distinct_by_paper=True),
        "b_final_question_slots": topic_rows(b_finals, distinct_by_paper=False),
        "b_2026_quiz_support": topic_rows(QUIZ_SUPPORT, distinct_by_paper=False),
        "prediction_scoreboard": prediction_rows(b_finals, QUIZ_SUPPORT),
        "all_occurrences": [asdict(occ) for occ in all_past + QUIZ_SUPPORT],
    }

    json_path = build_dir / "analysis_summary.json"
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "topic\tlabel\tb_final_exam_presence\tb_total_finals\tquiz_support_items\ttier",
    ]
    for row in summary["prediction_scoreboard"]:
        lines.append(
            f"{row['topic']}\t{row['label']}\t{row['final_exam_presence']}\t{row['total_b_finals']}\t{row['quiz_support_items']}\t{row['tier']}"
        )
    (build_dir / "prediction_scoreboard.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
