import pydicom
import cv2
import matplotlib.pyplot as plt
import numpy as np

def process_3d_volume(clean_base_slice):
    """Generates a simulated 3D volumetric matrix stack in memory."""
    h, w = clean_base_slice.shape
    volume_3d = np.zeros((15, h, w), dtype=np.uint8)
    for z in range(15):
        scale_factor = 1.0 - abs(z - 7) * 0.04
        resized = cv2.resize(clean_base_slice, (0,0), fx=scale_factor, fy=scale_factor)
        pad_h = (h - resized.shape) // 2
        pad_w = (w - resized.shape) // 2
        volume_3d[z, pad_h:pad_h+resized.shape, pad_w:pad_w+resized.shape] = resized
    return volume_3d

def run_density_masks(current_slice, hypo_limit, hyper_limit):
    """Classifies tissue types by splitting the matrix into 3 distinct color zones."""
    h, w = current_slice.shape
    hypo_mask = cv2.inRange(current_slice, 0, hypo_limit)
    hyper_mask = cv2.inRange(current_slice, hyper_limit, 255)
    iso_mask = cv2.inRange(current_slice, hypo_limit + 1, hyper_limit - 1)
    
    color_view = cv2.cvtColor(current_slice, cv2.COLOR_GRAY2BGR)
    blue_layer = np.full((h, w, 3), [255, 180, 0], dtype=np.uint8)   
    green_layer = np.full((h, w, 3), [100, 255, 100], dtype=np.uint8) 
    red_layer = np.full((h, w, 3), [0, 0, 255], dtype=np.uint8)     
    
    overlay = color_view.copy()
    overlay = np.where(hypo_mask[..., None] > 0, cv2.addWeighted(color_view, 0.6, blue_layer, 0.4, 0), overlay)
    overlay = np.where(iso_mask[..., None] > 0, cv2.addWeighted(color_view, 0.8, green_layer, 0.2, 0), overlay)
    overlay = np.where(hyper_mask[..., None] > 0, cv2.addWeighted(color_view, 0.4, red_layer, 0.6, 0), overlay)
    return overlay
