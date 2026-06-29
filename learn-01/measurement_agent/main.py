from unit import Unit
from length import Length

def main():
    # Create a Unit instance for meters
    length_in_meters = Length.of(5, "meter")
    print(length_in_meters.convert_to("centimeter"))  # Output: 500 Centimeter (cm) - Conversion Factor: 100.0

if __name__ == "__main__":
    main()