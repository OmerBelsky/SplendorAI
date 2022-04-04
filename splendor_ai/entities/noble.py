from dataclasses import dataclass


@dataclass
class Noble:
    req_w: int
    req_r: int
    req_u: int
    req_g: int
    req_b: int
    point_value: int = 3
