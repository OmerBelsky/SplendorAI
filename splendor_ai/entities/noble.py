from dataclasses import dataclass
from typing import Dict, List

from splendor_ai.entities.gem_color import GemColor
NOBLE_VECTOR_SIZE = 6

@dataclass
class Noble:
    req_w: int
    req_r: int
    req_u: int
    req_g: int
    req_b: int
    point_value: int = 3


    @property
    def requirements(self) -> Dict[GemColor, int]:
        return {
            GemColor.WHITE: self.req_w,
            GemColor.RED: self.req_r,
            GemColor.BLUE: self.req_u,
            GemColor.GREEN: self.req_g,
            GemColor.BLACK: self.req_b
        }

    @property
    def vectorized_state(self) -> List[int]:
        return [self.point_value, self.req_w, self.req_r, self.req_u, self.req_g, self.req_b]
