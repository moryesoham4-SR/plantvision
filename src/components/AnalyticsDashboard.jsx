import React from react;
import { BarChart3, Activity, Heart, AlertOctagon, TrendingUp, Sparkles } from lucide-react;

export default function AnalyticsDashboard({ analytics }) {
  const {
    totalScans = 0,
    healthyCount = 0,
    diseasedCount = 0,
    healthRatio = 0,
    plantCounts = {},
    diseaseCounts = {}
  } = analytics || {};

  const totalDiseasedEntries = Object.values(diseaseCounts).reduce((a, b) => a + b, 0);

  return (
    <div className=space-y-6>
      
      {/* Header */}
      <div className=bg-gradient-to-r from-emerald-800 to-emerald-600 rounded-2xl p-6 text-white shadow-md>
        <h2 className=text-2xl font-black tracking-tight>📊 Farm Health Analytics</h2>
        <p className=text-emerald-100 text-xs mt-1>
          Aggregated pathology metrics and distribution patterns across your scanned crops.
        </p>
      </div>

      {/* KPI Cards */}
      <div className=grid grid-cols-2 lg:grid-cols-4 gap-4>
        
        <div className=bg-white p-5 rounded-2xl border border-slate-200 shadow-xs>
          <div className=flex items-center justify-between text-slate-500 mb-2>
            <span className=text-xs font-bold uppercase tracking-wider>Total Scans</span>
            <Activity className=w-4 h-4 text-emerald-600 />
          </div>
          <div className=text-3xl font-black text-slate-900>{totalScans}</div>
          <div className=text-[11px] text-slate-400 mt-1>Lifetime processed leaves</div>
        </div>

        <div className=bg-white p-5 rounded-2xl border border-slate-200 shadow-xs>
          <div className=flex items-center justify-between text-slate-500 mb-2>
            <span className=text-xs font-bold uppercase tracking-wider>Healthy Crop</span>
            <Heart className=w-4 h-4 text-emerald-600 />
          </div>
          <div className=text-3xl font-black text-emerald-600>{healthyCount}</div>
          <div className=text-[11px] text-emerald-700/80 mt-1>Zero pathogen detected</div>
        </div>

        <div className=bg-white p-5 rounded-2xl border border-slate-200 shadow-xs>
          <div className=flex items-center justify-between text-slate-500 mb-2>
            <span className=text-xs font-bold uppercase tracking-wider>Infected / Blight</span>
            <AlertOctagon className=w-4 h-4 text-rose-600 />
          </div>
          <div className=text-3xl font-black text-rose-600>{diseasedCount}</div>
          <div className=text-[11px] text-rose-700/80 mt-1>Needs treatment plan</div>
        </div>

        <div className=bg-white p-5 rounded-2xl border border-slate-200 shadow-xs>
          <div className=flex items-center justify-between text-slate-500 mb-2>
            <span className=text-xs font-bold uppercase tracking-wider>Health Index</span>
            <TrendingUp className=w-4 h-4 text-blue-600 />
          </div>
          <div className=text-3xl font-black text-blue-600>{healthRatio}%</div>
          <div className=text-[11px] text-blue-700/80 mt-1>Overall farm health ratio</div>
        </div>

      </div>

      {totalScans === 0 ? (
        <div className=bg-white rounded-2xl border border-dashed border-slate-300 p-12 text-center text-slate-500>
          <BarChart3 className=w-12 h-12 text-slate-300 mx-auto mb-3 />
          <h3 className=font-bold text-slate-700>No Analytics Data Yet</h3>
          <p className=text-xs text-slate-400 mt-1>
            Perform some scans in the Scanner tab to populate health charts.
          </p>
        </div>
      ) : (
        <div className=grid grid-cols-1 lg:grid-cols-2 gap-6>
          
          {/* Plant Distribution */}
          <div className=bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-4>
            <h3 className=font-bold text-sm text-slate-900 uppercase tracking-wider>
              🌱 Scans by Crop Variety
            </h3>
            <div className=space-y-3>
              {[
                { name: Potato, count: plantCounts[potato] || 0, icon: 🥔, color: bg-amber-500 },
                { name: Tomato, count: plantCounts[tomato] || 0, icon: 🍅, color: bg-red-500 },
                { name: Apple, count: plantCounts[apple] || 0, icon: 🍎, color: bg-emerald-500 }
              ].map((item) => {
                const percent = totalScans > 0 ? Math.round((item.count / totalScans) * 100) : 0;
                return (
                  <div key={item.name} className=space-y-1>
                    <div className=flex items-center justify-between text-xs font-semibold text-slate-700>
                      <span className=flex items-center gap-1.5>{item.icon} {item.name}</span>
                      <span>{item.count} scans ({percent}%)</span>
                    </div>
                    <div className=w-full bg-slate-100 rounded-full h-2 overflow-hidden>
                      <div className={h-2 rounded-full } style={{ width: ${percent}% }}></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Disease Ranking */}
          <div className=bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-4>
            <h3 className=font-bold text-sm text-slate-900 uppercase tracking-wider>
              🦠 Top Detected Pathogens & Diseases
            </h3>
            {Object.keys(diseaseCounts).length === 0 ? (
              <div className=p-8 text-center text-emerald-700 text-xs font-semibold bg-emerald-50 rounded-xl>
                ✨ All your recent crop scans have been diagnosed as Healthy!
              </div>
            ) : (
              <div className=space-y-2.5>
                {Object.entries(diseaseCounts).map(([diseaseName, count]) => {
                  const share = totalDiseasedEntries > 0 ? Math.round((count / totalDiseasedEntries) * 100) : 0;
                  return (
                    <div key={diseaseName} className=flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100 text-xs>
                      <div>
                        <div className=font-bold text-slate-800>{diseaseName}</div>
                        <div className=text-[10px] text-slate-400>{count} occurrences detected</div>
                      </div>
                      <span className=font-mono font-bold text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-200>
                        {share}% of infections
                      </span>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

        </div>
      )}

    </div>
  );
}
