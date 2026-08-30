import { supabase, isSupabaseConfigured } from ./supabaseClient;

const STORAGE_KEY_SCANS = plantvision_scan_history;

export const historyService = {
  async getAllScans(userId) {
    // 1. SUPABASE DATABASE SYNC
    if (isSupabaseConfigured() && supabase && userId && userId !== guest_farmer) {
      try {
        const { data, error } = await supabase
          .from(scans)
          .select(*)
          .order(created_at, { ascending: false });

        if (!error && data) {
          // Normalize Supabase rows
          return data.map(d => ({
            id: d.id,
            userId: d.user_id,
            timestamp: d.created_at,
            plantId: d.plant_id,
            plantName: d.plant_name,
            predictedDisease: d.predicted_disease,
            pathogen: d.pathogen,
            confidence: d.confidence,
            confidencePercent: d.confidence_percent,
            isHealthy: d.is_healthy,
            severity: d.severity,
            imageThumbnail: d.image_thumbnail,
            symptoms: d.symptoms || [],
            remedies: d.remedies || {}
          }));
        }
      } catch (err) {
        console.warn(Supabase fetch failed, using local storage:, err);
      }
    }

    // 2. LOCAL STORAGE FALLBACK
    const raw = localStorage.getItem(STORAGE_KEY_SCANS);
    if (!raw) return [];
    try {
      const all = JSON.parse(raw);
      if (!userId) return all;
      return all.filter(s => s.userId === userId);
    } catch {
      return [];
    }
  },

  async saveScan(userId, scanResult) {
    const record = {
      id: scan_ + Date.now(),
      userId: userId || guest_farmer,
      timestamp: new Date().toISOString(),
      plantId: scanResult.plantId,
      plantName: scanResult.plantId.charAt(0).toUpperCase() + scanResult.plantId.slice(1),
      predictedDisease: scanResult.predictedDisease,
      pathogen: scanResult.pathogen,
      confidence: scanResult.confidence,
      confidencePercent: scanResult.confidencePercent,
      isHealthy: scanResult.isHealthy,
      severity: scanResult.severity,
      imageThumbnail: scanResult.preprocessedImage,
      symptoms: scanResult.symptoms || [],
      remedies: scanResult.remedies || {}
    };

    // Save to Local Storage
    const raw = localStorage.getItem(STORAGE_KEY_SCANS);
    const scans = raw ? JSON.parse(raw) : [];
    scans.unshift(record);
    localStorage.setItem(STORAGE_KEY_SCANS, JSON.stringify(scans));

    // Save to Supabase table if available
    if (isSupabaseConfigured() && supabase && userId && userId !== guest_farmer) {
      try {
        await supabase.from(scans).insert({
          user_id: userId,
          plant_id: record.plantId,
          plant_name: record.plantName,
          predicted_disease: record.predictedDisease,
          pathogen: record.pathogen,
          confidence: record.confidence,
          confidence_percent: record.confidencePercent,
          is_healthy: record.isHealthy,
          severity: record.severity,
          image_thumbnail: record.imageThumbnail,
          symptoms: record.symptoms,
          remedies: record.remedies
        });
      } catch (err) {
        console.warn(Supabase insert error:, err);
      }
    }

    return record;
  },

  async deleteScan(scanId, userId) {
    // Delete from Local Storage
    const raw = localStorage.getItem(STORAGE_KEY_SCANS);
    if (raw) {
      const scans = JSON.parse(raw);
      const updated = scans.filter(s => s.id !== scanId);
      localStorage.setItem(STORAGE_KEY_SCANS, JSON.stringify(updated));
    }

    // Delete from Supabase
    if (isSupabaseConfigured() && supabase) {
      try {
        await supabase.from(scans).delete().eq(id, scanId);
      } catch {}
    }
    return true;
  },

  computeAnalytics(scans = []) {
    const totalScans = scans.length;
    const healthyCount = scans.filter(s => s.isHealthy).length;
    const diseasedCount = totalScans - healthyCount;
    const healthRatio = totalScans > 0 ? ((healthyCount / totalScans) * 100).toFixed(1) : 0;

    const plantCounts = { potato: 0, tomato: 0, apple: 0 };
    scans.forEach(s => {
      const p = (s.plantId || ").toLowerCase();
 if (plantCounts[p] !== undefined) plantCounts[p]++;
 else plantCounts[p] = 1;
 });

 const diseaseCounts = {};
 scans.filter(s => !s.isHealthy).forEach(s => {
 diseaseCounts[s.predictedDisease] = (diseaseCounts[s.predictedDisease] || 0) + 1;
 });

 return {
 totalScans,
 healthyCount,
 diseasedCount,
 healthRatio,
 plantCounts,
 diseaseCounts,
 recentScans: scans.slice(0, 5)
 };
 }
};
