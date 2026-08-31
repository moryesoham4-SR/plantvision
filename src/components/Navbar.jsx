import React from "react";
import { Sprout, History, BarChart3, BookOpen, Settings, LogIn, User, LogOut } from "lucide-react";

export default function Navbar({ activeTab, setActiveTab, user, onOpenAuth, onOpenSettings, onLogout }) {
  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab("scanner")}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-700 to-emerald-500 flex items-center justify-center text-white shadow-md shadow-emerald-500/20">
              <Sprout className="w-6 h-6" />
            </div>
            <div>
              <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-emerald-800 to-emerald-600 bg-clip-text text-transparent">
                PlantVision AI
              </span>
              <span className="hidden sm:inline-block ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                v1.0 Vercel
              </span>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-1">
            <button
              onClick={() => setActiveTab("scanner")}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === "scanner"
                  ? "bg-emerald-50 text-emerald-800 font-semibold shadow-xs"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
              }`}
            >
              <Sprout className="w-4 h-4 text-emerald-600" />
              Scanner
            </button>
            <button
              onClick={() => setActiveTab("history")}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === "history"
                  ? "bg-emerald-50 text-emerald-800 font-semibold shadow-xs"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
              }`}
            >
              <History className="w-4 h-4 text-blue-600" />
              History
            </button>
            <button
              onClick={() => setActiveTab("analytics")}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === "analytics"
                  ? "bg-emerald-50 text-emerald-800 font-semibold shadow-xs"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
              }`}
            >
              <BarChart3 className="w-4 h-4 text-indigo-600" />
              Analytics
            </button>
            <button
              onClick={() => setActiveTab("library")}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === "library"
                  ? "bg-emerald-50 text-emerald-800 font-semibold shadow-xs"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
              }`}
            >
              <BookOpen className="w-4 h-4 text-amber-600" />
              Encyclopedia
            </button>
          </nav>

          {/* User & Settings Actions */}
          <div className="flex items-center gap-2">
            <button
              onClick={onOpenSettings}
              title="Backend & Google Drive Settings"
              className="p-2 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition"
            >
              <Settings className="w-5 h-5" />
            </button>

            {user ? (
              <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-100 text-slate-800 text-xs font-semibold">
                  <User className="w-3.5 h-3.5 text-emerald-600" />
                  <span className="max-w-[100px] truncate">{user.fullName || user.username}</span>
                </div>
                <button
                  onClick={onLogout}
                  title="Sign Out"
                  className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <button
                onClick={onOpenAuth}
                className="flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm transition"
              >
                <LogIn className="w-4 h-4" />
                Sign In
              </button>
            )}
          </div>

        </div>
      </div>

      {/* Mobile Tab Bar */}
      <div className="flex md:hidden border-t border-slate-200 bg-slate-50/80 px-2 py-1 justify-around text-xs">
        <button
          onClick={() => setActiveTab("scanner")}
          className={`flex flex-col items-center py-1.5 px-3 rounded-md ${activeTab === "scanner" ? "text-emerald-700 font-bold" : "text-slate-600"}`}
        >
          <Sprout className="w-4 h-4 mb-0.5" />
          Scanner
        </button>
        <button
          onClick={() => setActiveTab("history")}
          className={`flex flex-col items-center py-1.5 px-3 rounded-md ${activeTab === "history" ? "text-emerald-700 font-bold" : "text-slate-600"}`}
        >
          <History className="w-4 h-4 mb-0.5" />
          History
        </button>
        <button
          onClick={() => setActiveTab("analytics")}
          className={`flex flex-col items-center py-1.5 px-3 rounded-md ${activeTab === "analytics" ? "text-emerald-700 font-bold" : "text-slate-600"}`}
        >
          <BarChart3 className="w-4 h-4 mb-0.5" />
          Analytics
        </button>
        <button
          onClick={() => setActiveTab("library")}
          className={`flex flex-col items-center py-1.5 px-3 rounded-md ${activeTab === "library" ? "text-emerald-700 font-bold" : "text-slate-600"}`}
        >
          <BookOpen className="w-4 h-4 mb-0.5" />
          Library
        </button>
      </div>
    </header>
  );
}
