from dataclasses import dataclass

@dataclass
class CarInfo:
    id: int
    model_name: str
    body_type: str
    fuel_type: str
    price: int
    power: int
    fuel_efficiency: float
    model_year: str
    size: float
    engine_type: str
    image_link: str
    brand: str

