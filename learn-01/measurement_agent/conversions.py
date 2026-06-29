from unit import Unit

length_conversions = {
    "meter": Unit(name="Meter", symbol="m", conversion_factor=1.0),
    "kilometer": Unit(name="Kilometer", symbol="km", conversion_factor=1000.0),
    "centimeter": Unit(name="Centimeter", symbol="cm", conversion_factor=0.01),
    "millimeter": Unit(name="Millimeter", symbol="mm", conversion_factor=0.001),
    "micrometer": Unit(name="Micrometer", symbol="µm", conversion_factor=1e-6),
    "nanometer": Unit(name="Nanometer", symbol="nm", conversion_factor=1e-9),
    "mile": Unit(name="Mile", symbol="mi", conversion_factor=1609.34),
    "yard": Unit(name="Yard", symbol="yd", conversion_factor=0.9144),
    "foot": Unit(name="Foot", symbol="ft", conversion_factor=0.3048),
    "inch": Unit(name="Inch", symbol="in", conversion_factor=0.0254)   
}