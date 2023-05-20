class CustomerNameDb:
    def __init__(self):
        self._name_map = {
            1: "Astra Nova",
            2: "Baxter Quantum",
            3: "Cassiopeia Starlight",
            4: "Draco Cosmos",
            5: "Echo Nebula",
            6: "Falcon Orion",
            7: "Galaxy Pulsar",
            8: "Halley Comet",
            9: "Ignis Solaris",
            10: "Jupiter Zenith"
        }

    def get_name(self, id):
        return self._name_map.get(id, "Unknown")
