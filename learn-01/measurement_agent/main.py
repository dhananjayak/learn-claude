from unit import Unit
from length import Length

def main():
    # Create a Unit instance for meters
    meter_unit = Unit(name="Meter", symbol="m", conversion_factor=1.0)
    
    # Create a Length instance using the meter unit
    length_in_meters = Length(value=5.0, unit=meter_unit)
    
    # Print the Length instance
    print(length_in_meters)

if __name__ == "__main__":
    main()