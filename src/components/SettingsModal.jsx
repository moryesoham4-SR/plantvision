import React, { useState, useEffect } from react;
import { X, HardDrive, Check, Server, Sliders, Cpu } from lucide-react;

export default function SettingsModal({ isOpen, onClose }) {
  const [useMock, setUseMock] = useState(true);
  const [apiUrl, setApiUrl] = useState(http://localhost:8000);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const raw = localStorage.getItem(plantvision_api_config);
    if (raw) {
      try {
        const conf = JSON.parse(raw);
        setUseMock(conf.useMock !== undefined ? conf.useMock : true);
        setApiUrl(conf.apiUrl || http://localhost:8000);
      } catch {}
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSave = () => {
    localStorage.setItem(
      plantvision_api_config,
      JSON.stringify({ useMock, apiUrl: apiUrl.trim() })
    );
    setSaved(true);
    setTimeout(() => {
      setSaved(false);
      onClose();
    }, 800);
  };

  return (
    <div className=fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in>
      <div className=bg-white w-full max-w-lg rounded-2xl shadow-2xl border border-slate-200 overflow-hidden>
        
        {/* Header */}
        <div className=bg-slate-900 p-5 text-white flex items-center justify-between>
          <div className=flex items-center gap-2.5>
            <Sliders className=w-5 h-5 text-emerald-400 />
            <h3 className=font-bold text-base>Backend & Inference Settings</h3>
          </div>
          <button
            onClick={onClose}
            className=p-1 rounded-lg bg-white/10 hover:bg-white/20 text-white transition
          >
            <X className=w-4 h-4 />
          </button>
        </div>

        {/* Body */}
        <div className=p-6 space-y-5 text-slate-800>
          
          {/* Mode Switcher */}
          <div className=p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-3>
            <div className=flex items-center justify-between>
              <div>
                <span className=text-xs font-bold uppercase tracking-wider text-slate-700 block>
                  Inference Engine Mode
                </span>
                <span className=text-xs text-slate-500>
                  {useMock ? Running simulated high-accuracy mock engine : Connecting to live Python model server}
                </span>
              </div>
              <label className=relative inline-flex items-center cursor-pointer>
                <input
                  type=checkbox
                  checked={useMock}
                  onChange={(e) => setUseMock(e.target.checked)}
                  className=sr-only peer
                />
                <div className=w-11 h-6 bg-slate-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600></div>
              </label>
            </div>
          </div>

          {/* Real Backend API URL */}
          {!useMock && (
            <div className=space-y-2 animate-in fade-in>
              <label className=block text-xs font-bold text-slate-700 uppercase tracking-wider>
                Python FastAPI / Colab Endpoint URL
              </label>
              <div className=relative>
                <Server className=w-4 h-4 absolute left-3 top-3 text-slate-400 />
                <input
                  type=url
                  value={apiUrl}
                  onChange={(e) => setApiUrl(e.target.value)}
                  placeholder=https://your-ngrok-or-cloud-url.app
                  className=w-full pl-9 pr-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-emerald-600 font-mono
                />
              </div>
              <p className=text-[11px] text-slate-400>
                Your backend should accept <code>multipart/form-data</code> with <code>plant</code> and <code>image</code>.
              </p>
            </div>
          )}

          {/* Architecture Spec */}
          <div className=p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-2 text-xs text-slate-600>
            <span className=font-bold text-slate-800 flex items-center gap-1.5>
              <Cpu className=w-4 h-4 text-emerald-600 /> Model Pipeline Specifications
            </span>
            <ul className=space-y-1 text-[11px] text-slate-500>
              <li>• Input Tensor Format: <code>224 × 224 × 3 RGB (Normalized [0, 1])</code></li>
              <li>• Models: <code>Potato Model</code>, <code>Tomato Model</code>, <code>Apple Model</code></li>
              <li>• Storage Backend: Google Drive / Cloud Weight Store</li>
            </ul>
          </div>

          <button
            onClick={handleSave}
            className=w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md transition flex items-center justify-center gap-1.5
          >
            {saved ? <Check className=w-4 h-4 /> : null}
            {saved ? Settings Saved! : Save & Apply Settings}
          </button>

        </div>

      </div>
    </div>
  );
}
