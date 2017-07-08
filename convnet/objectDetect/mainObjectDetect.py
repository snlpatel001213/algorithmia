"this is the main file, change input file appropriately and run this script"

import objectDetectUtils

# keras gives too many deprecation warnings, ignoring all warnings
import warnings
warnings._setoption('ignore')

# making instance of objectDetectUtils class
objectDetectInstance = objectDetectUtils.objectDetectutils()

# getting compiled model
model = objectDetectInstance.getModelDefination()

# providing image to model for to predict on
imagePath = "images/halftrack.jpg"
image = objectDetectInstance.preprocessImage(imagePath)
# collecting responses
response = model.predict_proba(image)

# top five class according to prediction probability
topFive = objectDetectInstance.getClassName(response[0])

# witting to image
objectDetectInstance.writeToImage(imagePath,topFive)