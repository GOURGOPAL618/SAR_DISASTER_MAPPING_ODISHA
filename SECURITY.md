
# Security Policy & Vulnerability Management Matrix

## 1. Mission Security Statement
This repository architectures a high-fidelity Earth Observation pipeline processing spaceborne Synthetic Aperture Radar (SAR) imagery via deep learning frameworks. Due to the precision of the classified geospatial output matrices (`odisha_final_flood_map_prediction.tif`) and their strategic value in disaster response and regional analysis, security protocols are enforced across all operational layers.

This policy defines the structural bounds for vulnerability disclosure, vector asset handling, and neural weight integrity verification, managed strictly under the oversight of the Principal Investigator.

---

## 2. Supported Engineering Versions
Only validated production-grade baselines are actively monitored for security vulnerabilities and cryptographic patch deployments.

| Version | Status | Codebase Stream | Active Cryptographic Support |
| :--- | :--- | :--- | :--- |
| **v4.0.x** | ✔️ Active | Core Production Master (Odisha Manual Base) | Full Protocol Coverage |
| **v3.0.x** | ⚠️ Limited | Operational Legacy Architecture | Critical Exploits Only |
| **v2.0.x** | ❌ Deprecated | Early Prototypes & Tiling Tests | None |

---

## 3. Threat Vector Mitigation & Core Vulnerabilities

### A. Neural Weight Serialization Exploits (`.keras` / `.h5`)
* **Risk Parameter:** Standard Keras/TensorFlow model structures can be manipulated via bytecode injection or arbitrary expression execution during un-serialization routines.
* **Mitigation Protocol:** Any model weights, including `flood_unet_model.keras`, must have their SHA-256 cryptographic hashes matched against the official release logs prior to executing `inference.py` on shared-memory edge nodes. Never ingest models from unverified remote repositories.

### B. Geospatial Arbitrary Code Injection (GeoTIFF Parsing)
* **Risk Parameter:** Maliciously malformed target satellite rasters can trigger buffer overflows or pointer migration vulnerabilities within low-level C++ wrappers like `GDAL` or `Rasterio`.
* **Mitigation Protocol:** All source granules ingested by `src/dataset.py` must undergo upfront metadata validation to ensure structural conformity with standard Sentinel-1 Ground Range Detected (GRD) sensor geometries before entering the tensor generator loop.

---

## 4. Reporting a Vulnerability

If you identify a technical flaw, cryptographic exploit, or security vulnerability within this pipeline architecture, do not open a public issue tracking ticket. Follow the restricted reporting loop detailed below:

1. **Secure Contact:** Transmit an encrypted diagnostic report outlining the exploit mechanism directly to the Lead Systems Engineer via:
   * **Project Technical Mail:** `ggmohapatra.info.2007@gmail.com`
   * **Reference Lead:** GOURAGOPAL MOHAPATRA (GitHub: `GOURGOPAL618`)
2. **Telemetry Required:** Provide a minimal configuration setup or proof-of-concept payload, including targeted library dependency versions (matching `requirements.txt`) and specific hardware execution parameters (e.g., shared VRAM overflow metrics).
3. **Response Window:** The Lead Systems Engineer will acknowledge receipt of the encrypted vulnerability vector within **48 hours** and provide a formal engineering fix or isolation patch sequence within **7 business days**.

---

## 5. Security Sign-off & Compliance Tracking
* **Policy Authorization Token:** `S1-RS-DL-SEC-2026`
* **Compliance Grade:** Restricted Technical Specification Baseline
* **System Lead:** GOURAGOPAL MOHAPATRA
