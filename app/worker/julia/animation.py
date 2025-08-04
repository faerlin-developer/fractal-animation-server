import logging
import math

import imageio.v2 as imageio
import numpy as np

from worker.julia.image import JuliaImage

logger = logging.getLogger(__name__)


# def perturb_c(c0):
#	return complex(c0.real + 0.01, c0.imag + 0.01)


def perturb_c(c0, angle_step=0.01):
	r = abs(c0)
	theta = math.atan2(c0.imag, c0.real)
	theta += angle_step
	return complex(r * math.cos(theta), r * math.sin(theta))


class JuliaAnimation:

	def __init__(self, width, height, max_iterations, c, scale=1.2):
		self.width = width
		self.height = height
		self.max_iterations = max_iterations
		self.c = complex(*c)
		self.scale = scale

	def generate_and_save(self, filename="julia.mp4"):
		""""""

		images = []
		for i in range(120):
			logging.info(f"i={i} z_re={self.c.real} z_im={self.c.imag}")

			julia = JuliaImage(
				width=self.width,
				height=self.height,
				max_iterations=self.max_iterations,
				c=(self.c.real, self.c.imag),
				scale=self.scale
			)

			julia.generate()

			images.append(julia.image)
			self.c = perturb_c(self.c)

		logging.info(f"creating mp4...")
		# noinspection PyUnresolvedReferences
		frames = [np.asarray(img) for img in images]
		imageio.mimsave(filename, frames, fps=24)

		logging.info(f"finish generating animation")
