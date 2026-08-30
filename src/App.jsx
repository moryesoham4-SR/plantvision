import React, { useState, useEffect } from react;
import Navbar from ./components/Navbar;
import PlantSelector from ./components/PlantSelector;
import ImageScanner from ./components/ImageScanner;
import DiagnosisResult from ./components/DiagnosisResult;
import ScanHistory from ./components/ScanHistory;
import AnalyticsDashboard from ./components/AnalyticsDashboard;
import DiseaseLibrary from ./components/DiseaseLibrary;
import AuthModal from ./components/AuthModal;
import ReportModal from ./components/ReportModal;
import SettingsModal from ./components/SettingsModal;

import { authService } from ./services/authService;
import { detectionService } from ./services/detectionService;
import { historyService } from ./services/historyService;

export default function App() {
  const [activeTab, setActiveTab] = useState(scanner);
  const [currentUser, setCurrentUser] = useState(null);

  // Modals state
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isReportOpen, setIsReportOpen] = useState(false);
  const [activeReportData, setActiveReportData] = useState(null);

  // Scanner state
  const [selectedPlantId, setSelectedPlantId] = useState(tomato);
  const [selectedImage, setSelectedImage] = useState(null);
  const [imageHint, setImageHint] = useState(");
 const [preprocessedMeta, setPreprocessedMeta] = useState(null);
 const [isScanning, setIsScanning] = useState(false);
 const [diagnosisResult, setDiagnosisResult] = useState(null);

 // Scan History & Analytics state
 const [scans, setScans] = useState([]);
 const [analytics, setAnalytics] = useState({});

 useEffect(() => {
 // Load initial user session
 const user = authService.getCurrentUser();
 setCurrentUser(user);
 refreshHistory(user?.id);
 }, []);

 const refreshHistory = async (userId) => {
 const list = await historyService.getAllScans(userId);
 setScans(list);
 setAnalytics(historyService.computeAnalytics(list));
 };

 const handleImageSelected = async (imageSource, filename) => {
 try {
 const meta = await detectionService.preprocessImage(imageSource);
 setSelectedImage(meta.dataUrl);
 setImageHint(filename);
 setPreprocessedMeta(meta);
 setDiagnosisResult(null); // Clear previous result
 } catch (err) {
 alert(Error preprocessing image:  + err.message);
 }
 };

 const handleRunScan = async () => {
 if (!selectedImage) return;
 setIsScanning(true);

 try {
 const result = await detectionService.detectDisease(
 selectedPlantId,
 selectedImage,
 imageHint
 );

 setDiagnosisResult(result);

 // Auto save to user history
 await historyService.saveScan(currentUser?.id || guest_farmer, result);
 await refreshHistory(currentUser?.id);
 } catch (err) {
 alert(Diagnosis failed:  + err.message);
 } finally {
 setIsScanning(false);
 }
 };

 const handleDeleteScan = async (scanId) => {
 await historyService.deleteScan(scanId, currentUser?.id);
 await refreshHistory(currentUser?.id);
 };

 const handleOpenReport = (record) => {
 setActiveReportData(record || diagnosisResult);
 setIsReportOpen(true);
 };

 const handleLogout = async () => {
 await authService.logout();
 setCurrentUser(null);
 await refreshHistory(null);
 };

 return (
 <div className=min-h-screen bg-slate-50 flex flex-col font-sans>
 
 {/* Navigation Bar */}
 <Navbar
 activeTab={activeTab}
 setActiveTab={setActiveTab}
 user={currentUser}
 onOpenAuth={() => setIsAuthOpen(true)}
 onOpenSettings={() => setIsSettingsOpen(true)}
 onLogout={handleLogout}
 />

 {/* Main Content Area */}
 <main className=flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6>
 
 {/* Tab 1: SCANNER */}
 {activeTab === scanner && (
 <div className=space-y-6>
 
 {/* Plant Selector Carousel */}
 <PlantSelector
 selectedPlantId={selectedPlantId}
 onSelectPlant={(plantId) => {
 setSelectedPlantId(plantId);
 setDiagnosisResult(null);
 }}
 />

 {/* Split Scanner Grid */}
 <div className=grid grid-cols-1 lg:grid-cols-2 gap-6 items-start>
 
 {/* Left Column: Image Ingestion & Preprocessor */}
 <ImageScanner
 selectedPlantId={selectedPlantId}
 onImageSelected={handleImageSelected}
 selectedImage={selectedImage}
 preprocessedMeta={preprocessedMeta}
 isScanning={isScanning}
 onRunScan={handleRunScan}
 />

 {/* Right Column: AI Diagnosis Output */}
 <div>
 {diagnosisResult ? (
 <DiagnosisResult
 result={diagnosisResult}
 onOpenReport={() => handleOpenReport(diagnosisResult)}
 onScanAgain={() => {
 setSelectedImage(null);
 setDiagnosisResult(null);
 }}
 />
 ) : (
 <div className=bg-white rounded-2xl border border-dashed border-slate-300 p-12 text-center text-slate-400 space-y-3>
 <div className=w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-400>
 🔬
 </div>
 <h3 className=font-bold text-slate-700 text-sm>Diagnosis Results will appear here</h3>
 <p className=text-xs text-slate-400 max-w-xs mx-auto>
 Select your target crop, upload a leaf or click a 1-click sample leaf, and press Run AI Diagnosis.
 </p>
 </div>
 )}
 </div>

 </div>

 </div>
 )}

 {/* Tab 2: HISTORY */}
 {activeTab === history && (
 <ScanHistory
 scans={scans}
 onDeleteScan={handleDeleteScan}
 onOpenReport={handleOpenReport}
 />
 )}

 {/* Tab 3: ANALYTICS */}
 {activeTab === analytics && (
 <AnalyticsDashboard analytics={analytics} />
 )}

 {/* Tab 4: ENCYCLOPEDIA */}
 {activeTab === library && (
 <DiseaseLibrary />
 )}

 </main>

 {/* Modals */}
 <AuthModal
 isOpen={isAuthOpen}
 onClose={() => setIsAuthOpen(false)}
 onAuthSuccess={async (user) => {
 setCurrentUser(user);
 await refreshHistory(user.id);
 }}
 />

 <ReportModal
 isOpen={isReportOpen}
 onClose={() => setIsReportOpen(false)}
 reportData={activeReportData}
 user={currentUser}
 />

 <SettingsModal
 isOpen={isSettingsOpen}
 onClose={() => setIsSettingsOpen(false)}
 />

 {/* Footer */}
 <footer className=bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500 mt-12 print:hidden>
 <p className=font-medium text-slate-700>🌿 PlantVision AI — Computer Vision Plant Pathology System</p>
 <p className=mt-1 text-slate-400>Vercel & Supabase Ready • Preprocessed for 224×224×3 RGB Models</p>
 </footer>

 </div>
 );
}
