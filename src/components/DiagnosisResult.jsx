import React, { useState } from react;
import { AlertTriangle, CheckCircle2, ShieldAlert, Sparkles, FileText, Share2, Check, RefreshCw } from lucide-react;

export default function DiagnosisResult({ result, onOpenReport, onScanAgain }) {
  const [activeTab, setActiveTab] = useState(organic);

  if (!result) return null;

  const isHealthy = result.isHealthy;
  const severity = result.severity;

  // Severity theme styling
  const severityConfig = {
    None: {
      bg: bg-emerald-50 border-emerald-300 text-emerald-900,
      badge: bg-emerald-100 text-emerald-800 border-emerald-300,
      icon: CheckCircle2,
      label: Healthy Foliage
    },
    Moderate: {
      bg: bg-amber-50 border-amber-300 text-amber-900,
      badge: bg-amber-100 text-amber-800 border-amber-300,
      icon: AlertTriangle,
      label: Moderate Risk
    },
    Severe: {
      bg: bg-rose-50 border-rose-300 text-rose-900,
      badge: bg-rose-100 text-rose-800 border-rose-300,
      icon: ShieldAlert,
      label: High / Critical Risk
    }
  };

  const theme = severityConfig[severity] || severityConfig[Moderate];
  const StatusIcon = theme.icon;

  return (
    <div className=bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden space-y-4 animate-in fade-in slide-in-from-bottom-2>
      
      {/* Result Banner */}
      <div className={p-5 border-b }>
        <div className=flex items-start justify-between gap-3>
          <div>
            <div className=flex items-center gap-2 mb-1>
              <span className={	ext-xs font-bold px-2.5 py-0.5 rounded-full border  flex items-center gap-1}>
                <StatusIcon className=w-3 h-3 />
                {theme.label}
              </span>
              <span className=text-xs text-slate-500 font-mono>
                {result.inferenceTimeMs || 45}ms
              </span>
            </div>
            <h2 className=text-2xl font-black text-slate-900 tracking-tight>
              {result.predictedDisease}
            </h2>
            <p className=text-xs text-slate-600 mt-0.5>
              Pathogen: <em className=font-semibold>{result.pathogen || N/A}</em>
            </p>
          </div>

          <div className=text-right>
            <div className=text-2xl font-black text-slate-900>
              {result.confidencePercent}
            </div>
            <div className=text-[10px] font-bold text-slate-500 uppercase tracking-wider>
              Confidence Score
            </div>
          </div>
        </div>

        {/* Confidence Progress Bar */}
        <div className=w-full bg-slate-200/80 rounded-full h-2 mt-3 overflow-hidden>
          <div
            className={h-2 rounded-full transition-all duration-700 }
            style={{ width: ${result.confidence * 100}% }}
          ></div>
        </div>
      </div>

      {/* Main Body */}
      <div className=p-5 pt-0 space-y-4>
        
        {/* Description & Symptoms */}
        <div className=text-xs text-slate-600 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100>
          <p className=font-medium text-slate-800 mb-1>{result.description}</p>
          {result.causes && (
            <p className=text-slate-500><strong className=text-slate-700>Primary Causes:</strong> {result.causes}</p>
          )}
        </div>

        {/* Key Symptoms */}
        {result.symptoms && result.symptoms.length > 0 && (
          <div>
            <h4 className=text-xs font-bold text-slate-800 uppercase tracking-wider mb-2>
              📌 Detected Visual Symptoms
            </h4>
            <div className=grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs>
              {result.symptoms.map((s, idx) => (
                <div key={idx} className=flex items-start gap-2 bg-slate-50 p-2.5 rounded-lg border border-slate-100>
                  <span className=w-1.5 h-1.5 rounded-full bg-emerald-600 mt-1.5 shrink-0></span>
                  <span className=text-slate-700 font-medium>{s}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Multi-Class Probabilities */}
        {result.probabilities && (
          <div className=pt-2 border-t border-slate-100>
            <h4 className=text-xs font-bold text-slate-800 uppercase tracking-wider mb-2>
              📊 Class Probability Spread
            </h4>
            <div className=space-y-1.5 text-xs>
              {Object.entries(result.probabilities).map(([cls, prob]) => (
                <div key={cls} className=flex items-center gap-3>
                  <span className=w-32 truncate text-slate-600 font-medium>{cls}</span>
                  <div className=flex-1 bg-slate-100 rounded-full h-1.5 overflow-hidden>
                    <div
                      className=bg-emerald-600 h-1.5 rounded-full
                      style={{ width: ${prob * 100}% }}
                    ></div>
                  </div>
                  <span className=w-12 text-right font-mono text-[11px] text-slate-500 font-bold>
                    {(prob * 100).toFixed(1)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Treatment Tabs */}
        <div className=pt-2 border-t border-slate-100>
          <h4 className=text-xs font-bold text-slate-800 uppercase tracking-wider mb-2>
            💡 Treatment & Management Prescription
          </h4>

          <div className=flex border-b border-slate-200 text-xs font-semibold mb-3>
            <button
              onClick={() => setActiveTab(organic)}
              className={py-2 px-3 transition border-b-2 }
            >
              🌿 Organic Solutions
            </button>
            <button
              onClick={() => setActiveTab(chemical)}
              className={py-2 px-3 transition border-b-2 }
            >
              🧪 Chemical Sprays
            </button>
            <button
              onClick={() => setActiveTab(prevention)}
              className={py-2 px-3 transition border-b-2 }
            >
              🛡️ Preventative Care
            </button>
          </div>

          <div className=space-y-2 text-xs text-slate-700>
            {activeTab === organic && (
              <div className=space-y-1.5>
                {result.remedies?.organic?.map((item, idx) => (
                  <div key={idx} className=flex items-start gap-2 bg-emerald-50/50 p-2.5 rounded-lg border border-emerald-100>
                    <Check className=w-4 h-4 text-emerald-600 shrink-0 mt-0.5 />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === chemical && (
              <div className=space-y-1.5>
                {result.remedies?.chemical?.map((item, idx) => (
                  <div key={idx} className=flex items-start gap-2 bg-amber-50/50 p-2.5 rounded-lg border border-amber-100>
                    <Check className=w-4 h-4 text-amber-600 shrink-0 mt-0.5 />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === prevention && (
              <div className=space-y-1.5>
                {result.remedies?.prevention?.map((item, idx) => (
                  <div key={idx} className=flex items-start gap-2 bg-blue-50/50 p-2.5 rounded-lg border border-blue-100>
                    <Check className=w-4 h-4 text-blue-600 shrink-0 mt-0.5 />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className=flex items-center gap-3 pt-3 border-t border-slate-100>
          <button
            onClick={onOpenReport}
            className=flex-1 py-2.5 px-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold shadow-md transition flex items-center justify-center gap-2
          >
            <FileText className=w-4 h-4 />
            Download Diagnostic Report
          </button>
          <button
            onClick={onScanAgain}
            className=py-2.5 px-4 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold transition flex items-center gap-1.5
          >
            <RefreshCw className=w-3.5 h-3.5 />
            New Scan
          </button>
        </div>

      </div>
    </div>
  );
}
