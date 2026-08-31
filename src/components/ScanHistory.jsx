import React, { useState } from "react";
import { Search, Filter, Trash2, Calendar, CheckCircle2, AlertTriangle, ShieldAlert, Eye, FileText } from "lucide-react";

export default function ScanHistory({ scans, onDeleteScan, onViewDetails, onOpenReport }) {
  const [plantFilter, setPlantFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

  const filteredScans = scans.filter((scan) => {
    if (plantFilter !== "all" && scan.plantId !== plantFilter) return false;
    if (statusFilter === "healthy" && !scan.isHealthy) return false;
    if (statusFilter === "diseased" && scan.isHealthy) return false;
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      const matchPlant = (scan.plantName || "").toLowerCase().includes(term);
      const matchDisease = (scan.predictedDisease || "").toLowerCase().includes(term);
      if (!matchPlant && !matchDisease) return false;
    }
    return true;
  });

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-800 to-emerald-600 rounded-2xl p-6 text-white shadow-md">
        <h2 className="text-2xl font-black tracking-tight">📜 Personal Scan Records</h2>
        <p className="text-emerald-100 text-xs mt-1">
          Historical log of all leaf image diagnoses stored to your profile.
        </p>
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row items-center justify-between gap-3">
        
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
          <input
            type="text"
            placeholder="Search disease, crop, or pathogen..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-emerald-600"
          />
        </div>

        <div className="flex items-center gap-2 w-full md:w-auto">
          <select
            value={plantFilter}
            onChange={(e) => setPlantFilter(e.target.value)}
            className="text-xs border border-slate-200 rounded-lg py-2 px-3 focus:outline-emerald-600 bg-white font-medium text-slate-700"
          >
            <option value="all">All Plants</option>
            <option value="potato">Potato</option>
            <option value="tomato">Tomato</option>
            <option value="apple">Apple</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="text-xs border border-slate-200 rounded-lg py-2 px-3 focus:outline-emerald-600 bg-white font-medium text-slate-700"
          >
            <option value="all">All Conditions</option>
            <option value="healthy">Healthy Only</option>
            <option value="diseased">Diseased Only</option>
          </select>
        </div>

      </div>

      {/* Scans List / Cards */}
      {filteredScans.length === 0 ? (
        <div className="bg-white rounded-2xl border border-dashed border-slate-300 p-12 text-center text-slate-500">
          <Calendar className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="font-bold text-slate-700">No Scan Records Found</h3>
          <p className="text-xs text-slate-400 mt-1">
            Try adjusting your search filters or scan a new leaf from the Scanner tab.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredScans.map((scan) => {
            const isHealthy = scan.isHealthy;
            const sev = scan.severity;
            const dateStr = new Date(scan.timestamp).toLocaleDateString(undefined, {
              month: "short",
              day: "numeric",
              hour: "2-digit",
              minute: "2-digit"
            });

            return (
              <div
                key={scan.id}
                className="bg-white rounded-2xl border border-slate-200 shadow-xs hover:shadow-md transition overflow-hidden flex flex-col justify-between"
              >
                <div>
                  {/* Card Header & Image */}
                  <div className="flex items-center gap-3 p-4 border-b border-slate-100">
                    <img
                      src={scan.imageThumbnail || "/favicon.svg"}
                      alt={scan.plantName}
                      className="w-14 h-14 rounded-xl object-cover border border-slate-200 bg-slate-50 shrink-0"
                    />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                          {scan.plantName}
                        </span>
                        <span className="text-[10px] text-slate-400">{dateStr}</span>
                      </div>
                      <h4 className="font-bold text-sm text-slate-900 truncate mt-0.5">
                        {scan.predictedDisease}
                      </h4>
                      <div className="flex items-center gap-2 mt-1">
                        <span
                          className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                            isHealthy
                              ? "bg-emerald-100 text-emerald-800 border-emerald-200"
                              : sev === "Moderate"
                              ? "bg-amber-100 text-amber-800 border-amber-200"
                              : "bg-rose-100 text-rose-800 border-rose-200"
                          }`}
                        >
                          {scan.confidencePercent} • {sev}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Symptoms snippet */}
                  {scan.symptoms && scan.symptoms.length > 0 && (
                    <div className="p-4 text-xs text-slate-600 space-y-1">
                      <span className="font-semibold text-slate-700 block text-[11px]">Identified Indicators:</span>
                      <p className="line-clamp-2 text-slate-500">{scan.symptoms.join(" • ")}</p>
                    </div>
                  )}
                </div>

                {/* Card Actions Footer */}
                <div className="flex items-center justify-between p-3 bg-slate-50 border-t border-slate-100 text-xs">
                  <button
                    onClick={() => onOpenReport(scan)}
                    className="flex items-center gap-1 text-slate-700 hover:text-emerald-700 font-semibold transition"
                  >
                    <FileText className="w-3.5 h-3.5" /> PDF Report
                  </button>
                  <button
                    onClick={() => onDeleteScan(scan.id)}
                    className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition"
                    title="Delete record"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

              </div>
            );
          })}
        </div>
      )}

    </div>
  );
}
