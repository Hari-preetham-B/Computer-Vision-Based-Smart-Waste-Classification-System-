# Dataset

This folder should contain the training images organized by class.

## Structure
data/train/
├── Dry/        # ~1000 images of dry waste (paper, cardboard, plastic bottles)
├── Wet/        # ~1000 images of wet waste (food scraps, organic material)
└── Metal/      # ~1000 images of metal waste (cans, foil, scrap metal)

## Download

Dataset used: [Garbage Classification — Kaggle](https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification)

1. Download and extract the dataset from Kaggle
2. Sort images into the `Dry/`, `Wet/`, and `Metal/` subfolders above
3. Run `python scripts/train_model.py` to train the model

> Images are not committed to this repo due to file size. The trained model weights (`models/garbage_model.pth`) are included so you can run live detection directly without retraining.
