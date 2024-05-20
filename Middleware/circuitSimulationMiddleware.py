import numpy as np
import matplotlib.pyplot as plt
import sys

import PySpice
import PySpice.Logging.Logging as logging
from PySpice.Spice.Netlist import Circuit

from PySpice.Unit import *


# from Components.allTerminalComponent import OneTerminalComponent, ThreeTerminalComponent


class SimulationMiddleware:
    def __init__(self, circuit_name, canvas_components, canvas_wires, operating_temp, nominal_temp):
        self.circuit_name = circuit_name
        self.components = canvas_components
        self.wires = canvas_wires
        self.operating_temp = operating_temp
        self.nominal_temp = nominal_temp

        self.selectedNode: str = ""
        self.selectedNodeName: str = ""
        self.selectedComponent: str = ""

        self.unitMap = {
            'V': u_V,
            'kV': u_kV,
            'A': u_A,
            'Ohm': u_Ohm,
            'kOhm': u_kOhm,
            'F': u_F,
            'H': u_H,
            'Hz': u_Hz,
            'S': u_S,
            'W': u_W,
            'J': u_J
        }

        self.subCircuitElements = []
        self.subCircuits = {}

        # logger = logging.setup_logging()

        # if sys.platform == "linux" or sys.platform == "linux2":
        #     PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = "ngspice-subprocess"
        # elif sys.platform == "win32":
        #     pass

        self.circuit = Circuit(self.circuit_name)
        # self.test_circuit()
        try:
            component_ids = self.components.keys()
            for component_id in component_ids:
                component = self.components.get(component_id)
                is_sub_circuit, sub_circuit_component = self.check_sub_circuit(component)
                if is_sub_circuit:
                    # sub_circuit_id =
                    self.subCircuitElements.append(component)
                    pass
                else:
                    self.get_circuit_representation(component)
                self.run_analysis()
        except Exception as e:
            print(e)
            print(self.components.keys())

        value = 10
        unit2 = u_V
        print(value @ unit2)
    # def init_circuit(self):
    #     logger = logging.setup_logging()
    #
    #     if sys.platform == "linux" or sys.platform == "linux2":
    #         PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = "ngspice-subprocess"
    #     elif sys.platform == "win32":
    #         pass

    # self.circuit.R('R1', 'a', 'out', 9@u_kOhm)

    def check_sub_circuit(self, component):

        try:
            wired_to = component.terminal1To
            wire = self.wires.get(wired_to)
            if wire.connectedTo:
                sub_circuit_component = component
                return True, sub_circuit_component
        except Exception as e:
            print(e)
        try:
            wired_to = component.terminal2To
            wire = self.wires.get(wired_to)
            if wire.connectedTo:
                sub_circuit_component = component
                return True, sub_circuit_component
        except Exception as e:
            print(e)
        try:
            wired_to = component.terminal3To
            wire = self.wires.get(wired_to)
            if wire.connectedTo:
                sub_circuit_component = component
                return True, sub_circuit_component
        except Exception as e:
            print(e)

        return False, None

    def test_circuit(self):
        print("creating circuit")
        self.circuit.V("Vin", "In", self.circuit.gnd, 10@u_V)
        self.circuit.R(1, "In", "out", 9@u_kOhm)
        self.circuit.R(2, "out", self.circuit.gnd, 1@u_kOhm)

        print(self.circuit)
        print("analyzing")

        simulator = self.circuit.simulator(temperature=25, nominal_temperature=25)
        analysis = simulator.operating_point()
        print(analysis)
        print(float(analysis.nodes['out']))

    def show_specific_data(self, analysis):
        print(f"{self.selectedNodeName} - {float(analysis.nodes[self.selectedNode])}")

    def set_node(self, node, node_name):
        self.selectedNode = node
        self.selectedNodeName = node_name

    def get_sub_circuit(self):
        pass

    def get_circuit_representation(self, component):
        print("converting")
        node_1, node_2, node_3 = None, None, None
        value = None
        component_unit = None
        value_unit = None
        try:
            # node_1 = component.terminal1To
            node_1 = self.parent_connection(component.terminal1To)
            if component.terminal1To.startswith("ground"):
                node_1 = self.circuit.gnd
                print(node_1)
        except Exception as e:
            print(e)
        try:
            # node_2 = component.terminal2To
            node_2 = self.parent_connection(component.terminal2To)
            if component.terminal2To.startswith("ground"):
                node_2 = self.circuit.gnd
                print(node_2)
        except Exception as e:
            print(e)
        try:
            # node_3 = component.terminal3To
            node_3 = self.parent_connection(component.terminal3To)
            if component.terminal3To.startswith("ground"):
                node_3 = self.circuit.gnd
        except Exception as e:
            print(e)

        try:
            value = int(component.componentValue)
            print(f"\n\t\tComponent unit: {component.componentUnit}")
            comp_unit = component.componentUnit
            # component_unit = self.string_to_pyspice_unit(comp_unit)
            component_unit = self.unitMap.get(comp_unit)
            print(component_unit)
            value_unit = value @ component_unit
            print(f"value_unit: {value_unit}")
        except Exception as e:
            print(e)

        if component.componentType == "Resistor":
            self.circuit.R(component.componentName, node_1, node_2, value_unit)

        elif component.componentType == "Source_DC":
            self.circuit.V(component.componentName, node_1, node_2, value_unit)
            pass
        elif component.componentType == "Source_AC":
            pass

        print(self.circuit)
        # simulator = self.circuit.simulator(temperature=self.operating_temp, nominal_temperature=self.nominal_temp)
        # analysis = simulator.operating_point()
        # print(analysis)

    def run_analysis(self):
        simulator = self.circuit.simulator(temperature=self.operating_temp, nominal_temperature=self.nominal_temp)
        analysis = simulator.operating_point()
        print(analysis)
        if self.selectedNode != "":
            try:
                self.show_specific_data(analysis)
            except Exception as e:
                print(e)

    def parent_connection(self, wire_id):
        wire = self.wires.get(wire_id)
        # Base case
        if not wire.connectedTo:
            return wire_id
        # Recursive case
        else:
            return self.parent_connection(wire.connectedTo[0])


    def string_to_pyspice_unit(self, unit_str):
        print("mapping")
        unit_mapping = {
            'V': u_V,
            'kV': u_kV,
            'A': u_A,
            'Ohm': u_Ohm,
            'kOhm': u_kOhm,
            'F': u_F,
            'H': u_H,
            'Hz': u_Hz,
            'S': u_S,
            'W': u_W,
            'J': u_J
        }

        # Get the corresponding PySpice unit
        if unit_str not in unit_mapping:
            raise ValueError(f"Unit '{unit}' is not recognized.")
        else:
            pyspice_unit = unit_mapping[unit]
            print(pyspice_unit)
            return pyspice_unit


# test_sim = SimulationMiddleware("name", [], 25, 25)
