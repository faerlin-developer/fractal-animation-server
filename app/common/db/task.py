from dataclasses import dataclass


@dataclass
class FractalTask:
	id: int
	z_re: float
	z_im: float
