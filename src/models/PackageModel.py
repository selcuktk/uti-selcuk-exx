from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, \
    Config


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


class HighDensity(Config):
    name: Literal["HighDensity"] = "HighDensity"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "High Density"


class LowDensity(Config):
    name: Literal["LowDensity"] = "LowDensity"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Low Density"


class Temperature(Config):
    name: Literal["Temperature"] = "Temperature"
    value: float = Field(default=20, ge=80 * (-1), le=57)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Temperature"


class Rainy(Config):
    name: Literal["Rainy"] = "Rainy"
    value: Union[HighDensity, LowDensity]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Rainy"


class Sunny(Config):
    temperature: Temperature
    name: Literal["Sunny"] = "Sunny"
    value: Literal["Sunny"] = "Sunny"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Sunny"


class Weather(Config):
    name: Literal["Weather"] = "Weather"
    value: Union[Sunny, Rainy]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Weather"


class ClimateInputs(Inputs):
    inputImage: InputImage
    inputImage2: InputImage


class ClimateConfigs(Configs):
    weather: Weather


class ClimateOutputs(Outputs):
    outputImage: OutputImage
    outputImage2: OutputImage


class ClimateRequest(Request):
    inputs: Optional[ClimateInputs]
    configs: ClimateConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class ClimateResponse(Response):
    outputs: ClimateOutputs


class ClimateExecutor(Config):
    name: Literal["Climate"] = "Climate"
    value: Union[ClimateRequest, ClimateResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Climate Executor"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class UltraLight(Config):
    name: Literal["UltraLight"] = "UltraLight"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "UltraLight"


class DefaultLight(Config):
    name: Literal["DefaultLight"] = "DefaultLight"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "DefaultLight"


class DarknessValue(Config):
    name: Literal["DarknessValue"] = "DarknessValue"
    value: float = Field(default=5, ge=0, le=10)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Darkness Value"


class Light(Config):
    # lightness: Lightness
    name: Literal["Light"] = "Light"
    value: Union[DefaultLight, UltraLight]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Light"


class Dark(Config):
    darknessValue: DarknessValue
    name: Literal["Dark"] = "Dark"
    value: Literal["Dark"] = "Dark"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Dark"


class Grayness(Config):
    name: Literal["Grayness"] = "Grayness"
    value: Union[Dark, Light]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Grayness"


class GrayInputs(Inputs):
    inputImage: InputImage


class GrayConfigs(Configs):
    grayness: Grayness


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
    value: Union[GrayExecutor, ClimateExecutor]
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
