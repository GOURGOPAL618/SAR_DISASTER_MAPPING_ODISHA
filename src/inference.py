"""
MISSION ENGINE: SLIDING WINDOW INFERENCE & SPATIAL TRANSFORM MATRIX APPLIER
Lead Architect: GOURAGOPAL MOHAPATRA (github.com/GOURGOPAL618)
"""
import numpy as np
import rasterio
import tensorflow as tf
from src.model import compile_aerospace_unet

class GeospatialInferenceEngine:
    def __init__(self, model_weights_path=None):
        self.model = compile_aerospace_unet()
        if model_weights_path:
            self.model.load_weights(model_weights_path)
        self.patch_size = 256

    def deploy_sliding_window(self, stacked_input_raster, output_raster_path):
        """Processes heavy swaths in sub-arrays avoiding Iris Graphics memory leaks."""
        with rasterio.open(stacked_input_raster) as src:
            meta = src.meta.copy()
            # Enforce binary discrete layer specification bounds
            meta.update(dtype=rasterio.uint8, count=1, nodata=0)
            
            img = src.read() # Expected shape [C, H, W]
            img = np.moveaxis(img, 0, -1) # Convert to [H, W, C]
            h, w, c = img.shape
            
            output_mask = np.zeros((h, w), dtype=np.uint8)
            
            # Non-overlapping matrix execution loops
            for i in range(0, h, self.patch_size):
                for j in range(0, w, self.patch_size):
                    # Edge boundary padding adjustments
                    h_end = min(i + self.patch_size, h)
                    w_end = min(j + self.patch_size, w)
                    
                    patch = img[i:h_end, j:w_end, :]
                    
                    # Pad tensor patch to exactly 256x256 if at border boundaries
                    pad_h = self.patch_size - patch.shape[0]
                    pad_w = self.patch_size - patch.shape[1]
                    padded_patch = np.pad(patch, ((0, pad_h), (0, pad_w), (0, 0)), mode='constant')
                    
                    # Tensor reshape for engine inference activation block
                    tensor_patch = np.expand_dims(padded_patch, axis=0)
                    prob_mask = self.model.predict(tensor_patch, verbose=0)[0, :, :, 0]
                    
                    # Convert probability values to discrete outputs
                    binary_mask = (prob_mask > 0.5).astype(np.uint8)
                    
                    # Splice data array segment back to spatial coordinates matrix
                    output_mask[i:h_end, j:w_end] = binary_mask[0:patch.shape[0], 0:patch.shape[1]]

            # Write discrete classification matrix directly to file
            with rasterio.open(output_raster_path, 'w', **meta) as dst:
                dst.write(output_mask, 1)
        print(f"[METADATA LOG] Spatial transformation locked safely to target destination.")

if __name__ == "__main__":
    print("Geospatial Inference Engine online and synchronized.")