from PIL import Image


class Julia:
    def __init__(self, width, height, max_iterations, c, scale=1.5):
        self.width = width
        self.height = height
        self.max_iterations = max_iterations
        self.c = complex(*c)
        self.scale = scale

        self.iterations = [0] * (width * height)
        self.histogram = [0] * max_iterations
        self.total_iterations = 0
        self.image = Image.new("RGB", (width, height))
        self.pixels = self.image.load()

    def to_complex(self, x, y):
        aspect_ratio = self.width / self.height
        real = (x / self.width - 0.5) * self.scale * 2 * aspect_ratio
        imag = (y / self.height - 0.5) * self.scale * 2
        return complex(real, imag)

    def get_iterations(self, z):
        for i in range(self.max_iterations):
            z = z * z + self.c
            if abs(z) > 2:
                return i
        return self.max_iterations

    def generate(self):
        self.reset()
        self.compute_iterations()
        self.render()
        self.image.save("julia.png")

    def reset(self):
        self.iterations = [0] * (self.width * self.height)
        self.histogram = [0] * self.max_iterations
        self.total_iterations = 0

    def compute_iterations(self):
        for y in range(self.height):
            for x in range(self.width):
                z0 = self.to_complex(x, y)
                i = self.get_iterations(z0)
                idx = y * self.width + x
                self.iterations[idx] = i
                if i < self.max_iterations:
                    self.histogram[i] += 1
                    self.total_iterations += 1

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                i = self.iterations[y * self.width + x]

                if i == self.max_iterations:
                    color = (0, 0, 0)
                else:
                    # Use histogram-based hue without smoothing
                    hue = sum(self.histogram[:i + 1]) / self.total_iterations
                    val = int(pow(255, hue))
                    val = min(val, 255)
                    color = (val, val, 255)  # blueish gradient

                self.pixels[x, y] = color
