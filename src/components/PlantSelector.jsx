import React from react;
import { PLANTS } from ../data/diseaseData;
import { Check, Sparkles, Clock } from lucide-react;

export default function PlantSelector({ selectedPlantId, onSelectPlant }) {
  return (
    <div className=space-y-3>
      <div className=flex items-center justify-between>
        <label className=text-sm font-bold text-slate-800 uppercase tracking-wider>
          1. Select Target Crop
        </label>
        <span className=text-xs text-slate-500 font-medium>
          3 Active • 2 In Training
        </span>
      </div>

      <div className=grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3>
        {PLANTS.map((plant) => {
          const isSelected = selectedPlantId === plant.id;
          const isActive = plant.status === active;

          return (
            <div
              key={plant.id}
              onClick={() => {
                if (isActive) onSelectPlant(plant.id);
              }}
              className={elative p-3.5 rounded-xl border-2 transition text-left select-none }
            >
              {/* Top Badge */}
              <div className=flex items-center justify-between mb-2>
                <span className=text-2xl>{plant.icon}</span>
                {isActive ? (
                  isSelected ? (
                    <span className=w-5 h-5 rounded-full bg-emerald-600 text-white flex items-center justify-center>
                      <Check className=w-3 h-3 stroke-[3] />
                    </span>
                  ) : (
                    <span className=text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800>
                      Active
                    </span>
                  )
                ) : (
                  <span className=text-[10px] font-bold px-1.5 py-0.5 rounded bg-purple-100 text-purple-700 flex items-center gap-1>
                    <Clock className=w-2.5 h-2.5 />
                    {plant.status === training ? 75% : 40%}
                  </span>
                )}
              </div>

              {/* Title & Scientific */}
              <div className=font-bold text-sm text-slate-900 leading-tight>
                {plant.name}
              </div>
              <div className=text-[11px] italic text-slate-500 truncate mt-0.5>
                {plant.scientificName}
              </div>

              {/* Diseases Count */}
              <div className=mt-2 text-[10px] font-medium text-slate-400>
                {plant.diseases.length} condition classes
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
