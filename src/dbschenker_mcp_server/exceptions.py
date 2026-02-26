# Lays the foundations for a polymorphic hierarchy. Sustainable code!
class ShipmentError(Exception):
    def __init__(self, message):
        super().__init__("Shipment Error: " + message)


class ShipmentNotFoundError(ShipmentError):
    def __init__(self, message):
        super().__init__("Shipment not found: " + message)

class InvalidFormatError(ShipmentError):
    def __init__(self, message):
        super().__init__("Invalid Reference ID format: " + message)

class UnknownPageError(ShipmentError):
    def __init__(self, message):
        super().__init__("Unknown Page: " + message)
