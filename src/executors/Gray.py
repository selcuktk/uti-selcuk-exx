"""
    It is one of the preprocessing components in which the image is rotated.
"""

import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.SelcukExx.src.utils.response import build_response_gray
from components.SelcukExx.src.models.PackageModel import PackageModel


class Gray(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.darkness_value = None
        self.lightness = None
        self.image = self.request.get_param("inputImageOne")
        load_param()

    def load_param(self):
        if self.request.get_param("Grayness") == "Dark":
            self.darkness_value = self.request.get_param("DarknessValue")
        else:
            self.lightness = self.request.get_param("Lightness")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def gray_brightness(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.request.get_param("Grayness") == "Dark":
            darkness_factor = 1 - (self.darkness_value * 0.08)
            img = np.clip(img * darkness_factor, 0, 255).astype(np.uint8)
        elif not self.lightness:
            img = np.clip(img * 1.5, 0, 255).astype(np.uint8)
        else:
            img = np.clip(img * 2, 0, 255).astype(np.uint8)
        return img

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.gray_brightness(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response_gray(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
