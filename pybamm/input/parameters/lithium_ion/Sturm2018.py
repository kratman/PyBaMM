
def graphite_ocp_sturm2018(sto):
    raise NotImplementedError


def nmc_ocp_sturm2018(sto):
    raise NotImplementedError


def graphite_electrolyte_exchange_current_density_sturm2018(c_e, c_s_surf, c_s_max, temp):
    raise NotImplementedError


def nmc_electrolyte_exchange_current_density_sturm2018(c_e, c_s_surf, c_s_max, temp):
    raise NotImplementedError


def electrolyte_diffusivity_sturm2018(c_e, temp):
    raise NotImplementedError


def electrolyte_conductivity_sturm2018(c_e, temp):
    raise NotImplementedError


# Call dict via a function to avoid errors when editing in place
def get_parameter_values():
    """
    Parameters for an LG MJ1 cell, from the paper :footcite:t:`Sturm2018` and references
    therein.

    .. note::
        This parameter set does not claim to be representative of the true parameter
        values. Instead, these are parameter values that were used to fit SEI models to
        observed experimental data in the referenced papers.
    """

    return {
        "chemistry": "lithium_ion",
        # sei
        "Ratio of lithium moles to SEI moles": 2.0,  # x
        "Inner SEI reaction proportion": 0.5,  # x
        "Inner SEI partial molar volume [m3.mol-1]": 9.585e-05,  # x
        "Outer SEI partial molar volume [m3.mol-1]": 9.585e-05,  # x
        "SEI reaction exchange current density [A.m-2]": 1.5e-07,  # x
        "SEI resistivity [Ohm.m]": 200000.0,  # x
        "Outer SEI solvent diffusivity [m2.s-1]": 2.5000000000000002e-22,  # x
        "Bulk solvent concentration [mol.m-3]": 2636.0,  # x
        "Inner SEI open-circuit potential [V]": 0.1,  # x
        "Outer SEI open-circuit potential [V]": 0.8,  # x
        "Inner SEI electron conductivity [S.m-1]": 8.95e-14,  # x
        "Inner SEI lithium interstitial diffusivity [m2.s-1]": 1e-20,  # x
        "Lithium interstitial reference concentration [mol.m-3]": 15.0,  # x
        "Initial inner SEI thickness [m]": 2.5e-09,  # x
        "Initial outer SEI thickness [m]": 2.5e-09,  # x
        "EC initial concentration in electrolyte [mol.m-3]": 4541.0,  # x
        "EC diffusivity [m2.s-1]": 2e-18,  # x
        "SEI kinetic rate constant [m.s-1]": 1e-12,  # x
        "SEI open-circuit potential [V]": 0.4,  # x
        "SEI growth activation energy [J.mol-1]": 0.0,  # x
        "Negative electrode reaction-driven LAM factor [m3.mol-1]": 0.0,  # x
        "Positive electrode reaction-driven LAM factor [m3.mol-1]": 0.0,  # x
        # cell
        "Negative current collector thickness [m]": 1.2e-05,  # x
        "Negative electrode thickness [m]": 8.67e-05,
        "Separator thickness [m]": 1.2e-06,
        "Positive electrode thickness [m]": 6.62e-05,
        "Positive current collector thickness [m]": 1.6e-05,  # x
        "Electrode height [m]": 0.065,  # x
        "Electrode width [m]": 1.58,  # x
        "Cell cooling surface area [m2]": 0.00531,  # x
        "Cell volume [m3]": 2.42e-05,  # x
        "Cell thermal expansion coefficient [m.K-1]": 1.1e-06,  # x
        "Negative current collector conductivity [S.m-1]": 58411000.0,  # x
        "Positive current collector conductivity [S.m-1]": 36914000.0,  # x
        "Negative current collector density [kg.m-3]": 8960.0,  # x
        "Positive current collector density [kg.m-3]": 2700.0,  # x
        "Negative current collector specific heat capacity [J.kg-1.K-1]": 385.0,  # x
        "Positive current collector specific heat capacity [J.kg-1.K-1]": 897.0,  # x
        "Negative current collector thermal conductivity [W.m-1.K-1]": 401.0,  # x
        "Positive current collector thermal conductivity [W.m-1.K-1]": 237.0,  # x
        "Nominal cell capacity [A.h]": 3.35,
        "Current function [A]": 5.0,  # x
        "Contact resistance [Ohm]": 0,  # x
        # negative electrode
        "Negative electrode conductivity [S.m-1]": 100.0,
        "Maximum concentration in negative electrode [mol.m-3]": 34684.0,
        "Negative electrode diffusivity [m2.s-1]": 5.0e-14,
        "Negative electrode OCP [V]": graphite_ocp_sturm2018,
        "Negative electrode porosity": 0.216,
        "Negative electrode active material volume fraction": 0.694,
        "Negative particle radius [m]": 6.1e-06,
        "Negative electrode Bruggeman coefficient (electrolyte)": 1.5,
        "Negative electrode Bruggeman coefficient (electrode)": 0,  # x
        "Negative electrode charge transfer coefficient": 0.5,
        "Negative electrode double-layer capacity [F.m-2]": 0.2,  # x
        "Negative electrode exchange-current density [A.m-2]"
        "": graphite_electrolyte_exchange_current_density_sturm2018,
        "Negative electrode density [kg.m-3]": 2240.0,
        "Negative electrode specific heat capacity [J.kg-1.K-1]": 700.0,  # x
        "Negative electrode thermal conductivity [W.m-1.K-1]": 1.7,  # x
        "Negative electrode OCP entropic change [V.K-1]": 0.0,  # x
        # positive electrode
        "Positive electrode conductivity [S.m-1]": 0.17,
        "Maximum concentration in positive electrode [mol.m-3]": 50060.0,
        "Positive electrode diffusivity [m2.s-1]": 5e-13,
        "Positive electrode OCP [V]": nmc_ocp_sturm2018,
        "Positive electrode porosity": 0.171,
        "Positive electrode active material volume fraction": 0.745,
        "Positive particle radius [m]": 3.8e-06,
        "Positive electrode Bruggeman coefficient (electrolyte)": 1.85,
        "Positive electrode Bruggeman coefficient (electrode)": 0,  # x
        "Positive electrode charge transfer coefficient": 0.5,
        "Positive electrode double-layer capacity [F.m-2]": 0.2,  # x
        "Positive electrode exchange-current density [A.m-2]"
        "": nmc_electrolyte_exchange_current_density_sturm2018,
        "Positive electrode density [kg.m-3]": 4870.0,
        "Positive electrode specific heat capacity [J.kg-1.K-1]": 700.0,  # x
        "Positive electrode thermal conductivity [W.m-1.K-1]": 2.1,  # x
        "Positive electrode OCP entropic change [V.K-1]": 0.0,  # x
        # separator
        "Separator porosity": 0.45,
        "Separator Bruggeman coefficient (electrolyte)": 1.5,
        "Separator density [kg.m-3]": 397.0,  # x
        "Separator specific heat capacity [J.kg-1.K-1]": 700.0,  # x
        "Separator thermal conductivity [W.m-1.K-1]": 0.16,  # x
        # electrolyte
        "Initial concentration in electrolyte [mol.m-3]": 1000.0,
        "Cation transference number": 0.38,
        "Thermodynamic factor": 1.0,  # x
        "Electrolyte diffusivity [m2.s-1]": electrolyte_diffusivity_sturm2018,
        "Electrolyte conductivity [S.m-1]": electrolyte_conductivity_sturm2018,
        # experiment
        "Reference temperature [K]": 298.15,  # x
        "Total heat transfer coefficient [W.m-2.K-1]": 10.0,  # x
        "Ambient temperature [K]": 298.15,  # x
        "Number of electrodes connected in parallel to make a cell": 1.0,  # x
        "Number of cells connected in series to make a battery": 1.0,  # x
        "Lower voltage cut-off [V]": 2.5,  # x
        "Upper voltage cut-off [V]": 4.2,  # x
        "Open-circuit voltage at 0% SOC [V]": 2.5,  # x
        "Open-circuit voltage at 100% SOC [V]": 4.2,  # x
        "Initial concentration in negative electrode [mol.m-3]": 29866.0,  # x
        "Initial concentration in positive electrode [mol.m-3]": 17038.0,  # x
        "Initial temperature [K]": 298.15,  # x
        # citations
        "citations": ["Sturm2018"],
    }
