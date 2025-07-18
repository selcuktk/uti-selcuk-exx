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
from components.SelcukExx.src.utils.response import build_response
from components.SelcukExx.src.models.PackageModel import PackageModel


class Gray(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        load_param()

    def load_param(self):
        if self.request.get_param("Grayness") == "Dark":
            self.darkness_value = self.request.get_param("DarknessValue")
        else:
            if self.request.get_param("Rainy") == "LowDensity":
                self.density = False
            else:
                self.density = True



    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def gray(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.request.get_param("Grayness") == "Dark":
            darknessValue = self.request.get_param("DarknessValue")
            darknessFactor = 1 - (darknessValue * 0.08)
            img = np.clip(img*darknessFactor, 0, 255).astype(np.uint8)
        elif self.request.get_param("Light") == "DefaultLight":
            img = np.clip(img*1.5, 0, 255).astype(np.uint8)
        else:
            img = np.clip(img*2, 0, 255).astype(np.uint8)
        return img

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.gray(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()