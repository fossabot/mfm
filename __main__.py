import argparse
import json

from PIL import Image
from numpy import array

from src import MFM, Model, ModelInput, View
from src.fitter import FittersChain
from data import get_datafile_path

parser = argparse.ArgumentParser(
    description='Morphable Face Model fitting application')
parser.add_argument(
    '--config', metavar='config', type=str, required=True,
    help='specify configuration file for fitting procedure')

args = parser.parse_args()

fitting_settings = None
with open(args.config) as config:
    fitting_settings = json.load(config)

MFM.init()
view = View((500, 500))
model = Model(view)
model_input = ModelInput(model)

model_filename = get_datafile_path('test.png')
image = Image.open(model_filename).convert('L')
original_data = array((image.getdata())).astype('f') / 255
image_data = original_data.reshape(image.size)[::-1, :].flatten()
image.close()

fitters = [{
    'fitter': 'BruteForce',
    'dimensions': 0,
    'steps': [1, 10, 10, 5],
    'levels': list(range(4)),
    'offsets': [0, -0.5, -0.5, 0],
    'scales': [0, -2, -2, 1]
}, {
    'fitter': 'BruteForce',
    'dimensions': 4,
    'steps': [8, 8, 8, 8],
    'levels': list(range(0, 4)),
    'offsets': [-0.5, -0.5, -0.5, -0.5],
    'scales': [8, 8, 8, 8]
}, {
    'fitter': 'BGD',
    'dimensions': 50,
    'max_loops': 100,
    'dx': 1.,
    'step': 50.
}]

chain = FittersChain(fitters, image_data, model)

model.start(chain)
