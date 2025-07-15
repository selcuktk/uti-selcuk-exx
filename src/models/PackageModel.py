
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class HighVolume(Config):
    name: Literal["HighVolume"] = "HighVolume"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title="High Density"

class LowVolume(Config):
    name: Literal["LowVolume"] = "LowVolume"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title="Low Density"

class SpeedLimit(Config):
    name: Literal["SpeedLimit"] = "SpeedLimit"
    value: double = Field(default=100, ge=0, le=500)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title= "SpeedLimit"

class Truck(Config):
    name: Literal["Truck"] = "Truck"
    value: Union[HighVolume,LowVolume]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Truck"

class Car(Config):
    name: Literal["Car"] = "Car"
    speedLimit: SpeedLimit # speedLimit vehicle'ın altına SecondConfigs'in içine gidebilir
    value: Literal["Car"] = "Car"
    type: Literal["object"] = "object"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Car"

class Vehicle(Config):
    name: Literal["Vehicle"] = "Vehicle"
    value: Union[Car, Truck]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Vehicle"

class SecondInputs(Inputs):
    inputImage: InputImage

class SecondConfigs(Configs):
    vehicle: Vehicle

class SecondOutputs(Outputs):
    outputImage: OutputImage

class SecondRequest(Request):
    inputs: Optional[SecondInputs]
    configs: SecondConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class SecondResponse(Response):
    outputs: SecondOutputs

class SecondExecutor(Config):
    name: Literal["Second"] = "Second"
    value: Union[SecondRequest, SecondResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Second Operation"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class HighDensity(Config):
    name: Literal["HighDensity"] = "HighDensity"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title="High Density"

class LowDensity(Config):
    name: Literal["LowDensity"] = "LowDensity"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title="Low Density"

class Temperature(Config):
    name: Literal["Temperature"] = "Temperature"
    value: double = Field(default=20, ge=90*(-1), le=57)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title="Temperature"


class Rainy(Config):
    name: Literal["Rainy"] = "Rainy"
    value: Union[HighDensity,LowDensity]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Rainy"

class Sunny(Config):
    name: Literal["Sunny"] = "Sunny"
    temperature: Temperature # temperature weather'ın altına GrayConfigs'in içine gidebilir
    value: Literal["Sunny"] = "Sunny"
    type: Literal["int"] = "int"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Sunnyy"

class Weather(Config):
    name: Literal["Weather"] = "Weather"
    value: Union[Sunny, Rainy]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Weather"

class GrayInputs(Inputs):
    inputImage: InputImage

class GrayConfigs(Configs):
    weather: Weather

class GrayOutputs(Outputs):
    outputImage: OutputImage

class GrayRequest(Request):
    inputs: Optional[GrayInputs]
    configs: GrayConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class GrayResponse(Response):
    outputs: GrayOutputs

class GrayExecutor(Config):
    name: Literal["Gray"] = "Gray"
    value: Union[GrayRequest, GrayResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Gray"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[GrayExecutor, SecondExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["SelcukExx"] = "SelcukExx"
