import React, { useState } from react;
import { DISEASE_DATABASE } from ../data/diseaseData;
import { BookOpen, Search, Check, AlertCircle, ShieldCheck } from lucide-react;

export default function DiseaseLibrary() {
  const [selectedCrop, setSelectedCrop] = useState(potato);
  const [search, setSearch] = useState(");

 const cropDiseases = DISEASE_DATABASE[selectedCrop] || {};

 const filteredDiseases = Object.entries(cropDiseases).filter(([name, info]) => {
 if (!search) return true;
 const term = search.toLowerCase();
 return (
 name.toLowerCase().includes(term) ||
 (info.pathogen || ).toLowerCase().includes(term) ||
 info.description.toLowerCase().includes(term)
 );
 });

 return (
 <div className=space-y-6>
 
 {/* Header */}
 <div className=bg-gradient-to-r from-emerald-800 to-emerald-600 rounded-2xl p-6 text-white shadow-md>
 <h2 className=text-2xl font-black tracking-tight>📚 Plant Disease Encyclopedia</h2>
 <p className=text-emerald-100 text-xs mt-1>
 Field guide & pathology directory for Potato, Tomato, and Apple crops.
 </p>
 </div>

 {/* Selector & Search */}
 <div className=flex flex-col sm:flex-row items-center justify-between gap-3 bg-white p-4 rounded-xl border border-slate-200 shadow-xs>
 
 <div className=flex bg-slate-100 p-1 rounded-xl w-full sm:w-auto text-xs font-bold>
 <button
 onClick={() => setSelectedCrop(potato)}
 className={lex-1 sm:flex-initial px-4 py-2 rounded-lg transition }
 >
 🥔 Potato
 </button>
 <button
 onClick={() => setSelectedCrop(tomato)}
 className={lex-1 sm:flex-initial px-4 py-2 rounded-lg transition }
 >
 🍅 Tomato
 </button>
 <button
 onClick={() => setSelectedCrop(apple)}
 className={lex-1 sm:flex-initial px-4 py-2 rounded-lg transition }
 >
 🍎 Apple
 </button>
 </div>

 <div className=relative w-full sm:w-64>
 <Search className=w-4 h-4 absolute left-3 top-2.5 text-slate-400 />
 <input
 type=text
 placeholder=Search symptoms or disease...
 value={search}
 onChange={(e) => setSearch(e.target.value)}
 className=w-full pl-9 pr-3 py-1.5 text-xs border border-slate-200 rounded-lg focus:outline-emerald-600
 />
 </div>

 </div>

 {/* Disease Cards */}
 <div className=space-y-4>
 {filteredDiseases.map(([diseaseName, info]) => {
 const isHealthy = info.isHealthy;
 return (
 <div
 key={diseaseName}
 className=bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden p-6 space-y-4
 >
 <div className=flex items-start justify-between>
 <div>
 <div className=flex items-center gap-2>
 <span
 className={ ext-[10px] font-bold px-2 py-0.5 rounded-full border }
 >
 {info.severity} Severity
 </span>
 <span className=text-xs text-slate-500 italic>
 {info.pathogen}
 </span>
 </div>
 <h3 className=text-xl font-bold text-slate-900 mt-1>
 {diseaseName}
 </h3>
 </div>
 </div>

 <p className=text-xs text-slate-600 leading-relaxed>
 {info.description}
 </p>

 {info.causes && (
 <div className=text-xs bg-slate-50 p-2.5 rounded-lg border border-slate-100 text-slate-600>
 <strong className=text-slate-800>Primary Causes:</strong> {info.causes}
 </div>
 )}

 {/* Symptoms */}
 <div>
 <h4 className=text-xs font-bold text-slate-800 uppercase tracking-wider mb-2>
 📌 Key Symptoms
 </h4>
 <div className=grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs>
 {info.symptoms.map((s, idx) => (
 <div key={idx} className=flex items-start gap-2 bg-slate-50 p-2 rounded-lg text-slate-700>
 <span className=w-1.5 h-1.5 rounded-full bg-emerald-600 mt-1.5 shrink-0></span>
 <span>{s}</span>
 </div>
 ))}
 </div>
 </div>

 {/* Treatment Sections */}
 <div className=grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 border-t border-slate-100 text-xs>
 <div className=bg-emerald-50/60 p-3 rounded-xl border border-emerald-100 space-y-1.5>
 <span className=font-bold text-emerald-900 block>🌿 Organic Control</span>
 {info.remedies.organic.map((o, idx) => (
 <p key={idx} className=text-emerald-950 text-[11px] leading-tight>• {o}</p>
 ))}
 </div>

 <div className=bg-amber-50/60 p-3 rounded-xl border border-amber-100 space-y-1.5>
 <span className=font-bold text-amber-900 block>🧪 Chemical Sprays</span>
 {info.remedies.chemical.map((c, idx) => (
 <p key={idx} className=text-amber-950 text-[11px] leading-tight>• {c}</p>
 ))}
 </div>

 <div className=bg-blue-50/60 p-3 rounded-xl border border-blue-100 space-y-1.5>
 <span className=font-bold text-blue-900 block>🛡️ Prevention</span>
 {info.remedies.prevention.map((p, idx) => (
 <p key={idx} className=text-blue-950 text-[11px] leading-tight>• {p}</p>
 ))}
 </div>
 </div>

 </div>
 );
 })}
 </div>

 </div>
 );
}
