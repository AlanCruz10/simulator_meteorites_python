from pydantic import BaseModel
from typing import List


class Meteorite(BaseModel):
    id: int
    coordinate_x: int | float
    coordinate_z: int | float
    probability_explosion: int | float
    parts_explodes: int
    trajectory_x: List[float | int]
    trajectory_z: List[float | int]
    time_minute: int


class MeteoriteTwo(BaseModel):
    id: int
    x: int | float
    z: int | float
    x_speed: int | float
    z_speed: int | float
    trajectory_x: List[float | int]
    trajectory_z: List[float | int]
    trajectory_x_speed: List[float | int]
    trajectory_z_speed: List[float | int]
    status: str
