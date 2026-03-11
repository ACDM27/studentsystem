"""
Image Preprocessing Service
Enhances image quality before OCR recognition to improve accuracy
"""

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from pathlib import Path
from typing import Tuple, Optional


class ImagePreprocessor:
    """Preprocess images to improve OCR accuracy"""
    
    def __init__(self):
        self.default_target_size = (2048, 2048)  # Higher resolution for better OCR
        
    def preprocess_for_ocr(
        self,
        image_path: str,
        output_path: Optional[str] = None,
        enhance_contrast: bool = True,
        sharpen: bool = True,
        denoise: bool = True,
        upscale: bool = True
    ) -> str:
        """
        Preprocess image for better OCR recognition
        
        Args:
            image_path: Path to input image
            output_path: Path to save processed image (optional, defaults to temp file)
            enhance_contrast: Whether to enhance contrast
            sharpen: Whether to sharpen the image
            denoise: Whether to apply denoising
            upscale: Whether to upscale low-resolution images
            
        Returns:
            Path to processed image
        """
        # Open image
        img = Image.open(image_path)

        # Step 1: Apply EXIF orientation (fixes phone photos stored sideways)
        img = self._fix_exif_orientation(img)

        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Step 2: Fine skew correction (±15°)
        img = self._deskew(img)

        # Upscale if image is too small
        if upscale:
            img = self._upscale_if_needed(img)
        
        # Denoise
        if denoise:
            img = self._denoise(img)
        
        # Enhance contrast
        if enhance_contrast:
            img = self._enhance_contrast(img)
        
        # Sharpen
        if sharpen:
            img = self._sharpen(img)
        
        # Save processed image
        if output_path is None:
            input_path = Path(image_path)
            output_path = str(input_path.parent / f"{input_path.stem}_processed{input_path.suffix}")
        
        img.save(output_path, quality=95)
        return output_path
    
    def _fix_exif_orientation(self, img: Image.Image) -> Image.Image:
        """Apply EXIF orientation tag so phone photos are upright before any processing"""
        try:
            from PIL import ImageOps
            return ImageOps.exif_transpose(img)
        except Exception:
            return img

    def _deskew(self, img: Image.Image, max_angle: float = 15.0) -> Image.Image:
        """
        Fine skew correction (±15°) using projection profile method.
        Uses adaptive threshold and confidence check to avoid rotating
        already-correct images (especially portrait certificate scans).
        """
        detect_size = (512, 512)
        small = img.copy()
        small.thumbnail(detect_size, Image.Resampling.LANCZOS)

        gray = np.array(small.convert('L'))

        # Adaptive threshold: pixels darker than (mean - 0.5 * std) are treated as text
        # Much more reliable than fixed 128 for colourful certificate backgrounds
        threshold = float(np.mean(gray) - 0.5 * np.std(gray))
        binary = (gray < threshold).astype(np.float32)

        # If too little or too much content, skip (colourful/blank images → unreliable)
        text_ratio = binary.mean()
        if text_ratio < 0.005 or text_ratio > 0.6:
            return img

        def _score(angle: float) -> float:
            rotated = Image.fromarray((binary * 255).astype(np.uint8)).rotate(
                angle, resample=Image.Resampling.BILINEAR, expand=False, fillcolor=0
            )
            proj = np.array(rotated, dtype=np.float32).sum(axis=1)
            return float(proj.var())

        # Baseline: score at 0° (no rotation)
        baseline = _score(0.0)

        best_angle = 0.0
        best_score = baseline

        for angle in np.arange(-max_angle, max_angle + 0.5, 0.5):
            if angle == 0.0:
                continue
            s = _score(angle)
            if s > best_score:
                best_score = s
                best_angle = angle

        # Only rotate if:
        #   1. The skew is perceptible (> 0.5°)
        #   2. The improvement over baseline is meaningful (> 20%)
        #      — avoids rotating an already-correct portrait certificate
        improvement = (best_score - baseline) / (baseline + 1e-9)
        if abs(best_angle) > 0.5 and improvement > 0.20:
            img = img.rotate(
                best_angle,
                resample=Image.Resampling.BILINEAR,
                expand=True,
                fillcolor=(255, 255, 255)
            )
        return img

    def _upscale_if_needed(self, img: Image.Image) -> Image.Image:
        """Upscale image if it's too small"""
        width, height = img.size
        
        # If image is smaller than 1024px on any side, upscale
        if width < 1024 or height < 1024:
            # Calculate scale factor
            scale = max(1024 / width, 1024 / height)
            new_size = (int(width * scale), int(height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
        return img
    
    def _denoise(self, img: Image.Image) -> Image.Image:
        """Apply gentle denoising"""
        # Use median filter for noise reduction
        img = img.filter(ImageFilter.MedianFilter(size=3))
        return img
    
    def _enhance_contrast(self, img: Image.Image, factor: float = 1.3) -> Image.Image:
        """Enhance image contrast"""
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(factor)
        return img
    
    def _sharpen(self, img: Image.Image, factor: float = 1.5) -> Image.Image:
        """Sharpen image for better text clarity"""
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(factor)
        return img
    
    def get_image_quality_score(self, image_path: str) -> dict:
        """
        Assess image quality for OCR
        
        Returns:
            Dictionary with quality metrics
        """
        img = Image.open(image_path)
        width, height = img.size
        
        # Calculate quality score
        resolution_score = min(1.0, (width * height) / (1024 * 1024))
        
        # Convert to numpy for more analysis
        img_array = np.array(img)
        
        # Calculate sharpness (variance of Laplacian)
        from scipy import ndimage
        laplacian = ndimage.laplace(img_array.mean(axis=2))
        sharpness = laplacian.var()
        sharpness_score = min(1.0, sharpness / 1000)
        
        overall_score = (resolution_score * 0.6 + sharpness_score * 0.4)
        
        return {
            "resolution": f"{width}x{height}",
            "resolution_score": round(resolution_score, 2),
            "sharpness_score": round(sharpness_score, 2),
            "overall_score": round(overall_score, 2),
            "recommendation": "good" if overall_score > 0.7 else "needs_enhancement"
        }


# Create singleton instance
image_preprocessor = ImagePreprocessor()
