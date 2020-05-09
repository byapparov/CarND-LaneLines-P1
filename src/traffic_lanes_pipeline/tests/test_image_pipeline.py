import unittest
from src.traffic_lanes_pipeline.image_pipeline import process_image
import numpy as np


class TestLaneMethods(unittest.TestCase):

    def test_process_image(self):
        # TODO pipeline has hardcoded params for lane size
        height: int = 300
        width: int = 300
        layers: int = 3
        image = np.zeros((height, width, layers), np.uint8)

        # https://stackoverflow.com/questions/12881926/create-a-new-rgb-opencv-image-using-python
        # Here we want to split the image into two parts
        # colored in four segments
        image[0:height // 2:, 0:width // 2] = (255, 0, 0)  # (B, G, R)
        image[:, width // 2:width] = (0, 255, 0)
        image[0:height // 2, width // 2:width] = (0, 255, 255)
        image[height // 2:height, width // 2:width] = (255, 255, 255)

        process_image(image)
