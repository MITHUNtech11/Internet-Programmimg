import React, { useState } from 'react';
import { 
  Calendar, 
  Ticket, 
  ShieldCheck, 
  Sparkles, 
  Cloud, 
  Database, 
  LogIn, 
  UserPlus,
  ChevronDown,
  LogOut,
  Menu,
  X,
  User
} from 'lucide-react';
import { isSupabaseConfigured } from '../services/supabaseClient.js';
import { useAuth } from '../context/useAuth.js';

export default function Navbar({ 
  currentView = 'events', 
  onNavigate, 
  onOpenMyTickets 
}) {
  const isCloudActive = isSupabaseConfigured();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const { 
    user, 
    role, 
    isAuthenticated,
    openAuthModal,
    openProfileModal,
    logout
  } = useAuth();

  const handleNavClick = (view) => {
    setMobileMenuOpen(false);
    if (view === 'admin') {
      if (role !== 'admin') {
        openAuthModal('admin');
        return;
      }
    }
    if (onNavigate) {
      onNavigate(view);
    }
  };

  const handleOpenPasses = () => {
    setMobileMenuOpen(false);
    if (onOpenMyTickets) {
      onOpenMyTickets();
    }
  };

  const handleSignOut = () => {
    setMobileMenuOpen(false);
    logout();
    if (currentView === 'admin') {
      if (onNavigate) onNavigate('events');
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-navy-900/95 backdrop-blur-md border-b border-slate-800 text-white shadow-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20">
          
          {/* Brand Logo & Tagline */}
          <div 
            onClick={() => handleNavClick('events')}
            className="flex items-center gap-3.5 cursor-pointer select-none group"
            title="Go to EventFlow Home"
          >
            <div className="relative">
              <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-2xl bg-gradient-to-tr from-brand-600 via-indigo-500 to-violet-400 flex items-center justify-center shadow-lg shadow-indigo-500/25 border border-indigo-400/30 group-hover:scale-105 transition-transform">
                <Sparkles className="w-5 h-5 text-white animate-pulse" />
              </div>
              <span className="absolute -bottom-1 -right-1 flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500 border-2 border-navy-900"></span>
              </span>
            </div>

            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg sm:text-xl tracking-tight bg-gradient-to-r from-white via-indigo-100 to-indigo-300 bg-clip-text text-transparent">
                  EVENTFLOW
                </span>
                
                {/* Cloud / Engine Indicator */}
                {isCloudActive ? (
                  <span className="hidden sm:inline-flex items-center gap-1 text-[11px] font-semibold tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                    <Cloud className="w-3 h-3 text-emerald-400" />
                    Supabase Cloud
                  </span>
                ) : (
                  <span className="hidden sm:inline-flex items-center gap-1 text-[11px] font-semibold tracking-wider px-2 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30">
                    <Database className="w-3 h-3 text-brand-400" />
                    FastAPI Engine
                  </span>
                )}
              </div>
              <p className="text-[11px] text-slate-400 font-normal tracking-tight -mt-0.5 hidden xs:block">
                Smart Campus Event Coordination Platform
              </p>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-1 bg-navy-950/80 p-1.5 rounded-2xl border border-slate-800 shadow-inner">
            <button
              onClick={() => handleNavClick('events')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-heading font-semibold transition-all duration-200 ${
                currentView === 'events'
                  ? 'bg-gradient-to-r from-brand-600 to-indigo-600 text-white shadow-md shadow-brand-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <Calendar className="w-4 h-4" />
              <span>Events</span>
            </button>

            <button
              onClick={handleOpenPasses}
              className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-heading font-semibold text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition-all duration-200"
              title="View my registered passes"
            >
              <Ticket className="w-4 h-4 text-brand-400" />
              <span>My Passes</span>
            </button>

            <button
              onClick={() => handleNavClick('admin')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-heading font-semibold transition-all duration-200 ${
                currentView === 'admin'
                  ? 'bg-gradient-to-r from-indigo-700 to-purple-700 text-white shadow-md shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
              title={role !== 'admin' ? 'Organizer / Faculty access only' : 'Switch to Admin Command OS'}
            >
              <ShieldCheck className="w-4 h-4 text-purple-400" />
              <span>Admin Suite</span>
            </button>
          </nav>

          {/* Right Section: Auth & Profile */}
          <div className="flex items-center gap-2.5 sm:gap-3">
            
            {/* Authenticated User View */}
            {isAuthenticated && user ? (
              <div className="flex items-center gap-2">
                <button
                  onClick={() => openProfileModal()}
                  className="flex items-center gap-2.5 p-1.5 sm:pr-3 rounded-2xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/90 text-left transition-all hover:border-brand-500/40 shadow-sm group"
                  title="Open user profile settings"
                >
                  <div className="relative shrink-0">
                    <img
                      src={user.avatar || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80'}
                      alt={user.name}
                      className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl object-cover border border-white/20 shadow-sm"
                    />
                    <span className="absolute -bottom-0.5 -right-0.5 flex h-2.5 w-2.5">
                      <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500 border border-navy-900"></span>
                    </span>
                  </div>

                  <div className="hidden lg:block max-w-[130px]">
                    <span className="font-heading font-bold text-xs text-white block truncate leading-tight group-hover:text-brand-300 transition-colors">
                      {user.name}
                    </span>
                    <span className="text-[11px] text-slate-400 font-medium block truncate leading-tight mt-0.5">
                      {user.role === 'admin' ? (user.roleTitle || 'Organizer') : 'Student'}
                    </span>
                  </div>

                  <ChevronDown className="w-3.5 h-3.5 text-slate-400 group-hover:text-white transition-colors hidden sm:block shrink-0" />
                </button>

                {/* Quick Logout Button */}
                <button
                  onClick={handleSignOut}
                  className="p-2 sm:p-2.5 rounded-xl bg-slate-800/80 hover:bg-rose-900/40 hover:text-rose-300 text-slate-400 border border-slate-700/80 transition-all hover:border-rose-500/30"
                  title="Sign out of EventFlow"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              /* Unauthenticated / Guest State */
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleNavClick('login')}
                  className={`flex items-center gap-1.5 px-3 py-2 sm:px-3.5 sm:py-2 rounded-xl text-xs font-heading font-semibold transition-all border ${
                    currentView === 'login'
                      ? 'bg-slate-700 text-white border-brand-500'
                      : 'bg-slate-800/80 hover:bg-slate-700 text-slate-200 border-slate-700 hover:text-white'
                  }`}
                >
                  <LogIn className="w-4 h-4 text-brand-400" />
                  <span>Sign In</span>
                </button>

                <button
                  onClick={() => handleNavClick('signup')}
                  className="flex items-center gap-1.5 px-3.5 py-2 sm:px-4 sm:py-2 rounded-xl text-xs font-heading font-semibold text-white bg-gradient-to-r from-brand-600 via-indigo-600 to-indigo-700 hover:from-brand-500 hover:to-indigo-600 transition-all shadow-md shadow-brand-500/20 active:scale-95"
                >
                  <UserPlus className="w-4 h-4" />
                  <span className="hidden xs:inline">Sign Up</span>
                </button>
              </div>
            )}

            {/* Mobile Menu Toggle Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition-colors"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>

          </div>

        </div>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-800 bg-navy-950/95 backdrop-blur-xl px-4 pt-3 pb-5 space-y-3 animate-in slide-in-from-top-2 duration-200">
          <div className="flex flex-col gap-1.5">
            <button
              onClick={() => handleNavClick('events')}
              className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-heading font-semibold transition-all ${
                currentView === 'events'
                  ? 'bg-brand-600/20 text-brand-300 border border-brand-500/40'
                  : 'text-slate-300 hover:bg-slate-800/60'
              }`}
            >
              <Calendar className="w-4 h-4 text-brand-400" />
              <span>Event Catalog</span>
            </button>

            <button
              onClick={handleOpenPasses}
              className="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-heading font-semibold text-slate-300 hover:bg-slate-800/60 transition-all"
            >
              <Ticket className="w-4 h-4 text-brand-400" />
              <span>My Registered Passes</span>
            </button>

            <button
              onClick={() => handleNavClick('admin')}
              className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-heading font-semibold transition-all ${
                currentView === 'admin'
                  ? 'bg-purple-600/20 text-purple-300 border border-purple-500/40'
                  : 'text-slate-300 hover:bg-slate-800/60'
              }`}
            >
              <ShieldCheck className="w-4 h-4 text-purple-400" />
              <span>Organizer Admin Suite</span>
            </button>
          </div>

          <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
            {isAuthenticated && user ? (
              <div className="flex items-center justify-between w-full">
                <div 
                  onClick={() => { setMobileMenuOpen(false); openProfileModal(); }}
                  className="flex items-center gap-2.5 cursor-pointer"
                >
                  <img
                    src={user.avatar || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80'}
                    alt={user.name}
                    className="w-8 h-8 rounded-xl object-cover border border-white/20"
                  />
                  <div>
                    <span className="font-heading font-bold text-xs text-white block">
                      {user.name}
                    </span>
                    <span className="text-[11px] text-slate-400 block">
                      {user.role === 'admin' ? (user.roleTitle || 'Organizer') : 'Student'}
                    </span>
                  </div>
                </div>

                <button
                  onClick={handleSignOut}
                  className="px-3 py-1.5 rounded-xl text-xs font-semibold text-rose-300 bg-rose-500/10 border border-rose-500/20"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-2 w-full">
                <button
                  onClick={() => handleNavClick('login')}
                  className="w-full py-2.5 px-3 rounded-xl text-xs font-heading font-semibold text-center bg-slate-800 text-slate-200 border border-slate-700"
                >
                  Sign In
                </button>
                <button
                  onClick={() => handleNavClick('signup')}
                  className="w-full py-2.5 px-3 rounded-xl text-xs font-heading font-semibold text-center text-white bg-gradient-to-r from-brand-600 to-indigo-600"
                >
                  Sign Up
                </button>
              </div>
            )}
          </div>
        </div>
      )}

    </header>
  );
}
