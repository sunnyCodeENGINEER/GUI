import numpy as np
from array import array
import matplotlib.pyplot as plt
import sys

import PySpice
import PySpice.Logging.Logging as logging
from PySpice.Spice.Netlist import Circuit

from PySpice.Unit import *

from PyQt6.QtCore import pyqtSignal, QObject
from Components.logger import logger


# from Middleware.resultPlot import plotView


# from Components.allTerminalComponent import OneTerminalComponent, ThreeTerminalComponent


class ResultPlot:
    def __init__(self, plot_label, x_axis, y_axis, x_axis_label, y_axis_label):
        self.plot_label = plot_label
        self.x_axis = x_axis
        self.x_axis_label = x_axis_label
        self.y_axis = y_axis
        self.y_axis_label = y_axis_label


class SimulationMiddleware:
    class Signals(QObject):
        simulationResult = pyqtSignal(np.ndarray)
        simulationData = pyqtSignal(str)

    def __init__(self, circuit_name, canvas_components, canvas_wires, analysis_type, var_1, var_2, operating_temp,
                 nominal_temp):
        self.circuit_name = circuit_name
        self.components = canvas_components
        self.wires = canvas_wires
        self.analysisType = analysis_type
        self.operating_temp = operating_temp
        self.nominal_temp = nominal_temp

        self.var_1 = var_1
        self.var_2 = var_2

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
            'uF': u_uF,
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

        self.signals = self.Signals()
        self.circuit = Circuit(self.circuit_name)
        self.result_plot = None

        # circuit models
        # self.circuit.model('MyDiode', 'D', IS=4.35 @ u_nA, RS=0.64 @ u_Ohm, BV=110 @ U_V,
        #                    IBV=0.0001 @ u_V, N=1.906)

        # self.test_circuit()
        try:
            logger.info("Extracting Components Information")
            component_ids = self.components.keys()
            for component_id in component_ids:
                component = self.components.get(component_id)
                print(component_id)
                # is_sub_circuit, sub_circuit_component = self.check_sub_circuit(component)
                # if is_sub_circuit:
                #     # sub_circuit_id =
                #     self.subCircuitElements.append(component)
                #     pass
                # else:
                #     self.get_circuit_representation(component)
                self.get_circuit_representation(component)
            logger.info("Components Information Extracted")
            logger.info("Creating PySpice Circuit")
            self.run_analysis()
        except Exception as e:
            print("error here")
            print(e)
            print(self.components.keys())

        # if self.analysisType == "Transient":
        #     try:
        #         self.run_analysis()
        #     except Exception as e:
        #         print(e)

        self.signals.simulationResult.connect(self.handle)

        if self.result_plot is not None:
            # self.signals.simulationResult.emit(self.result_plot)
            self.emit_result()
            # print(self.signals.simulationResult.emit(self.result_plot))

    def handle(self, results):
        print(f"emitting: {results}")

    def emit_result(self):
        print(self.result_plot)
        self.signals.simulationResult.emit(self.result_plot.x_axis)

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
        self.circuit.V("Vin", "In", self.circuit.gnd, 10 @ u_V)
        self.circuit.R(1, "In", "out", 9 @ u_kOhm)
        self.circuit.R(2, "out", self.circuit.gnd, 1 @ u_kOhm)

        print(self.circuit)
        print("analyzing")

        simulator = self.circuit.simulator(temperature=25, nominal_temperature=25)
        analysis = simulator.operating_point()
        print(analysis)
        print(float(analysis.nodes['out']))

    def show_specific_data(self, analysis):
        if self.analysisType == "Transient":
            return
        try:
            print(f"{self.selectedNodeName} - {float(analysis.nodes[self.selectedNode])}")
            data = f"{self.selectedNodeName} - {float(analysis.nodes[self.selectedNode])}"
            self.signals.simulationData.emit(data)
        except Exception as e:
            logger.info(e)

        if self.analysisType != "Operating Point":
            result = self.format_data(analysis)
            print(f"result {result}")
            result_plot = ResultPlot("", [], [], "", "")
            if self.analysisType == "Transient":
                result_plot = ResultPlot("Transient Analysis", np.array(analysis.time),
                                         np.array(analysis.nodes[self.selectedNode]), "Time", "Voltage")
                pass
            elif self.analysisType == "DC Sweep":
                result_plot = ResultPlot("DC Sweep", np.array(analysis.time),
                                         np.array(analysis.nodes[self.selectedNode]), "Time", "Voltage")
                pass
            self.signals.simulationResult.emit(np.array(analysis.time))

    def set_node(self, node, node_name):
        self.selectedNode = node
        self.selectedNodeName = node_name

    def get_sub_circuit(self):
        pass

    def get_circuit_representation(self, component):
        node_1, node_2, node_3 = None, None, None
        value = None
        component_unit = None
        value_unit = None
        is_error = False
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
            is_error = True

        if component.componentType == "Resistor":
            self.circuit.R(component.componentName, node_1, node_2, value_unit)

        elif component.componentType == "Source_DC":
            # self.circuit.V(component.componentName, node_1, node_2, value_unit)
            if self.analysisType == "DC Sweep":
                self.circuit.V("SourceDC1", node_1, node_2, value_unit)
            else:
                self.circuit.V(component.componentName, node_1, node_2, value_unit)
        elif component.componentType == "Source_AC":
            self.circuit.SinusoidalVoltageSource(component.componentName, node_1, node_2, amplitude=value_unit,
                                                 frequency=float(component.frequency) @ u_Hz)
            pass
        elif component.componentType == "Source_P":
            self.circuit.PulseVoltageSource(component.componentName, node_1, node_2,
                                            initial_value=float(component.initialValue) @ u_V, pulsed_value=value_unit,
                                            pulse_width=float(component.puleWidth) @ u_ms,
                                            period=float(component.period) @ u_ms)
            print(self.circuit)

        elif component.componentType == "Capacitor":
            self.circuit.C(component.componentName, node_1, node_2, value_unit)
        elif component.componentType == "Inductor":
            self.circuit.L(component.componentName, node_1, node_2, value_unit)
        elif component.componentType == "Diode":
            self.circuit.model(f'MyDiode', 'D', IS=float(component.Is) @ u_nA,
                               RS=float(component.Rs) @ u_Ohm, BV=float(component.BV) @ u_V,
                               IBV=float(component.IBV) @ u_V, N=float(component.N))
            # self.circuit.model('MyDiode', 'D', IS=4.35@u_nA, RS=0.64@u_Ohm, BV=110@u_V,
            #                                       IBV=0.0001@u_V, N=1.906)
            # pass
            self.circuit.Diode(component.componentName, node_1, node_2, model='MyDiode')

        # if not is_error:
        #     data2 = "There was an issue.\nPlease check your circuit diagram."
        #     self.signals.simulationData.emit(data2)
        print(self.circuit)
        # for line in self.circuit:
        #     try:
        #         self.signals.simulationData.emit(line)
        #         print(line)
        #     except Exception as e:
        #         print(e)

        # self.signals.simulationData.emit(data)

    def run_analysis(self):
        logger.info("Simulating Circuit")
        simulator = self.circuit.simulator(temperature=self.operating_temp, nominal_temperature=self.nominal_temp)
        analysis = simulator.operating_point()
        if self.analysisType == "Operating Point":
            analysis = simulator.operating_point()
        elif self.analysisType == "DC Sweep":
            step_time, end_value = None, None
            try:
                step_time = float(self.var_1)
                print(step_time)
            except Exception as e:
                logger.info(e)
                pass
            try:
                end_value = float(self.var_2)
                print(end_value)
            except Exception as e:
                logger.info(e)
                pass
            try:
                for component_id in self.components:
                    component = self.components.get(component_id)
                    # if component.componentType.startswith("Source"):
                    if component.componentName == "Source_DC-1":
                        # component.componentID = "SourceDC1"
                        analysis = simulator.dc(SourceDC1=slice(0, 5, 0.5))
                        result_plot = ResultPlot("DC Sweep Analysis", np.array(analysis.time),
                                                 np.array((analysis["wire-1"])), "Time", "Voltage")
                        self.result_plot = result_plot
                        self.signals.simulationResult.emit(self.result_plot.x_axis)
                        return self.result_plot
            except Exception as e:
                print(e)

        elif self.analysisType == "Transient":
            step_time, end_time = None, None
            try:
                step_time = float(self.var_1)
                print(step_time)
            except Exception as e:
                logger.info(e)
                pass
            try:
                end_time = float(self.var_2)
                print(end_time)
            except Exception as e:
                logger.info(e)
                pass

            analysis = simulator.transient(step_time=step_time, end_time=end_time)
            result_plot = ResultPlot("Transient Analysis", np.array(analysis.time),
                                     np.array((analysis["wire-1"])), "Time", "Voltage")
            # print(result_plot.x_axis)
            self.result_plot = result_plot
            # plotView.plot(self.result_plot.x_axis, self.result_plot.y_axis)
            self.signals.simulationResult.emit(self.result_plot.x_axis)
            return self.result_plot
            pass
        elif self.analysisType == "AC Analysis":
            start_freq, end_freq = None, None
            try:
                start_freq = float(self.var_1)
                print(start_freq)
            except Exception as e:
                logger.info(e)
                pass
            try:
                end_freq = float(self.var_2)
                print(end_freq)
            except Exception as e:
                logger.info(e)
                pass

            analysis = simulator.ac(start_frequency=start_freq@u_Hz, stop_frequency=end_freq@u_Hz, variation='dec',
                                    number_of_points=10)
            result_plot = ResultPlot("AC Analysis", np.array(analysis.time),
                                     np.array((analysis["wire-1"])), "Time", "Voltage")
            self.result_plot = result_plot
            self.signals.simulationResult.emit(self.result_plot.x_axis)
            return self.result_plot
            pass
        if self.selectedNode != "":
            try:
                self.show_specific_data(analysis)
            except Exception as e:
                print(e)

        print(analysis)

    def parent_connection(self, wire_id):
        print("parenting")
        wire = self.wires.get(wire_id)
        # Base case
        if not wire.connectedTo:
            if wire.wireID.startswith("ground"):
                return self.circuit.gnd
            else:
                return wire_id
        # Recursive case
        else:
            return self.parent_connection(wire.connectedTo[0])

    def format_data(self, analysis):
        simulation_result = {}
        for node in analysis.nodes.values():
            data_label = f"{str(node)}"  # node name
            simulation_result[data_label] = np.array(node)

        return simulation_result

        # self.signals.simulationResult.emit(simulation_result)

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
