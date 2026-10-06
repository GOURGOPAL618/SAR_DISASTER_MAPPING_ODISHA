<!--
=====================================================================
BADGES: paste your ORIGINAL badge block here, exactly as it is today.
Do not edit it. Everything below is the rewritten body of the README.
=====================================================================
-->

# ◈ SAR-DISASTER-MAPPING-ODISHA ◈

### Spaceborne Synthetic Aperture Radar · Deep Learning Inundation Classification

### Coastal Odisha Flood Mapping Pipeline (Sentinel-1 + U-Net)

---

## ⚡ MISSION OVERVIEW

This repository contains the codebase and geospatial workflow for **Sentinel-1 SAR flood inundation mapping across coastal Odisha**, developed by **Gouragopal Mohapatra** (Mission ID `OM-ODISHA-S1-UNET-02`).

During monsoon and cyclone events, persistent cloud cover blocks optical sensors (Sentinel-2, Landsat). C-band SAR images the surface through cloud, so this pipeline uses **Sentinel-1 backscatter change** with a **U-Net segmentation model** to extract flood extent as a georeferenced raster for use in QGIS.

**Study area:** coastal Odisha, Puri to Balasore (Mahanadi, Brahmani, Baitarani and Salandi delta systems).
**Event(s) used:** `[FILL IN: event name(s), Sentinel-1 acquisition dates (pre-event and post-event), orbit/pass]`

---

## 🛰️ SYSTEM SPECIFICATIONS

| Parameter                  | Specification                                                      |
| -------------------------- | ------------------------------------------------------------------ |
| **Sensor**                 | Sentinel-1 C-band SAR, GRD, VV polarization                        |
| **Model**                  | U-Net semantic segmentation (Keras / TensorFlow)                   |
| **Loss**                   | Dice loss with Laplace smoothing (class-imbalance handling)        |
| **Input tile**             | 256 × 256 × 3 (`[FILL IN: channel definition, e.g. pre, post, log-ratio]`) |
| **Batch memory**           | ≈ 3.14 MB per batch (B = 4, float32)                               |
| **CRS**                    | WGS 84 / EPSG:4326                                                 |
| **GIS platform**           | QGIS                                                               |
| **Compute**                | 16 GB RAM, integrated GPU (shared memory)                          |
| **Output product**         | `odisha_final_flood_map_prediction.tif` (binary flood mask)        |

---

## 🧪 DATA & LABELS

> This section is required for the results below to be interpretable.

| Item                   | Detail                                                            |
| ---------------------- | ----------------------------------------------------------------- |
| **Input preprocessing**| `[FILL IN: orbit file, thermal noise removal, calibration to σ⁰, terrain correction, speckle filter, dB conversion]` |
| **Label (mask) source**| `[FILL IN: manual annotation / Sentinel-2 derived / external product / threshold-derived]` |
| **Train / val / test split** | `[FILL IN: e.g. spatial block split by district; no overlapping tiles across splits]` |
| **Number of tiles**    | `[FILL IN: train / val / test]`                                   |

If masks were derived from a backscatter-change threshold, state that explicitly and report the model against an independent reference, because a model trained on threshold-derived labels learns the threshold.

---

## 🗺️ GEOGRAPHIC FOCUS

| Sector                      | Hydrological driver                       | Observed pattern                                   |
| --------------------------- | ----------------------------------------- | -------------------------------------------------- |
| **Kendrapara (delta core)** | Brahmani & Baitarani convergence overflow | Largest contiguous inundation (`[FILL IN: % area]`) |
| **Jagatsinghpur**           | Mahanadi distributary embankment breaches | Continuous agricultural block submersion           |
| **Puri (NE of Chilika)**    | Daya & Bhargavi discharge backwater       | Expanded lagoon margins                            |
| **Bhadrak**                 | Salandi & Baitarani catchment runoff      | Fragmented inundation pockets                      |
| **Ganjam coastal fringe**   | Storm surge and creek expansion           | Localized, low spatial contiguity                  |

---

## 🔬 BACKSCATTER INTERPRETATION GUIDE

| Surface class              | Typical σ⁰ behaviour (VV)             | Scattering mechanism                                          | Mask value |
| -------------------------- | ------------------------------------- | ------------------------------------------------------------- | ---------- |
| **Permanent water**        | Very low (≲ −22 dB)                   | Specular reflection, almost no return                         | Masked out |
| **Open flood water**       | Strong drop vs. pre-event (≈ −6 dB or more) | Land surface replaced by smooth water                   | 1          |
| **Flooded vegetation / crops** | Variable: drop (open water between stalks) or **increase** (double-bounce) | Water–stem interaction | 1 if detected; see limitations |
| **Dry land**               | Stable, higher (≈ −14 to −8 dB)       | Diffuse rough-surface scattering                              | 0          |
| **Dense mangroves**        | High (≈ −6 to −3 dB)                  | Volume scattering in canopy                                   | 0          |

Values are indicative ranges, not hard class boundaries. The model uses multi-temporal features rather than a single fixed threshold.

---

## 📁 PROJECT STRUCTURE

```
SAR_DISASTER_MAPPING_ODISHA/
├── config/                 # pipeline parameters (JSON)
├── data/
│   └── masks/              # label rasters
├── models/                 # trained model weights / checkpoints
├── notebooks/              # exploration, training, evaluation
├── output/
│   └── metrics/
│       └── QGIS INSIGHT/   # QGIS screenshots and map outputs
├── src/
│   ├── dataset.py          # GeoTIFF ingestion, log-ratio features, tile generator
│   ├── model.py            # U-Net architecture + Dice loss
│   └── inference.py        # sliding-window inference + georeferenced reassembly
├── vector/                 # administrative boundaries and QGIS overlays
├── Makefile
├── requirements.txt
├── Comprehensive_Odisha_Flood_Mapping_Operational_Manual.pdf
└── ODISHA_Flood_Mapping_Blueprint.pdf
```

---

## ⚙️ PIPELINE (`src/`)

- **`dataset.py`**: reads co-registered GeoTIFFs, builds log-ratio features with division-by-zero protection, and streams 256×256×3 tiles.
- **`model.py`**: U-Net encoder–decoder with a smoothed Dice loss to handle the flood/land pixel imbalance (flood ≈ 18.5% of evaluated pixels).
- **`inference.py`**: sliding-window prediction over the full scene, then reassembly into a georeferenced mask with the original metadata.

**Known limitation:** the current window is non-overlapping, which can leave seams at tile borders. Overlapping windows with blended edges are planned (see Roadmap).

---

## 🗺️ QGIS OUTPUT

Predicted pixel indices are mapped to geographic coordinates with the affine geotransform:

```
X_geo = A · X_pixel + B · Y_pixel + C
Y_geo = D · X_pixel + E · Y_pixel + F
```

The output is stored in **WGS 84 / EPSG:4326** and checked for alignment against OpenStreetMap and satellite base layers.

Rendering: `0` = fully transparent; `1` = cyan, opaque. Discrete (binary) rendering only, no color interpolation.

---

## 🚀 QUICK START

```bash
git clone https://github.com/GOURGOPAL618/SAR_DISASTER_MAPPING_ODISHA.git
cd SAR_DISASTER_MAPPING_ODISHA

pip install -r requirements.txt

# Run inference on a target scene
python src/inference.py --config config/odisha_mission.json

# Open in QGIS:
# output/odisha_final_flood_map_prediction.tif
```

---

## 📊 EVALUATION REPORT

> **Evaluation:** June 2026 · sliding-window patch inference · 256×256 tiles · 55,504,795 evaluated pixels
> All metrics below are computed directly from the confusion matrix.

### Confusion matrix (pixel counts)

```
                        Predicted Dry (0)     Predicted Flood (1)
Actual Dry   (0)          42,045,701  TN          3,164,731  FP
Actual Flood (1)           1,647,098  FN          8,647,265  TP
```

### Per-class metrics

| Class     | Precision | Recall | F1 / Dice | IoU    | Support (px) |
| --------- | --------- | ------ | --------- | ------ | ------------ |
| Dry (0)   | 0.9623    | 0.9300 | 0.9459    | 0.8973 | 45,210,432   |
| Flood (1) | 0.7321    | 0.8400 | 0.7824    | 0.6425 | 10,294,363   |

### Summary

| Metric                      | Value  |
| --------------------------- | ------ |
| Overall pixel accuracy      | 0.9133 |
| Mean IoU (mIoU, 2 classes)  | 0.7699 |
| Macro-averaged F1 (mean Dice) | 0.8642 |
| Flood-class IoU             | 0.6425 |
| Flood-class Dice            | 0.7824 |

### Interpretation

- The model recovers **84%** of true flood pixels (recall), which suits an emergency-mapping use case where missed flood is costly.
- Precision for the flood class is **73%**: roughly one in four predicted flood pixels is a false alarm (3.16 M FP vs 8.65 M TP). Remaining false positives are expected over wet or flooded-by-design surfaces such as aquaculture ponds and monsoon paddy fields.
- Flood-class IoU (0.64) is the more conservative figure for operational planning; the 2-class mIoU (0.77) is inflated by the easier dry-land class.

### Comparison with classical thresholding

`[FILL IN: add a table comparing against Otsu and/or a fixed dB-change threshold on the same test tiles, with precision / recall / IoU, and the claimed false-alarm reduction per district (e.g. Kendrapara, Jagatsinghpur).]`

---

## ⚠️ LIMITATIONS

- Metrics are from `[FILL IN: single event / N events]` and the split described in *Data & Labels*; generalization to other events, seasons and sensors is not yet demonstrated.
- Labels may carry their own errors (see *Data & Labels*).
- Flooded vegetation and mangroves can show an **increase** in VV backscatter (double-bounce), which pure drop-based logic misses.
- Monsoon paddy fields and aquaculture ponds are persistent false-positive sources.
- Non-overlapping inference tiles can produce seam artifacts.
- No per-pixel uncertainty output yet.

---

## 🧭 ROADMAP

1. Report results on an independent test event / region and on a public benchmark (e.g. Sen1Floods11).
2. Overlapping sliding-window inference with blended borders.
3. Add VH polarization and a permanent-water / HAND-based exclusion mask.
4. Per-pixel confidence / uncertainty layer.
5. Threshold-baseline comparison table in this README.

---

## 👤 AUTHOR

| Field       | Detail                                                     |
| ----------- | ---------------------------------------------------------- |
| **Name**    | Gouragopal Mohapatra                                       |
| **Role**    | Lead Systems Engineer & Principal Investigator             |
| **GitHub**  | [github.com/GOURGOPAL618](https://github.com/GOURGOPAL618) |
| **Contact** | ggmohapatra.info.2007@gmail.com                            |

---

## © COPYRIGHT & LICENSE

**Copyright © 2026 Gouragopal Mohapatra. All Rights Reserved.**

This codebase, operational manual, trained model weights, geospatial output products and associated documentation are the intellectual property of Gouragopal Mohapatra. Reproduction, redistribution or derivative use, in whole or in part, requires explicit written authorization from the author.

<!--
=====================================================================
BADGES (bottom block): paste your ORIGINAL License / Author / Build
Status / Application badges here, exactly as they are today. Unchanged.
=====================================================================
-->
