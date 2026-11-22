import React, { useState } from 'react';
import { 
  Lock, 
  Mail, 
  GraduationCap, 
  ShieldCheck, 
  Eye, 
  EyeOff, 
  Sparkles, 
  ArrowRight, 
  ArrowLeft,
  Loader2, 
  AlertCircle, 
  CheckCircle2,
  Users
} from 'lucide-react';
import { useAuth } from '../context/useAuth.js';
import { MOCK_USERS } from '../data/mockUsers.js';

export default function LoginPage({ onNavigate, onSuccess }) {
  const { login, loginAsDemo } = useAuth();

  const [activeTab, setActiveTab] = useState('student'); // 'student' | 'admin'
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  // Form states
  const [studentForm, setStudentForm] = useState({
    email: 'aditya.nair@college.edu',
    password: 'password123'
  });

  const [adminForm, setAdminForm] = useState({
    email: 'aarav.sharma@college.edu',
    password: 'password123'
  });

  const handleDemoClick = async (mockUser) => {
    try {
      setLoading(true);
      setError(null);
      const res = loginAsDemo(mockUser.id);
      setSuccessMessage(`Signed in as ${mockUser.name} (${mockUser.role === 'admin' ? 'Organizer' : 'Student'})`);
      setTimeout(() => {
        if (onSuccess) {
          onSuccess(res.user);
        } else if (onNavigate) {
          onNavigate(mockUser.role === 'admin' ? 'admin' : 'events');
        }
      }, 500);
    } catch (err) {
      setError(err.message || 'Demo login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleStudentSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!studentForm.email.trim()) {
      setError('Please provide your college email.');
      return;
    }

    try {
      setLoading(true);
      const res = await login(studentForm.email, studentForm.password, 'student');
      setSuccessMessage(`Welcome back, ${res.user.name}!`);
      setTimeout(() => {
        if (onSuccess) {
          onSuccess(res.user);
        } else if (onNavigate) {
          onNavigate('events');
        }
      }, 500);
    } catch (err) {
      setError(err.message || 'Authentication failed. Please verify your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleAdminSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!adminForm.email.trim()) {
      setError('Please provide your organizer / faculty email.');
      return;
    }

    try {
      setLoading(true);
      const res = await login(adminForm.email, adminForm.password, 'admin');
      setSuccessMessage(`Organizer access granted. Welcome, ${res.user.name}!`);
      setTimeout(() => {
        if (onSuccess) {
          onSuccess(res.user);
        } else if (onNavigate) {
          onNavigate('admin');
        }
      }, 500);
    } catch (err) {
      setError(err.message || 'Access verification failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-140px)] flex flex-col justify-center items-center py-10 px-4 sm:px-6 lg:px-8">
      
      {/* Return to events breadcrumb */}
      <div className="w-full max-w-xl mb-4">
        <button
          onClick={() => onNavigate && onNavigate('events')}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-brand-600 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Event Catalog</span>
        </button>
      </div>

      <div className="bg-white/95 backdrop-blur-xl rounded-3xl max-w-xl w-full overflow-hidden shadow-2xl border border-slate-200/90 flex flex-col">
        
        {/* Header with vibrant dark gradient and Poppins ExtraBold hierarchy */}
        <div className="p-6 sm:p-8 bg-gradient-to-r from-navy-900 via-indigo-950 to-navy-900 text-white relative shrink-0 border-b border-indigo-900/30">
          <div className="flex items-center gap-2.5 mb-2">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center shadow-md shadow-brand-500/25 border border-indigo-400/30">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <h2 className="font-heading font-extrabold text-2xl sm:text-3xl text-white tracking-tight">
              Sign In to EventFlow
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-slate-300 font-light tracking-wide max-w-md">
            Enter your campus credentials to access your event passes, registrations, or coordinator tools.
          </p>

          {/* Navigation Tabs */}
          <div className="flex bg-navy-950/70 p-1.5 rounded-2xl border border-white/10 mt-6 gap-1">
            <button
              type="button"
              onClick={() => { setActiveTab('student'); setError(null); }}
              className={`flex-1 py-2.5 px-3 rounded-xl text-xs sm:text-sm font-heading font-semibold transition-all duration-200 flex items-center justify-center gap-2 ${
                activeTab === 'student'
                  ? 'bg-gradient-to-r from-brand-600 to-indigo-600 text-white shadow-md shadow-brand-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <GraduationCap className="w-4 h-4" />
              <span>Student Attendee</span>
            </button>

            <button
              type="button"
              onClick={() => { setActiveTab('admin'); setError(null); }}
              className={`flex-1 py-2.5 px-3 rounded-xl text-xs sm:text-sm font-heading font-semibold transition-all duration-200 flex items-center justify-center gap-2 ${
                activeTab === 'admin'
                  ? 'bg-gradient-to-r from-brand-600 to-indigo-600 text-white shadow-md shadow-brand-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <ShieldCheck className="w-4 h-4" />
              <span>Organizer / Faculty</span>
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6 sm:p-8 space-y-6">
          
          {/* Notification Feedback Alerts */}
          {error && (
            <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2.5 animate-in fade-in duration-200">
              <AlertCircle className="w-4 h-4 shrink-0 text-rose-500" />
              <span className="font-medium">{error}</span>
            </div>
          )}

          {successMessage && (
            <div className="p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs flex items-center gap-2.5 animate-in fade-in duration-200">
              <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-500" />
              <span className="font-semibold">{successMessage}</span>
            </div>
          )}

          {/* TAB 1: Student Login Form */}
          {activeTab === 'student' && (
            <form onSubmit={handleStudentSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-heading font-semibold text-slate-700 mb-1.5">
                  College Email Address
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <input
                    type="email"
                    required
                    value={studentForm.email}
                    onChange={(e) => setStudentForm({ ...studentForm, email: e.target.value })}
                    placeholder="student.id@college.edu"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-slate-800 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all font-sans placeholder:text-slate-400"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="block text-xs font-heading font-semibold text-slate-700">
                    Password
                  </label>
                  <span className="text-[11px] text-slate-400">Default: password123</span>
                </div>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={studentForm.password}
                    onChange={(e) => setStudentForm({ ...studentForm, password: e.target.value })}
                    placeholder="••••••••"
                    className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-slate-300 text-slate-800 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all font-sans"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 rounded-xl font-heading font-semibold text-sm text-white bg-gradient-to-r from-brand-600 via-indigo-600 to-indigo-700 hover:from-brand-500 hover:to-indigo-600 transition-all shadow-md shadow-brand-500/25 flex items-center justify-center gap-2 active:scale-95 disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Verifying Identity...</span>
                  </>
                ) : (
                  <>
                    <span>Sign In to Student Portal</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>
          )}

          {/* TAB 2: Organizer / Admin Form */}
          {activeTab === 'admin' && (
            <form onSubmit={handleAdminSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-heading font-semibold text-slate-700 mb-1.5">
                  Organizer or Faculty Email
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <input
                    type="email"
                    required
                    value={adminForm.email}
                    onChange={(e) => setAdminForm({ ...adminForm, email: e.target.value })}
                    placeholder="aarav.sharma@college.edu"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-slate-800 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all font-sans placeholder:text-slate-400"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="block text-xs font-heading font-semibold text-slate-700">
                    Password / Master Passcode
                  </label>
                  <span className="text-[11px] text-slate-400">Default: password123</span>
                </div>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={adminForm.password}
                    onChange={(e) => setAdminForm({ ...adminForm, password: e.target.value })}
                    placeholder="••••••••"
                    className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-slate-300 text-slate-800 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all font-sans"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 rounded-xl font-heading font-semibold text-sm text-white bg-gradient-to-r from-indigo-700 via-purple-700 to-indigo-800 hover:from-indigo-600 hover:to-purple-600 transition-all shadow-md shadow-indigo-600/25 flex items-center justify-center gap-2 active:scale-95 disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Authorizing Command Console...</span>
                  </>
                ) : (
                  <>
                    <ShieldCheck className="w-4 h-4" />
                    <span>Access Organizer Command OS</span>
                  </>
                )}
              </button>
            </form>
          )}

          {/* Quick 1-Click Demo Profiles */}
          <div className="pt-2 border-t border-slate-200">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-heading font-bold text-slate-600 uppercase tracking-wider flex items-center gap-1.5">
                <Users className="w-3.5 h-3.5 text-brand-500" />
                Quick 1-Click Demo Personas
              </span>
              <span className="text-[11px] text-slate-400">Zero typing required</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {MOCK_USERS.map((u) => (
                <button
                  key={u.id}
                  type="button"
                  onClick={() => handleDemoClick(u)}
                  className="p-2.5 rounded-xl border border-slate-200 hover:border-brand-400 hover:bg-brand-50/40 text-left transition-all flex items-center gap-2.5 group bg-white shadow-sm"
                >
                  <img
                    src={u.avatar}
                    alt={u.name}
                    className="w-8 h-8 rounded-lg object-cover border border-slate-200 shrink-0 group-hover:border-brand-400"
                  />
                  <div className="min-w-0 flex-1">
                    <span className="font-heading font-bold text-xs text-slate-900 block truncate group-hover:text-brand-600">
                      {u.name}
                    </span>
                    <span className="text-[11px] text-slate-500 font-normal block truncate">
                      {u.roleTitle || (u.role === 'admin' ? 'Organizer' : 'Student')}
                    </span>
                  </div>
                  <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider shrink-0 ${
                    u.role === 'admin'
                      ? 'bg-purple-100 text-purple-700'
                      : 'bg-brand-100 text-brand-700'
                  }`}>
                    {u.role === 'admin' ? 'Lead' : 'Student'}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Bottom Switch to Sign Up */}
          <div className="pt-2 border-t border-slate-100 text-center">
            <p className="text-xs text-slate-500">
              New to EventFlow?{' '}
              <button
                type="button"
                onClick={() => onNavigate && onNavigate('signup')}
                className="font-semibold text-brand-600 hover:text-brand-700 underline underline-offset-2 ml-1"
              >
                Create a student or organizer account
              </button>
            </p>
          </div>

        </div>

      </div>
    </div>
  );
}
