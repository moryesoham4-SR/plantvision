import React, { useState } from react;
import { X, Lock, Mail, User, CheckCircle2, AlertCircle } from lucide-react;
import { authService } from ../services/authService;

export default function AuthModal({ isOpen, onClose, onAuthSuccess }) {
  const [mode, setMode] = useState(login); // 'login' or 'register'
  const [fullName, setFullName] = useState(");
 const [username, setUsername] = useState();
 const [email, setEmail] = useState();
 const [password, setPassword] = useState();
 const [error, setError] = useState();

 if (!isOpen) return null;

 const handleSubmit = (e) => {
 e.preventDefault();
 setError();

 if (mode === login) {
 if (!username || !password) {
 setError(Please enter both username and password.);
 return;
 }
 const res = authService.login(username, password);
 if (res.success) {
 onAuthSuccess(res.user);
 onClose();
 } else {
 setError(res.message);
 }
 } else {
 if (!fullName || !username || !email || !password) {
 setError(All fields are required for registration.);
 return;
 }
 const res = authService.register(fullName, username, email, password);
 if (res.success) {
 onAuthSuccess(res.user);
 onClose();
 } else {
 setError(res.message);
 }
 }
 };

 const handleGuestLogin = () => {
 const res = authService.guestLogin();
 onAuthSuccess(res.user);
 onClose();
 };

 return (
 <div className=fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in>
 <div className=bg-white w-full max-w-md rounded-2xl shadow-2xl border border-slate-100 overflow-hidden>
 
 {/* Header */}
 <div className=bg-gradient-to-r from-emerald-800 to-emerald-600 p-6 text-white relative>
 <button
 onClick={onClose}
 className=absolute top-4 right-4 p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition
 >
 <X className=w-5 h-5 />
 </button>
 <h3 className=text-xl font-bold>
 {mode === login ? Welcome Back to PlantVision : Create PlantVision Account}
 </h3>
 <p className=text-emerald-100 text-xs mt-1>
 {mode === login
 ? Sign in to access your personal scans and farm history.
 : Register to start recording plant disease scans & analytics.}
 </p>
 </div>

 {/* Tab Switcher */}
 <div className=flex border-b border-slate-100 bg-slate-50 text-sm font-semibold>
 <button
 onClick={() => { setMode(login); setError(); }}
 className={lex-1 py-3 text-center transition }
 >
 Sign In
 </button>
 <button
 onClick={() => { setMode(register); setError(); }}
 className={lex-1 py-3 text-center transition }
 >
 New Registration
 </button>
 </div>

 {/* Form Body */}
 <form onSubmit={handleSubmit} className=p-6 space-y-4>
 {error && (
 <div className=flex items-center gap-2 p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-xs>
 <AlertCircle className=w-4 h-4 shrink-0 />
 <span>{error}</span>
 </div>
 )}

 {mode === register && (
 <div>
 <label className=block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1>Full Name</label>
 <div className=relative>
 <User className=w-4 h-4 absolute left-3 top-3 text-slate-400 />
 <input
 type=text
 placeholder=e.g. Dr. Jane Smith
 value={fullName}
 onChange={(e) => setFullName(e.target.value)}
 className=w-full pl-9 pr-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-emerald-600
 />
 </div>
 </div>
 )}

 <div>
 <label className=block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1>Username</label>
 <div className=relative>
 <User className=w-4 h-4 absolute left-3 top-3 text-slate-400 />
 <input
 type=text
 placeholder=e.g. farmer_john
 value={username}
 onChange={(e) => setUsername(e.target.value)}
 className=w-full pl-9 pr-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-emerald-600
 />
 </div>
 </div>

 {mode === register && (
 <div>
 <label className=block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1>Email Address</label>
 <div className=relative>
 <Mail className=w-4 h-4 absolute left-3 top-3 text-slate-400 />
 <input
 type=email
 placeholder=john@example.com
 value={email}
 onChange={(e) => setEmail(e.target.value)}
 className=w-full pl-9 pr-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-emerald-600
 />
 </div>
 </div>
 )}

 <div>
 <label className=block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1>Password</label>
 <div className=relative>
 <Lock className=w-4 h-4 absolute left-3 top-3 text-slate-400 />
 <input
 type=password
 placeholder=••••••••
 value={password}
 onChange={(e) => setPassword(e.target.value)}
 className=w-full pl-9 pr-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-emerald-600
 />
 </div>
 </div>

 <button
 type=submit
 className=w-full py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm shadow-md transition
 >
 {mode === login ? Sign In to PlantVision : Create My Account}
 </button>

 <div className=relative flex py-2 items-center>
 <div className=flex-grow border-t border-slate-200></div>
 <span className=flex-shrink mx-3 text-slate-400 text-xs>or instant test</span>
 <div className=flex-grow border-t border-slate-200></div>
 </div>

 <button
 type=button
 onClick={handleGuestLogin}
 className=w-full py-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition
 >
 Continue as Guest Tester
 </button>
 </form>

 </div>
 </div>
 );
}
