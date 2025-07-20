"""
    It is one of the preprocessing components in which the image is rotated.
"""

import os
import cv2
import sys
import numpy as np

from src.utils.response import build_response_climate

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.SelcukExx.src.utils.response import build_response_climate
from components.SelcukExx.src.models.PackageModel import PackageModel


class Climate(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.temperature = None
        self.density = None
        self.image_one = self.request.get_param("inputImageOne")
        self.image_two = self.request.get_param("inputImageTwo")
        load_param()

    def load_param(self):
        if self.request.get_param("Weather") == "Sunny":
            self.temperature = self.request.get_param("Temperature")
        else:
            self.density = self.request.get_param("Rainy")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def gray(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    def run(self):
        imgOne = Image.get_frame(img=self.image_one, redis_db=self.redis_db)
        imgTwo = Image.get_frame(img=self.image_two, redis_db=self.redis_db)
        if self.request.get_param("Weather") == "Sunny":
            imgOne.value = self.gray(imgOne.value)
            if self.temperature >= 20:
                imgTwo.value = self.gray(imgTwo.value)
        else:
            if not self.density:
                imgTwo.value = self.gray(imgTwo.value)
        self.image_one = Image.set_frame(img=imgOne, package_uID=self.uID, redis_db=self.redis_db)
        self.image_two = Image.set_frame(img=imgTwo, package_uID=self.uID, redis_db=self.redis_db)

        packageModel = build_response_climate(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
