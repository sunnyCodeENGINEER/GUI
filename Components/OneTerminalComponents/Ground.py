from Components.twoTerminalComponent import Component


class Ground(Component):
    def __init__(self, unique_id, name):
        super(Ground, self).__init__(unique_id, name)

        self.componentUnit = None
        self.componentType = "Passive"

