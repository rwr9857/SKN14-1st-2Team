from dataclasses import dataclass
from typing import Optional

@dataclass
class CarInfoDTO:
    car_id: Optional[int] = None
    car_full_name: Optional[str] = None
    car_model: Optional[int] = None
    car_brand: Optional[int] = None
    car_body_type: Optional[int] = None
    car_engine_type: Optional[int] = None
    car_fuel_type: Optional[int] = None
    car_price: Optional[int] = None
    car_horsepower: Optional[int] = None
    car_fuel_efficiency: Optional[int] = None
    car_size: Optional[int] = None
    car_img_url: Optional[str] = None

