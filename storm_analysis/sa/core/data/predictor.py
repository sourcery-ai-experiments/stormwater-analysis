import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from tensorflow.keras.models import load_model  # noqa

current_directory = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_directory, "catchemnt_classifier", "model.keras")

try:
    classifier = load_model(model_path)
except FileNotFoundError:
    print(f"Cannot load model: {model_path}")
    raise Exception("Cannot load model")
