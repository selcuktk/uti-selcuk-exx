
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

class SecondInputs(Inputs):
    inputImage: InputImage

class SecondConfigs(Configs):
    pass

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

class NumberOfSomething(Config):
    name: Literal["NumberOfSomething"] = "NumberOfSomething"
    value: int = Field(default=7, ge=0, le=100)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeholder: Literal["[0, 100]"] = "[0, 100]"

class MeaninglessProbability(Config):
    name: Literal["MeaninglessProbability"] = "MeaninglessProbability"
    value: double = Field(default=0.5, ge=0, le=1)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeholder: Literal["[0, 1]"] = "[0, 1]"
    class Config:
        title = "Meaningless Probability Factor"


class DdListFalse(Config):
    name: Literal["DdListFalse"] = "DdListFalse"
    meaninglessProbability: MeaninglessProbability
    numberOfSomething: NumberOfSomething
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"

class DdListTrue(Config):
    name: Literal["DdListTrue"] = "DdListTrue"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"

class DdList(Config):
    """
        Rotate image without catting off sides.
    """
    name: Literal["DdList"] = "DdList"
    value: Union[DdListTrue, DdListFalse]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Dependent Dropdownlist"

class Degree(Config):
    """
        Positive angles specify counterclockwise rotation while negative angles indicate clockwise rotation.
    """
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359.0, le=359.0,default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "AAAngle"

class GrayInputs(Inputs):
    inputImage: InputImage

class GrayConfigs(Configs):
    degree: Degree
    ddList: DdList

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
