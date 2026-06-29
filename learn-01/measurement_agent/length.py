from unit import Unit
from conversions import length_conversions

class Length:
    def __init__(self, value: float, unit: Unit):
        self.value = value
        self.unit = unit

    def __str__(self):
        return f"{self.value} {self.unit}"
    
    def convert_to(self, target_unit_name: str):
        if target_unit_name not in length_conversions:
            raise ValueError(f"Unit '{target_unit_name}' is not defined in length conversions.")
        
        target_unit = length_conversions[target_unit_name]
        converted_value = self.value * (self.unit.conversion_factor / target_unit.conversion_factor)
        
        return Length(converted_value, target_unit) 
    
    @staticmethod
    def of(value: float, unit_name: str):
        if unit_name not in length_conversions:
            raise ValueError(f"Unit '{unit_name}' is not defined in length conversions.")
        
        unit = length_conversions[unit_name]

        return Length(value, unit)