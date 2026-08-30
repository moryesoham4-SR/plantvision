import React, { useState, useRef } from react;
import { Upload, Camera, Sparkles, RefreshCw, Layers, CheckCircle } from lucide-react;
import { PLANTS } from ../data/diseaseData;

export default function ImageScanner({
  selectedPlantId,
  onImageSelected,
  selectedImage,
  preprocessedMeta,
  isScanning,
  onRunScan
}) {
  const [activeMode, setActiveMode] = useState(samples); // 'samples', 'upload', 'camera'
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);

  // Sample leaf configurations
  const sampleLeaves = {
    potato: [
      { name: Early Blight, file: potato_early_blight.jpg, color: bg-amber-100 border-amber-300 text-amber-900 },
      { name: Late Blight, file: potato_late_blight.jpg, color: bg-red-100 border-red-300 text-red-900 },
      { name: Healthy Leaf, file: potato_healthy.jpg, color: bg-emerald-100 border-emerald-300 text-emerald-900 }
    ],
    tomato: [
      { name: Early Blight, file: tomato_early_blight.jpg, color: bg-amber-100 border-amber-300 text-amber-900 },
      { name: Late Blight, file: tomato_late_blight.jpg, color: bg-red-100 border-red-300 text-red-900 },
      { name: Healthy Leaf, file: tomato_healthy.jpg, color: bg-emerald-100 border-emerald-300 text-emerald-900 }
    ],
    apple: [
      { name: Apple Scab, file: apple_scab.jpg, color: bg-red-100 border-red-300 text-red-900 },
      { name: Black Rot, file: apple_black_rot.jpg, color: bg-purple-100 border-purple-300 text-purple-900 },
      { name: Healthy Leaf, file: apple_healthy.jpg, color: bg-emerald-100 border-emerald-300 text-emerald-900 }
    ]
  };

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      onImageSelected(file, file.name);
    }
  };

  const handleSampleClick = (sample) => {
    // Generate SVG / Canvas Data URL for sample leaf
    const canvas = document.createElement(canvas);
    canvas.width = 300;
    canvas.height = 300;
    const ctx = canvas.getContext(2d);

    // Leaf background
    ctx.fillStyle = #f8fafc;
    ctx.fillRect(0, 0, 300, 300);

    // Draw stylized leaf
    ctx.fillStyle = sample.name.includes(Healthy) ? #16a34a : #4ade80;
    ctx.beginPath();
    ctx.moveTo(150, 30);
    ctx.bezierCurveTo(250, 90, 270, 200, 150, 270);
    ctx.bezierCurveTo(30, 200, 50, 90, 150, 30);
    ctx.fill();

    // Central vein
    ctx.strokeStyle = #14532d;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(150, 30);
    ctx.lineTo(150, 270);
    ctx.stroke();

    // Spots if diseased
    if (sample.name.includes(Early Blight)) {
      ctx.fillStyle = #78350f;
      ctx.beginPath();
      ctx.arc(120, 140, 20, 0, Math.PI * 2);
      ctx.arc(180, 170, 16, 0, Math.PI * 2);
      ctx.fill();
    } else if (sample.name.includes(Late Blight)) {
      ctx.fillStyle = #1e293b;
      ctx.beginPath();
      ctx.ellipse(110, 130, 35, 20, Math.PI / 4, 0, Math.PI * 2);
      ctx.ellipse(170, 180, 30, 25, 0, 0, Math.PI * 2);
      ctx.fill();
    } else if (sample.name.includes(Scab)) {
      ctx.fillStyle = #292524;
      ctx.beginPath();
      ctx.arc(110, 110, 14, 0, Math.PI * 2);
      ctx.arc(160, 140, 18, 0, Math.PI * 2);
      ctx.arc(130, 190, 12, 0, Math.PI * 2);
      ctx.fill();
    }

    const dataUrl = canvas.toDataURL(image/jpeg);
    onImageSelected(dataUrl, sample.file);
  };

  const startCamera = async () => {
    try {
      setCameraActive(true);
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: environment } });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      alert(Camera access denied or not available:  + err.message);
      setCameraActive(false);
    }
  };

  const captureCamera = () => {
    if (videoRef.current) {
      const canvas = document.createElement(canvas);
      canvas.width = 224;
      canvas.height = 224;
      const ctx = canvas.getContext(2d);
      ctx.drawImage(videoRef.current, 0, 0, 224, 224);
      const dataUrl = canvas.toDataURL(image/jpeg);

      // Stop camera stream
      const stream = videoRef.current.srcObject;
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      setCameraActive(false);
      onImageSelected(dataUrl, camera_snap_224x224.jpg);
    }
  };

  const currentPlantSamples = sampleLeaves[selectedPlantId] || sampleLeaves[tomato];

  return (
    <div className=bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4>
      
      {/* Step Header & Modes */}
      <div className=flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3>
        <label className=text-sm font-bold text-slate-800 uppercase tracking-wider>
          2. Input Leaf Image
        </label>
        <div className=flex bg-slate-100 p-1 rounded-lg text-xs font-semibold>
          <button
            onClick={() => { setActiveMode(samples); setCameraActive(false); }}
            className={px-3 py-1 rounded-md transition }
          >
            ⚡ 1-Click Samples
          </button>
          <button
            onClick={() => { setActiveMode(upload); setCameraActive(false); }}
            className={px-3 py-1 rounded-md transition }
          >
            📁 File Upload
          </button>
          <button
            onClick={() => { setActiveMode(camera); startCamera(); }}
            className={px-3 py-1 rounded-md transition }
          >
            📷 Live Camera
          </button>
        </div>
      </div>

      {/* Mode 1: 1-Click Samples */}
      {activeMode === samples && (
        <div className=space-y-2>
          <p className=text-xs text-slate-500>
            Click any test sample below to test the diagnostic pipeline instantly:
          </p>
          <div className=grid grid-cols-3 gap-2>
            {currentPlantSamples.map((sample, idx) => (
              <button
                key={idx}
                onClick={() => handleSampleClick(sample)}
                className={p-3 rounded-xl border text-center transition flex flex-col items-center justify-center gap-1.5 hover:scale-[1.02] }
              >
                <Sparkles className=w-4 h-4 opacity-75 />
                <span className=text-xs font-bold leading-tight>{sample.name}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Mode 2: File Upload Drag & Drop */}
      {activeMode === upload && (
        <div>
          <input
            type=file
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept=image/png, image/jpeg, image/jpg
            className=hidden
          />
          <div
            onClick={() => fileInputRef.current?.click()}
            className=border-2 border-dashed border-slate-300 hover:border-emerald-500 rounded-xl p-6 text-center cursor-pointer bg-slate-50/50 hover:bg-emerald-50/30 transition flex flex-col items-center justify-center gap-2
          >
            <div className=w-10 h-10 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center>
              <Upload className=w-5 h-5 />
            </div>
            <div className=text-xs font-semibold text-slate-700>
              Click to browse or drag & drop leaf image
            </div>
            <div className=text-[10px] text-slate-400>
              Supports JPG, JPEG, PNG (Auto-converts to 224×224×3 RGB)
            </div>
          </div>
        </div>
      )}

      {/* Mode 3: Live Camera View */}
      {activeMode === camera && (
        <div className=space-y-3>
          {cameraActive ? (
            <div className=relative rounded-xl overflow-hidden bg-black aspect-video flex items-center justify-center>
              <video ref={videoRef} autoPlay playsInline className=w-full h-full object-cover />
              <div className=absolute inset-0 border-2 border-emerald-400/60 pointer-events-none rounded-xl m-4 border-dashed flex items-center justify-center>
                <span className=bg-black/60 text-white text-[10px] px-2 py-0.5 rounded>Frame leaf here</span>
              </div>
              <button
                onClick={captureCamera}
                className=absolute bottom-3 px-4 py-1.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-lg transition
              >
                📸 Capture Photo
              </button>
            </div>
          ) : (
            <button
              onClick={startCamera}
              className=w-full py-6 rounded-xl border-2 border-dashed border-slate-300 text-slate-600 text-xs font-semibold flex items-center justify-center gap-2
            >
              <Camera className=w-4 h-4 /> Start Camera
            </button>
          )}
        </div>
      )}

      {/* Preprocessing Preview */}
      {selectedImage && (
        <div className=pt-2 border-t border-slate-100 space-y-3>
          <div className=flex items-center justify-between>
            <span className=text-xs font-bold text-slate-700 flex items-center gap-1.5>
              <Layers className=w-3.5 h-3.5 text-emerald-600 />
              Normalized Model Input Preview
            </span>
            <span className=text-[10px] font-mono bg-slate-100 text-slate-600 px-2 py-0.5 rounded>
              224 × 224 × 3 RGB
            </span>
          </div>

          <div className=flex items-center gap-4 bg-slate-50 p-3 rounded-xl border border-slate-200/80>
            <img
              src={selectedImage}
              alt=Leaf Preview
              className=w-20 h-20 rounded-lg object-cover border border-slate-300 shadow-xs
            />
            <div className=flex-1 text-xs space-y-1 text-slate-600>
              <div><span className=font-semibold text-slate-800>Target Crop:</span> {PLANTS.find(p => p.id === selectedPlantId)?.name}</div>
              <div><span className=font-semibold text-slate-800>Preprocessed:</span> 224px (RGB float32)</div>
              <div className=flex items-center gap-1 text-[11px] text-emerald-700 font-semibold>
                <CheckCircle className=w-3.5 h-3.5 /> Ready for Model Inference
              </div>
            </div>
          </div>

          <button
            disabled={isScanning}
            onClick={onRunScan}
            className=w-full py-3 rounded-xl bg-gradient-to-r from-emerald-700 to-emerald-600 hover:from-emerald-800 hover:to-emerald-700 text-white font-bold text-sm shadow-md shadow-emerald-600/20 transition flex items-center justify-center gap-2 disabled:opacity-50
          >
            {isScanning ? (
              <>
                <RefreshCw className=w-4 h-4 animate-spin />
                Analyzing with {PLANTS.find(p => p.id === selectedPlantId)?.name} Model...
              </>
            ) : (
              <>
                <Sparkles className=w-4 h-4 />
                Run AI Diagnosis
              </>
            )}
          </button>
        </div>
      )}

    </div>
  );
}
