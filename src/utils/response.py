from sdks.novavision.src.helper.package import PackageHelper
from components.Package.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, GrayOutputs, \
    GrayResponse, GrayExecutor, ClimateOutputs, ClimateResponse, ClimateExecutor, OutputImageOne, OutputImageTwo


def build_response_climate(context):
    outputImageOne = OutputImageOne(value=context.image_one)
    outputImageTwo = OutputImageTwo(value=context.image_two)
    Outputs = ClimateOutputs(outputImageOne=outputImageOne, outputImageTwo=outputImageTwo)
    climateResponse = ClimateResponse(outputs=Outputs)
    climateExecutor = ClimateExecutor(value=climateResponse)
    executor = ConfigExecutor(value=climateExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel



def build_response_gray(context):
    outputImageOne = OutputImageOne(value=context.image)
    Outputs = GrayOutputs(outputImageOne=outputImageOne)
    grayResponse = GrayResponse(outputs=Outputs)
    grayExecutor = GrayExecutor(value=grayResponse)
    executor = ConfigExecutor(value=grayExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
