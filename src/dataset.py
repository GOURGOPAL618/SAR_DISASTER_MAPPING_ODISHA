"""
MISSION ENGINE: DATASET PRODUCTION LOOPS & RADAR MATRIX TRANSFORMATIONS
Lead Architect: GOURAGOPAL MOHAPATRA (github.com/GOURGOPAL618)
"""
import os
import json
import numpy as np
import rasterio
from skimage.util import view_as_windows

class SpaceborneDataEngine:
    def __init__(self, config_path="config/sensor_calibration.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.patch_size = 256
        self.epsilon = 1e-5

    def compute_log_ratio(self, pre_path, co_path):
        """Computes localized change vectors to isolate temporal variations."""
        with rasterio.open(pre_path) as src_pre, rasterio.open(co_path) as src_co:
            pre_matrix = src_pre.read(1).astype(np.float32)
            co_matrix = src_co.read(1).astype(np.float32)
            
            # Radiometric log-ratio calculation matrix
            log_ratio = np.log((co_matrix + self.epsilon) / (pre_matrix + self.epsilon))
            return pre_matrix, co_matrix, log_ratio

    def generate_flight_patches(self, pre_path, co_path, output_dir="data/patches"):
        """Generates non-overlapping localized structural arrays for U-Net ingestion."""
        os.makedirs(output_dir, exist_ok=True)
        pre, co, log_r = self.compute_log_ratio(pre_path, co_path)
        
        # Core tensor channel stacking (B x H x W x C)
        stacked_tensor = np.stack([pre, co, log_r], axis=-1)
        h, w, c = stacked_tensor.shape
        
        # Math bound check for tiling limits
        h_tiles = h // self.patch_size
        w_tiles = w // self.patch_size
        
        count = 0
        for i in range(h_tiles):
            for j in range(w_tiles):
                r_start = i * self.patch_size
                c_start = j * self.patch_size
                patch = stacked_tensor[r_start:r_start+self.patch_size, c_start:c_start+self.patch_size, :]
                
                np.save(os.path.join(output_dir, f"patch_tensor_{count}.npy"), patch)
                count += 1
        print(f"[METADATA LOG] Generated {count} validated 256x256 computational matrices.")

if __name__ == "__main__":
    print("Spaceborne Data Engine structured and ready for pipeline loops.")