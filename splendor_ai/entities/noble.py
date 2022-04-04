from dataclasses import dataclass


@dataclass
class Noble:
    point_value: int
    req_w: int
    req_r: int
    req_u: int
    req_g: int
    req_b: int
