"""
=========================================================
Training Configuration
Project PI Bitcoin LSTM
=========================================================
"""

# Dataset
DATASET_NAME = "BTC-USD Yahoo Finance"

FEATURES = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]

# Window
WINDOW_SIZE = 60

# Training
EPOCHS = 50
BATCH_SIZE = 32

# Model
LSTM_LAYER_1 = 64
LSTM_LAYER_2 = 32
DROPOUT = 0.2

# Compile
OPTIMIZER = "adam"
LOSS_FUNCTION = "mse"

# Dashboard
ALGORITHM = "LSTM"