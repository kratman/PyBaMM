import pybamm
import numpy as np


def sic_ocp_sturm2019(sto):
    a = 2.31794991e-01
    b = 3.45600198e-01
    c = -9.91250133e+03
    d = 5.12883954e-01
    e = -5.77907652e+02
    f = 5.74540667e-01
    g = -4.80814406e+01
    h = -4.08098181e-01
    i = 2.16300705e-01
    pot = a
    pot += b * np.exp(c * sto)
    pot += d * np.exp(e * sto)
    pot += f * np.exp(g * sto)
    pot += h * sto + i * sto ** 2
    return pot


def nmc_ocp_sturm2019(sto):
    a = 3.17566649
    b = 1.35487509
    c = 0.04694686
    d = -1.16220412
    e = -0.41835083
    f = 0.53203523
    pot = a
    pot += b * np.exp(c * sto)
    pot += d * sto + e * sto ** 2 + f * sto ** 3
    return pot


def sic_electrolyte_exchange_current_density_sturm2019(c_e, c_s_surf, c_s_max, temp):
    a = 3e-11 * pybamm.constants.F
    e_r = 3600.0  # In Kelvin
    arrhenius = a * np.exp(e_r * (1 / 298.15 - 1 / temp))
    concentrations = c_e ** 0.5 * c_s_surf ** 0.5 * (c_s_max - c_s_surf) ** 0.5
    return arrhenius * concentrations


def nmc_electrolyte_exchange_current_density_sturm2019(c_e, c_s_surf, c_s_max, temp):
    a = 1e-11 * pybamm.constants.F
    e_r = 3600.0  # In Kelvin
    arrhenius = a * np.exp(e_r * (1 / 298.15 - 1 / temp))
    concentrations = c_e ** 0.5 * c_s_surf ** 0.5 * (c_s_max - c_s_surf) ** 0.5
    return arrhenius * concentrations


def electrolyte_diffusivity_sturm2019(c_e, temp):
    c = c_e / 1000
    exponent = -4.43 - (54.0 / (temp - 229 - 5 * c)) - 0.22 * c
    diffusivity = 1e-3 * (10 ** exponent)
    return diffusivity


def electrolyte_conductivity_sturm2019(c_e, temp):
    c = c_e / 1000
    cond = -10.5
    cond += 0.668 * c
    cond += 0.494 * (c ** 2)
    cond += 0.074 * temp
    cond += -0.0178 * c * temp
    cond += -8.86e-4 * (c ** 2) * temp
    cond += -6.96e-5 * (temp ** 2)
    cond += 2.8e-5 * c * (temp ** 2)
    return 0.1 * c * (cond ** 2)


# Call dict via a function to avoid errors when editing in place
def get_parameter_values():
    """
    Parameters for an LG MJ1 cell, from the paper :footcite:t:`Sturm2019` and references
    therein.

    .. note::
        This parameter set does not claim to be representative of the true parameter
        values. Instead, these are parameter values that were used to fit SEI models to
        observed experimental data in the referenced papers.
    """

    return {
        "chemistry": "lithium_ion",
        # cell
        "Negative current collector thickness [m]": 1.1e-05,
        "Negative electrode thickness [m]": 8.67e-05,
        "Separator thickness [m]": 1.2e-05,
        "Positive electrode thickness [m]": 6.62e-05,
        "Positive current collector thickness [m]": 1.73e-05,
        "Electrode height [m]": 0.058,
        "Electrode width [m]": 0.615,
        "Negative current collector conductivity [S.m-1]": 5.96e7,
        "Positive current collector conductivity [S.m-1]": 3.78e7,
        "Negative current collector density [kg.m-3]": 8950.0,
        "Positive current collector density [kg.m-3]": 4870.0,
        "Negative current collector specific heat capacity [J.kg-1.K-1]": 385.0,
        "Positive current collector specific heat capacity [J.kg-1.K-1]": 903.0,
        "Negative current collector thermal conductivity [W.m-1.K-1]": 398.0,
        "Positive current collector thermal conductivity [W.m-1.K-1]": 238.0,
        "Nominal cell capacity [A.h]": 3.35,
        "Current function [A]": 3.35,
        # negative electrode
        "Negative electrode conductivity [S.m-1]": 100.0,
        "Maximum concentration in negative electrode [mol.m-3]": 34684.0,
        "Negative electrode diffusivity [m2.s-1]": 5.0e-14,
        "Negative electrode OCP [V]": sic_ocp_sturm2019,
        "Negative electrode porosity": 0.216,
        "Negative electrode active material volume fraction": 0.694,
        "Negative particle radius [m]": 6.1e-06,
        "Negative electrode Bruggeman coefficient (electrolyte)": 1.5,
        "Negative electrode Bruggeman coefficient (electrode)": 0,
        "Negative electrode charge transfer coefficient": 0.5,
        "Negative electrode exchange-current density [A.m-2]"
        "": sic_electrolyte_exchange_current_density_sturm2019,
        "Negative electrode density [kg.m-3]": 2240.0,
        "Negative electrode specific heat capacity [J.kg-1.K-1]": 867.0,
        "Negative electrode thermal conductivity [W.m-1.K-1]": 1.04,
        "Negative electrode OCP entropic change [V.K-1]": 0.0,  # Function
        # Positive electrode
        "Positive electrode conductivity [S.m-1]": 0.17,
        "Maximum concentration in positive electrode [mol.m-3]": 50060.0,
        "Positive electrode diffusivity [m2.s-1]": 5e-13,
        "Positive electrode OCP [V]": nmc_ocp_sturm2019,
        "Positive electrode porosity": 0.171,
        "Positive electrode active material volume fraction": 0.745,
        "Positive particle radius [m]": 3.8e-06,
        "Positive electrode Bruggeman coefficient (electrolyte)": 1.85,
        "Positive electrode Bruggeman coefficient (electrode)": 0,
        "Positive electrode charge transfer coefficient": 0.5,
        "Positive electrode exchange-current density [A.m-2]"
        "": nmc_electrolyte_exchange_current_density_sturm2019,
        "Positive electrode density [kg.m-3]": 4870.0,
        "Positive electrode specific heat capacity [J.kg-1.K-1]": 840.1,
        "Positive electrode thermal conductivity [W.m-1.K-1]": 1.58,
        "Positive electrode OCP entropic change [V.K-1]": 0.0,  # Function
        # Separator
        "Separator porosity": 0.45,
        "Separator Bruggeman coefficient (electrolyte)": 1.5,
        "Separator density [kg.m-3]": 1009.0,
        "Separator specific heat capacity [J.kg-1.K-1]": 1978.2,
        "Separator thermal conductivity [W.m-1.K-1]": 0.33,
        # Electrolyte
        "Initial concentration in electrolyte [mol.m-3]": 1000.0,
        "Cation transference number": 0.38,
        "Thermodynamic factor": 1.0,
        "Electrolyte diffusivity [m2.s-1]": electrolyte_diffusivity_sturm2019,
        "Electrolyte conductivity [S.m-1]": electrolyte_conductivity_sturm2019,
        # Experiment
        "Reference temperature [K]": 298.15,
        "Ambient temperature [K]": 298.15,
        "Number of electrodes connected in parallel to make a cell": 1.0,
        "Number of cells connected in series to make a battery": 1.0,
        "Lower voltage cut-off [V]": 2.5,
        "Upper voltage cut-off [V]": 4.2,
        "Open-circuit voltage at 0% SOC [V]": 2.5,
        "Open-circuit voltage at 100% SOC [V]": 4.2,
        "Initial concentration in negative electrode [mol.m-3]": 30163.0,
        "Initial concentration in positive electrode [mol.m-3]": 13208.0,
        "Initial temperature [K]": 298.15,
        # citations
        "citations": ["Sturm2019"],
    }
