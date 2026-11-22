import React, { useState } from 'react';
import { 
  Lock, 
  Mail, 
  User, 
  GraduationCap, 
  ShieldCheck, 
  Building, 
  Phone, 
  IdCard, 
  Eye, 
  EyeOff, 
  Sparkles, 
  ArrowRight, 
  ArrowLeft,
  Loader2, 
  AlertCircle, 
  CheckCircle2 
} from 'lucide-react';
import { useAuth } from '../context/useAuth.js';

const DEPARTMENTS = [
  'Computer Science & Engineering',
  'Information Technology',
  'Electronics & Communication (ECE)',
  'Electrical & Electronics (EEE)',
  'Mechanical Engineering',
  'Mechatronics & Robotics',
  'Civil & Structural Engineering',
  'Biotechnology / Biomedical',
  'Management & Business Studies',
  'Media, Arts & Humanities'
];

const YEARS = ['1st Year', '2nd Year', '3rd Year', '4th Year', 'Postgraduate / PhD', 'Faculty / Staff'];

export default function SignupPage({ onNavigate, onSuccess }) {
  const { signup } = useAuth();

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const [form, setForm] = useState({
    name: '',
    email: '',
    department: 'Computer Science & Engineering',
    year: '1st Year',
    roll: '',
    phone: '',
    password: '',
    confirmPassword: '',
    accountType: 'student' // 'student' | 'admin'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!form.name.trim() || !form.email.trim()) {
      setError('Full name and college email are required.');
      return;
    }

    if (!form.password) {
      setError('Please provide a secure password.');
      return;
    }

    if (form.password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match. Please verify and retry.');
      return;
    }

    try {
      setLoading(true);
      const res = await signup({
        name: form.name,
        email: form.email,
        role: form.accountType,
        department: form.department,
        year: form.year,
        roll: form.roll || `STU${Math.floor(1000 + Math.random() * 9000)}`,
        phone: form.phone || '+91 98765 00000',
        password: form.password
      });

      setSuccessMessage(`Account created successfully! Welcome to EventFlow, ${res.user.name}.`);
      setTimeout(() => {
        if (onSuccess) {
          onSuccess(res.user);
        } else if (onNavigate) {
          onNavigate(res.user.role === 'admin' ? 'admin' : 'events');
        }
      }, 600);
    } catch (err) {
      setError(err.message || 'Registration failed. Please check form values.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-140px)] flex flex-col justify-center items-center py-10 px-4 sm:px-6 lg:px-8">
      
      {/* Return to events breadcrumb */}
      <div className="w-full max-w-2xl mb-4">
        <button
          onClick={() => onNavigate && onNavigate('events')}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-brand-600 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Event Catalog</span>
        </button>
      </div>

      <div className="bg-white/95 backdrop-blur-xl rounded-3xl max-w-2xl w-full overflow-hidden shadow-2xl border border-slate-200/90 flex flex-col">
        
        {/* Header with vibrant dark gradient and Poppins ExtraBold hierarchy */}
        <div className="p-6 sm:p-8 bg-gradient-to-r from-navy-900 via-indigo-950 to-navy-900 text-white relative shrink-0 border-b border-indigo-900/30">
          <div className="flex items-center gap-2.5 mb-2">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center shadow-md shadow-brand-500/25 border border-indigo-400/30">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <h2 className="font-heading font-extrabold text-2xl sm:text-3xl text-white tracking-tight">
              Create Campus Account
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-slate-300 font-light tracking-wide max-w-lg">
            Join EventFlow to register for hackathons and workshops, track live rounds, and claim verifiable QR passes.
          </p>

          {/* Account Type Selector */}
          <div className="flex bg-navy-950/70 p-1.5 rounded-2xl border border-white/10 mt-6 gap-1.5">
            <button
              type="button"
              onClick={() => setForm({ ...form, accountType: 'student' })}
              className={`flex-1 py-2.5 px-3 rounded-xl text-xs sm:text-sm font-heading font-semibold transition-all duration-200 flex items-center justify-center gap-2 ${
                form.accountType === 'student'
                  ? 'bg-gradient-to-r from-brand-600 to-indigo-600 text-white shadow-md shadow-brand-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <GraduationCap className="w-4 h-4" />
              <span>Student Account</span>
            </button>

            <button
              type="button"
              onClick={() => setForm({ ...form, accountType: 'admin' })}
              className={`flex-1 py-2.5 px-3 rounded-xl text-xs sm:text-sm font-heading font-semibold transition-all duration-200 flex items-center justify-center gap-2 ${
                form.accountType === 'admin'
                  ? 'bg-gradient-to-r from-brand-600 to-indigo-600 text-white shadow-md shadow-brand-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <ShieldCheck className="w-4 h-4" />
              <span>Club Organizer / Lead</span>
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

          <form onSubmit={handleSubmit} className="space-y-4">
            
            {/* Row 1: Name and Email */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-heading font-semibold text-slate-700 mb-1.5">
                  Full Name *
                </label>
                <div className="relative">
                  <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <input
                    type="text"
                    required
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    placeholder="e.g. Priya Sharma"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-slate-800 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all font-sans placeholder:text-slate-400"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-heading font-semibold text-slate-700 mb-1.5">
                  College Email *
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <input
                    type="email"
                    required
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    placeholder="priya.sharma@college.edu"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-slate-800 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all font-sans placeholder:text-slate-400"
                  />
                </div>
              </div>
            </div>

            {/* Row 2: Department and Year */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-heading font-semibold text-slate-700 mb-1.5">
                  Department / Branch
                </label>
                <div className="relative">
                  <Building className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <select
                    value={form.department}
                    onChange={(e) => setForm({ ...form, department: e.target.value })}
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-slate-800 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all font-sans bg-white"
                  >
                    {DEPARTMENTS.map((dept) => (
                      <option key={dept} value={dept}>{dept}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-heading font-semibold text-slate-700 mb-1.5">
                  Year of Study / Designation
                </label>
                <div className="relative">
                  <GraduationCap className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <select
                    value={form.year}
                    onChange={(e) => setForm({ ...form, year: e.target.value })}
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-slate-800 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all font-sans bg-white"
                  >
                    {YEARS.map((yr) => (
                      <option key={yr} value={yr}>{yr}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Row 3: Roll Number and Phone */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-heading font-semibold text-slate-700 mb-1.5">
                  {form.accountType === 'admin' ? 'Faculty / Staff ID' : 'Student Roll Number'}
                </label>
                <div className="relative">
                  <IdCard className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <input
                    type="text"
                    value={form.roll}
                    onChange={(e) => setForm({ ...form, roll: e.target.value })}
                    placeholder={form.accountType === 'admin' ? 'FAC-CSE-09' : 'CS24B1055'}
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-slate-800 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all font-sans placeholder:text-slate-400"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-heading font-semibold text-slate-700 mb-1.5">
                  Contact Phone
                </label>
                <div className="relative">
                  <Phone className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <input
                    type="tel"
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    placeholder="+91 98765 43210"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-slate-800 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all font-sans placeholder:text-slate-400"
                  />
                </div>
              </div>
            </div>

            {/* Row 4: Password and Confirm Password */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-heading font-semibold text-slate-700 mb-1.5">
                  Password *
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={form.password}
                    onChange={(e) => setForm({ ...form, password: e.target.value })}
                    placeholder="Min. 6 characters"
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

              <div>
                <label className="block text-xs font-heading font-semibold text-slate-700 mb-1.5">
                  Confirm Password *
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={form.confirmPassword}
                    onChange={(e) => setForm({ ...form, confirmPassword: e.target.value })}
                    placeholder="Re-enter password"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-slate-800 text-sm focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all font-sans"
                  />
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 rounded-xl font-heading font-semibold text-sm text-white bg-gradient-to-r from-brand-600 via-indigo-600 to-indigo-700 hover:from-brand-500 hover:to-indigo-600 transition-all shadow-md shadow-brand-500/25 flex items-center justify-center gap-2 active:scale-95 disabled:opacity-60 mt-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Registering Campus Identity...</span>
                </>
              ) : (
                <>
                  <span>Create Account & Continue</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Bottom Switch to Sign In */}
          <div className="pt-4 border-t border-slate-100 text-center">
            <p className="text-xs text-slate-500">
              Already have an account?{' '}
              <button
                type="button"
                onClick={() => onNavigate && onNavigate('login')}
                className="font-semibold text-brand-600 hover:text-brand-700 underline underline-offset-2 ml-1"
              >
                Sign in to your portal
              </button>
            </p>
          </div>

        </div>

      </div>
    </div>
  );
}
