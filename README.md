# 🛕 Odisha Cyclone & Flood Segmentation Model (SAR U-Net)

A professional end-to-end Deep Learning pipeline designed to extract, preprocess, and segment flood-affected regions along the highly vulnerable coastal stretch of Odisha, India (covering **Puri, Jagatsinghpur, Kendrapara, Bhadrak, and Balasore** districts). 

The project leverages **Sentinel-1 Synthetic Aperture Radar (SAR) Ground Range Detected (GRD)** dual-polarization imagery to capture surface changes during high-impact extreme weather events like Cyclone Fani (2019), bypassing cloud cover limitations.

---


<div align="center">

![Project Status - In Progress](https://img.shields.io/badge/status-in--progress-orange?style=for-the-badge&logo=github)
![Python Version](https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Google Earth Engine](https://img.shields.io/badge/Google%20Earth%20Engine-4285F4?style=for-the-badge&logo=google-earth-engine&logoColor=white)

![License - MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Framework - Keras](https://img.shields.io/badge/framework-Keras-D00000?style=flat-square&logo=keras&logoColor=white)
![Domain - Remote Sensing](https://img.shields.io/badge/domain-Remote%20Sensing-9cf?style=flat-square)
![Location - Odisha Coast](https://img.shields.io/badge/focus-Odisha%20Coast%20🇮🇳-blue?style=flat-square)

</div>

---

## 🗺️ Project Scope & Geographic ROI
The model targets the core Northern & Central Cyclone Zones of Odisha:
* **Bounding Box:** `Long 85.0°E to 87.2°E` | `Lat 19.5°N to 21.8°N`
* **Sensor Resolution:** Optimized 40-meter spatial resolution.
* **Temporal Windows:** April 2019 (Pre-event Baseline) vs. May 2019 (Post-Cyclone Fani Landfall).

---

## 🛠️ Repository Architecture (Target Structure)
The repository is structured to follow production-ready software engineering standards:

```text
├── data/
│   ├── raw/           # Master raw multi-band GeoTIFF file from GEE (346 MB)
│   ├── processed/     # 256x256 image & mask patches for ML training
│   └── vector/        # Predicted flood footprints converted to Shapefiles (.shp)
├── models/            # Saved model weights (.h5 / .keras) and architectures
├── notebooks/         # Step-by-step Jupyter/Kaggle Notebooks
│   ├── 01_data_extraction.ipynb      # GEE API Data Download Pipeline
│   ├── 02_data_preprocessing.ipynb   # Patch Generation (256x256)
│   ├── 03_model_training.ipynb       # U-Net Architecture & Training
│   └── 04_inference_vectorization.ipynb # Flood Mapping & Raster-to-Vector
├── src/               # Production-ready production scripts (.py)
└── README.md          # Project documentation
