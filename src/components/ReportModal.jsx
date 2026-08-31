import React from "react";
import { X, Printer, Download, Sprout, CheckCircle2, ShieldAlert, AlertTriangle } from "lucide-react";

export default function ReportModal({ isOpen, onClose, reportData, user }) {
  if (!isOpen || !reportData) return null;

  const handlePrint = () => {
    window.print();
  };

  const isHealthy = reportData.isHealthy;
  const dateStr = reportData.timestamp
    ? new Date(reportData.timestamp).toLocaleString()
    : new Date().toLocaleString();

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs overflow-y-auto animate-in fade-in">
      <div className="bg-white w-full max-w-2xl rounded-2xl shadow-2xl border border-slate-200 overflow-hidden my-8">
        
        {/* Modal Controls (Hidden in Print) */}
        <div className="flex items-center justify-between p-4 bg-slate-900 text-white print:hidden">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Pathology Report Preview
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold transition"
            >
              <Printer className="w-3.5 h-3.5" /> Print / Save as PDF
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Printable Report Canvas */}
        <div className="p-8 space-y-6 text-slate-900" id="printable-report">
          
          {/* Letterhead */}
          <div className="flex items-center justify-between border-b-2 border-emerald-700 pb-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-emerald-700 text-white flex items-center justify-center">
                <Sprout className="w-7 h-7" />
              </div>
              <div>
                <h1 className="text-xl font-black text-emerald-800 uppercase tracking-tight">
                  PlantVision AI Pathology Report
                </h1>
                <p className="text-xs text-slate-500">
                  Automated Computer Vision Plant Disease Diagnosis & Treatment System
                </p>
              </div>
            </div>
            <div className="text-right text-xs text-slate-500">
              <div><strong className="text-slate-800">Date:</strong> {dateStr}</div>
              <div><strong className="text-slate-800">Account:</strong> {user?.fullName || "Guest Agronomist"}</div>
            </div>
          </div>

          {/* Diagnosis Overview Block */}
          <div className="grid grid-cols-3 gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase">Target Crop</span>
              <div className="font-black text-sm text-slate-800">{reportData.plantName || reportData.plantId}</div>
            </div>
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase">Diagnosed Condition</span>
              <div className={`font-black text-sm ${isHealthy ? "text-emerald-700" : "text-rose-700"}`}>
                {reportData.predictedDisease}
              </div>
            </div>
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase">Model Confidence</span>
              <div className="font-black text-sm text-slate-800">{reportData.confidencePercent}</div>
            </div>
          </div>

          {/* Leaf Snapshot & Pathogen */}
          <div className="flex gap-4 items-start">
            {reportData.imageThumbnail && (
              <img
                src={reportData.imageThumbnail}
                alt="Leaf Snapshot"
                className="w-28 h-28 rounded-xl object-cover border border-slate-300 shadow-xs shrink-0"
              />
            )}
            <div className="space-y-1.5 text-xs text-slate-600">
              <p>
                <strong className="text-slate-800">Pathogen / Cause:</strong>{" "}
                <em>{reportData.pathogen || "N/A"}</em>
              </p>
              <p>
                <strong className="text-slate-800">Severity Assessment:</strong>{" "}
                <span className="font-semibold text-slate-900">{reportData.severity || "Moderate"}</span>
              </p>
              <p className="text-slate-500 italic text-[11px]">
                {reportData.description}
              </p>
            </div>
          </div>

          {/* Symptoms List */}
          {reportData.symptoms && reportData.symptoms.length > 0 && (
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800 mb-2">
                1. Identified Morphological Symptoms
              </h3>
              <ul className="text-xs space-y-1 text-slate-700">
                {reportData.symptoms.map((s, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 mt-1.5 shrink-0"></span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Treatment Protocol */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800">
              2. Recommended Management & Spray Protocol
            </h3>

            {reportData.remedies?.organic && (
              <div className="bg-emerald-50/50 p-3 rounded-lg border border-emerald-100 text-xs">
                <span className="font-bold text-emerald-900 block mb-1">🌿 Organic & Cultural Control:</span>
                {reportData.remedies.organic.map((o, idx) => (
                  <p key={idx} className="text-emerald-950 text-[11px] leading-tight">• {o}</p>
                ))}
              </div>
            )}

            {reportData.remedies?.chemical && (
              <div className="bg-amber-50/50 p-3 rounded-lg border border-amber-100 text-xs">
                <span className="font-bold text-amber-900 block mb-1">🧪 Chemical Fungicide Formulations:</span>
                {reportData.remedies.chemical.map((c, idx) => (
                  <p key={idx} className="text-amber-950 text-[11px] leading-tight">• {c}</p>
                ))}
              </div>
            )}
          </div>

          {/* Footer Note */}
          <div className="pt-4 border-t border-slate-200 text-[10px] text-slate-400 text-center">
            Report generated by PlantVision AI Computer Vision Engine • Verified against Plant Pathology standards.
          </div>

        </div>

      </div>
    </div>
  );
}
