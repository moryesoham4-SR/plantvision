import { simulateInference } from "../data/mockInference";

export const detectionService = {
  /**
   * Preprocesses image via HTML5 Canvas to exact 224x224x3 RGB format
   */
  async preprocessImage(imageSource) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = () => {
        const canvas = document.createElement("canvas");
        canvas.width = 224;
        canvas.height = 224;
        const ctx = canvas.getContext("2d");
        
        // Draw & resize to 224x224
        ctx.drawImage(img, 0, 0, 224, 224);
        
        // Get RGBA pixel data
        const imageData = ctx.getImageData(0, 0, 224, 224);
        const data = imageData.data;
        
        // Calculate RGB channel averages for quality validation
        let rSum = 0, gSum = 0, bSum = 0;
        const totalPixels = 224 * 224;
        for (let i = 0; i < data.length; i += 4) {
          rSum += data[i];
          gSum += data[i + 1];
          bSum += data[i + 2];
        }

        const dataUrl224 = canvas.toDataURL("image/jpeg", 0.92);

        resolve({
          originalWidth: img.width,
          originalHeight: img.height,
          processedWidth: 224,
          processedHeight: 224,
          channels: 3,
          dataUrl: dataUrl224,
          avgR: Math.round(rSum / totalPixels),
          avgG: Math.round(gSum / totalPixels),
          avgB: Math.round(bSum / totalPixels)
        });
      };
      img.onerror = () => reject(new Error("Failed to load leaf image for preprocessing."));
      
      if (typeof imageSource === "string") {
        img.src = imageSource;
      } else if (imageSource instanceof File || imageSource instanceof Blob) {
        const reader = new FileReader();
        reader.onload = (e) => { img.src = e.target.result; };
        reader.onerror = () => reject(new Error("File reading error."));
        reader.readAsDataURL(imageSource);
      } else {
        reject(new Error("Invalid image source type."));
      }
    });
  },

  /**
   * Runs plant disease diagnosis (Mock or Remote Backend API)
   */
  async detectDisease(plantId, imageFileOrUrl, filenameHint = "") {
    const configData = JSON.parse(localStorage.getItem("plantvision_api_config") || "{}");
    const useMock = configData.useMock !== undefined ? configData.useMock : true;
    const apiUrl = configData.apiUrl || "";

    // 1. Client-side Preprocessing to 224x224x3 RGB
    const preprocessed = await this.preprocessImage(imageFileOrUrl);

    if (useMock || !apiUrl) {
      // Simulate realistic model inference latency (800ms - 1200ms)
      await new Promise(r => setTimeout(r, 900));
      const result = simulateInference(plantId, filenameHint);
      return {
        ...result,
        preprocessedImage: preprocessed.dataUrl,
        preprocessedMeta: preprocessed
      };
    }

    // 2. Real Remote Backend Inference (Google Drive / Colab / FastAPI)
    const formData = new FormData();
    formData.append("plant", plantId);
    if (imageFileOrUrl instanceof File) {
      formData.append("image", imageFileOrUrl);
    } else {
      // Convert dataURL to Blob
      const blob = await (await fetch(preprocessed.dataUrl)).blob();
      formData.append("image", blob, "leaf_224x224.jpg");
    }

    const res = await fetch(`${apiUrl}/predict`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      throw new Error(`Inference server responded with error ${res.status}`);
    }

    const data = await res.json();
    return {
      ...data,
      preprocessedImage: preprocessed.dataUrl,
      preprocessedMeta: preprocessed
    };
  }
};
