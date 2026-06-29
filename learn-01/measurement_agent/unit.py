class Unit:
    def __init__(self, name: str, symbol: str, conversion_factor: float):
        self.name = name
        self.symbol = symbol
        self.conversion_factor = conversion_factor

    def __str__(self):
        return f"{self.name} ({self.symbol}) - Conversion Factor: {self.conversion_factor}"    