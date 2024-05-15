from Components.allTerminalComponent import ThreeTerminalComponent


class TestTransistor(ThreeTerminalComponent):
    def __init__(self, unique_id, name):
        super(TestTransistor, self).__init__(unique_id, name)

        self.componentUnit = "kOhm"
        # self.componentName = "Capacitor"
        self.componentType = "Transistor"
