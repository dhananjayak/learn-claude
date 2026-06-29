from unit import Unit

class Length:
    def __init__(self, value: float, unit: str):
        self.value = value
        self.unit = unit

    def __str__(self):
        return f"{self.value} {self.unit}"