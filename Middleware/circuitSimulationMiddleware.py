import numpy as np
import matplotlib.pyplot as plt
import sys

import PySpice
import PySpice.Logging.Logging as logging
from PySpice.Spice.Netlist import Circuit

from PySpice.Unit import *


class SimulationMiddleware:
    def __init__(self, circuit_name, canvas_components, operating_temp, nominal_temp):
        self.circuit_name = circuit_name
        self.components = canvas_components
        self.operating_temp = operating_temp
        self.nominal_temp = nominal_temp

    def init_circuit(self):
        logger = logging.setup_logging()

        if sys.platform == "linux" or sys.platform == "linux2":
            PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = "ngspice-subprocess"
        elif sys.platform == "win32":
            pass

        circuit = Circuit(self.circuit_name)

        circuit.R('R1', 'a', 'out', 9@u_kOhm)

    def string_to_pyspice_unit(unit_str):
        unit_mapping = {
            'V': @u_V,
            'kV': @u_kV,
            'A': @u_A,
            'Ohm': @u_Ohm,
            'kOhm': @u_kOhm
            'F': @u_F,
            'H': @u_H,
            'Hz': @u_Hz,
            'S': @u_S,
            'W': @u_W,
            'J': @u_J
        }

        # Get the corresponding PySpice unit
        if unit_str not in unit_mapping:
            raise ValueError(f"Unit '{unit}' is not recognized.")
        else:
            pyspice_unit = unit_mapping[unit]
            return pyspice_unit
