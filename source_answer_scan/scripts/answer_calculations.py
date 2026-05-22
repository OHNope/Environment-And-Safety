from pathlib import Path


def main() -> None:
    proton_mass = 1.6e-27  # kg, value used in the recreated exam notes
    speed_of_light = 3.0e8  # m/s
    ev_joule = 1.6e-19  # J
    mass_defect = 0.020 * proton_mass
    energy_joule = mass_defect * speed_of_light**2
    energy_ev = energy_joule / ev_joule

    out = Path("build/calculation_summary.md")
    out.write_text(
        "\n".join(
            [
                "# Calculation Summary",
                "",
                "## D-T fusion energy",
                "",
                f"- mass defect: 0.020 * {proton_mass:.2e} kg = {mass_defect:.2e} kg",
                f"- energy: dm c^2 = {energy_joule:.2e} J",
                f"- energy: {energy_ev:.2e} eV",
                "",
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
