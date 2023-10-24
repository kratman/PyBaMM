import pybamm
import numpy as np


def sic_ocp_sturm2019(sto):
    params = [2.78822910e-01, 9.55053661e-01, -1.82565434e+02,
              -4.70074568e-02, 2.89538197e+04,  1.64723478e-04,
              -1.06353035e+00,  2.43996536e+00, 3.22405988e-02,
              -5.37849275e-02,  1.34031755e+02,  4.03670553e-02,
              2.26933218e+00, -1.44503235e+00]
    pot = params[0]
    pot += params[1] * np.exp(params[2] * sto)
    pot += params[3] * np.tanh(params[4] * (sto - params[5]))
    pot += params[6] * np.tanh(params[7] * (sto - params[8]))
    pot += params[9] * np.tanh(params[10] * (sto - params[11]))
    pot += params[12] * sto + params[13] * sto**2
    return pot


def nmc_ocp_sturm2019(sto):
    params = [4.22843764e+00, -1.75032830e+00, -4.23924601e-01,
              2.13924294e+03, 9.99973289e-01, -1.75710279e+01,
              1.57608700e+01,  3.11479561e-01, 1.75819760e+01,
              1.57942423e+01, 3.11484291e-01, 6.08682148e-01]
    pot = params[0]
    pot += params[1] * sto
    pot += params[2] * np.tanh(params[3] * (sto - params[4]))
    pot += params[5] * np.tanh(params[6] * (sto - params[7]))
    pot += params[8] * np.tanh(params[9] * (sto - params[10]))
    pot += params[11] * sto ** 2
    return pot


def sic_entropic_sturm2019(sto, c_s_max):
    return 0


def nmc_entropic_sturm2019(sto, c_s_max):
    return 0


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
        "Negative electrode OCP entropic change [V.K-1]": sic_entropic_sturm2019,
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
        "Positive electrode OCP entropic change [V.K-1]": nmc_entropic_sturm2019,
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
