"""Import the required packages."""
import numpy as np
import os

from tflite_model_maker.config import ExportFormat, QuantizationConfig
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

from tflite_support import metadata

import tensorflow as tf
assert tf.__version__.startswith('2')

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)



"""
Here is the performance of each EfficientDet-Lite models compared to each others.

| Model architecture | Size(MB)* | Latency(ms)** | Average Precision*** |
|--------------------|-----------|---------------|----------------------|
| EfficientDet-Lite0 | 4.4       | 146           | 25.69%               |
| EfficientDet-Lite1 | 5.8       | 259           | 30.55%               |
| EfficientDet-Lite2 | 7.2       | 396           | 33.97%               |
| EfficientDet-Lite3 | 11.4      | 716           | 37.70%               |
| EfficientDet-Lite4 | 19.9      | 1886          | 41.96%               |

"""

tf_modes_cust = ['efficientdet_lite0', 'efficientdet_lite1', 'efficientdet_lite2', 'efficientdet_lite3', 'efficientdet_lite4']

selected_tf_model_index = 0

my_selected_tflite_model = tf_modes_cust[selected_tf_model_index]
model_file_name = "helmate-tflite"+".tflite"+str(selected_tf_model_index)
my_epoches = 500
my_batch_size = 24


train_data = object_detector.DataLoader.from_pascal_voc(
    'vehicles-images/train',
    'vehicles-images/train',
    ['ambulance','car']
)

val_data = object_detector.DataLoader.from_pascal_voc(
    'vehicles-images/test',
    'vehicles-images/test',
     ['ambulance','car']
)




spec = model_spec.get(my_selected_tflite_model)


model = object_detector.create(train_data, model_spec=spec, batch_size=my_batch_size, train_whole_model=True, epochs=my_epoches, validation_data=val_data)


model.evaluate(val_data)

"""### Step 5: Export as a TensorFlow Lite model.
"""

model.export(export_dir='.', tflite_filename=model_file_name)

"""### Step 6:  Evaluate the TensorFlow Lite model.
"""

model.evaluate_tflite(model_file_name, val_data)

# Download the TFLite model to your local computer.
print("""
from google.colab import files
files.download('traffic_ambu.tflite4')

""")
print(model_file_name)
#@markdown This code comes from the TFLite Object Detection [Raspberry Pi sample](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi).
