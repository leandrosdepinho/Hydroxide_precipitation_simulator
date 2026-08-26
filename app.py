import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# HYDROXIDE PRECIPITATION SIMULATOR
# ============================================================

st.set_page_config(
    page_title="Hydroxide Precipitation Simulator",
    page_icon="🧪",
    layout="wide"
)


# ============================================================
# DATABASE
# ============================================================

HYDROXIDE_DATABASE = {

    "Ag+":    {"ksp": 2.0e-8,  "y": 1},
    "Al3+":   {"ksp": 1.0e-33, "y": 3},
    "Ba2+":   {"ksp": 5.0e-3,  "y": 2},
    "Be2+":   {"ksp": 6.9e-22, "y": 2},
    "Bi3+":   {"ksp": 4.0e-31, "y": 3},
    "Ca2+":   {"ksp": 5.5e-6,  "y": 2},
    "Cd2+":   {"ksp": 2.5e-14, "y": 2},
    "Ce3+":   {"ksp": 1.6e-20, "y": 3},
    "Ce4+":   {"ksp": 1.5e-51, "y": 4},
    "Co2+":   {"ksp": 1.3e-15, "y": 2},
    "Cr3+":   {"ksp": 6.3e-31, "y": 3},
    "Cu2+":   {"ksp": 2.2e-20, "y": 2},
    "Dy3+":   {"ksp": 1.4e-22, "y": 3},
    "Er3+":   {"ksp": 1.3e-22, "y": 3},
    "Eu3+":   {"ksp": 3.4e-24, "y": 3},
    "Fe2+":   {"ksp": 8.0e-16, "y": 2},
    "Fe3+":   {"ksp": 1.0e-39, "y": 3},
    "Ga3+":   {"ksp": 7.1e-36, "y": 3},
    "Gd3+":   {"ksp": 1.8e-23, "y": 3},
    "Hf4+":   {"ksp": 1.5e-52, "y": 4},
    "Hg2+":   {"ksp": 3.0e-26, "y": 2},
    "Ho3+":   {"ksp": 1.5e-22, "y": 3},
    "In3+":   {"ksp": 1.0e-33, "y": 3},
    "La3+":   {"ksp": 2.0e-21, "y": 3},
    "Lu3+":   {"ksp": 2.5e-24, "y": 3},
    "Mg2+":   {"ksp": 1.5e-11, "y": 2},
    "Mn2+":   {"ksp": 1.9e-13, "y": 2},
    "Nb5+":   {"ksp": 1.0e-62, "y": 5},
    "Nd3+":   {"ksp": 1.0e-31, "y": 3},
    "Ni2+":   {"ksp": 2.0e-15, "y": 2},
    "Pb2+":   {"ksp": 1.2e-15, "y": 2},
    "Pr3+":   {"ksp": 1.0e-23, "y": 3},
    "Sc3+":   {"ksp": 8.0e-31, "y": 3},
    "Sm3+":   {"ksp": 9.0e-25, "y": 3},
    "Sn2+":   {"ksp": 5.0e-26, "y": 2},
    "Sn4+":   {"ksp": 1.0e-56, "y": 4},
    "Sr2+":   {"ksp": 3.2e-4,  "y": 2},
    "Ta5+":   {"ksp": 1.0e-64, "y": 5},
    "Tb3+":   {"ksp": 1.6e-24, "y": 3},
    "Th4+":   {"ksp": 1.0e-50, "y": 4},
    "Ti4+":   {"ksp": 1.0e-53, "y": 4},
    "Tl+":    {"ksp": 1.4e-4,  "y": 1},
    "Tl3+":   {"ksp": 1.7e-39, "y": 3},
    "Tm3+":   {"ksp": 1.1e-22, "y": 3},
    "U4+":    {"ksp": 1.0e-52, "y": 4},
    "UO2_2+": {"ksp": 1.1e-22, "y": 2},
    "V3+":    {"ksp": 7.0e-36, "y": 3},
    "VO2+":   {"ksp": 7.9e-24, "y": 2},
    "Y3+":    {"ksp": 8.0e-23, "y": 3},
    "Yb3+":   {"ksp": 2.8e-24, "y": 3},
    "Zn2+":   {"ksp": 3.0e-17, "y": 2},
    "Zr4+":   {"ksp": 1.0e-62, "y": 4}
}


# ============================================================
# TITLE
# ============================================================

st.title("🧪 Hydroxide Precipitation Simulator")

st.write(
    "Select the metals you want to simulate and enter "
    "their initial concentrations."
)


# ============================================================
# METAL SELECTION
# ============================================================

st.subheader("Metal Selection")

selected_metals = []

metal_names = list(HYDROXIDE_DATABASE.keys())

# Three columns for the metal selection
columns = st.columns(3)

for i, metal in enumerate(metal_names):

    column = columns[i % 3]

    with column:

        selected = st.checkbox(
            metal,
            key=f"select_{metal}"
        )

        if selected:

            concentration = st.number_input(
                f"Initial concentration of {metal} (M)",
                min_value=0.0,
                value=0.05,
                format="%.6g",
                key=f"conc_{metal}"
            )

            selected_metals.append({
                "name": metal,
                "initial_conc": concentration,
                "ksp": HYDROXIDE_DATABASE[metal]["ksp"],
                "y": HYDROXIDE_DATABASE[metal]["y"]
            })


# ============================================================
# PH RANGE
# ============================================================

st.subheader("pH Range")

ph_min, ph_max = st.slider(
    "Select the pH range:",
    min_value=0.0,
    max_value=14.0,
    value=(0.0, 14.0),
    step=1.0
)


# ============================================================
# SIMULATE BUTTON
# ============================================================

simulate = st.button(
    "▶ SIMULATE",
    type="primary",
    use_container_width=True
)


# ============================================================
# SIMULATION
# ============================================================

if simulate:

    # --------------------------------------------------------
    # Validate metal selection
    # --------------------------------------------------------

    if len(selected_metals) == 0:

        st.warning(
            "Please select at least one metal."
        )

        st.stop()


    # --------------------------------------------------------
    # Validate concentrations
    # --------------------------------------------------------

    for metal in selected_metals:

        if metal["initial_conc"] <= 0:

            st.error(
                f"Please enter a concentration greater than "
                f"zero for {metal['name']}."
            )

            st.stop()


    # --------------------------------------------------------
    # Generate pH range
    # --------------------------------------------------------

    ph_range = np.linspace(
        ph_min,
        ph_max,
        1000
    )


    # --------------------------------------------------------
    # Chemical calculations
    # --------------------------------------------------------

    simulation_results = []

    for ph in ph_range:

        # At 25 °C:
        #
        # Kw = [H+][OH-] = 1.0 × 10^-14
        #
        # Therefore:
        #
        # [OH-] = 10^(pH - 14)

        free_oh = 10 ** (ph - 14)

        data_row = {
            "pH": ph
        }


        for metal in selected_metals:

            # ------------------------------------------------
            # Hydroxide equilibrium:
            #
            # M(OH)y(s) ⇌ M + y OH-
            #
            # Ksp = [M][OH-]^y
            #
            # Therefore:
            #
            # [M] = Ksp / [OH-]^y
            # ------------------------------------------------

            solubility_limit = (
                metal["ksp"]
                / (free_oh ** metal["y"])
            )


            # The dissolved concentration cannot exceed
            # the initial analytical concentration.

            real_solubility = np.clip(
                solubility_limit,
                0,
                metal["initial_conc"]
            )


            # ------------------------------------------------
            # Percentage precipitated
            # ------------------------------------------------

            precipitation_pct = (
                (
                    metal["initial_conc"]
                    - real_solubility
                )
                / metal["initial_conc"]
            ) * 100


            data_row[metal["name"]] = np.clip(
                precipitation_pct,
                0,
                100
            )


        simulation_results.append(data_row)


    # ========================================================
    # DATAFRAME
    # ========================================================

    df_results = pd.DataFrame(
        simulation_results
    )


    # ========================================================
    # GRAPH
    # ========================================================

    st.subheader("Precipitation Curve")

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )


    for metal in selected_metals:

        ax.plot(
            df_results["pH"],
            df_results[metal["name"]],
            label=(
                f"{metal['name']} "
                f"(Ksp = {metal['ksp']:.1e})"
            ),
            linewidth=2.5
        )


    ax.set_title(
        "Hydroxide Precipitation",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel(
        "pH",
        fontsize=12
    )

    ax.set_ylabel(
        "Precipitated (%)",
        fontsize=12
    )

    ax.set_xlim(
        ph_min,
        ph_max
    )

    ax.set_ylim(
        0,
        100
    )

    ax.set_xticks(
        np.arange(
            ph_min,
            ph_max + 1,
            1
        )
    )

    ax.set_yticks(
        np.arange(
            0,
            101,
            10
        )
    )

    ax.grid(
        True,
        linestyle="--",
        alpha=0.5
    )

    ax.legend()

    fig.tight_layout()

    st.pyplot(fig)


    # ========================================================
    # SELECTED METALS SUMMARY
    # ========================================================

    st.subheader("Selected Metals")

    summary = pd.DataFrame({

        "Metal": [
            metal["name"]
            for metal in selected_metals
        ],

        "Initial concentration (M)": [
            metal["initial_conc"]
            for metal in selected_metals
        ],

        "Ksp": [
            metal["ksp"]
            for metal in selected_metals
        ],

        "OH⁻ coefficient (y)": [
            metal["y"]
            for metal in selected_metals
        ]

    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )
