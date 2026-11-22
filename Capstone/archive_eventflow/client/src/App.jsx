import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar.jsx';
import ParticipantPortal from './components/ParticipantPortal.jsx';
import RegistrationModal from './components/RegistrationModal.jsx';
import TicketPassModal from './components/TicketPassModal.jsx';
import MyTicketsModal from './components/MyTicketsModal.jsx';

// Dedicated Auth Pages
import LoginPage from './pages/LoginPage.jsx';
import SignupPage from './pages/SignupPage.jsx';

// Admin Components
import AdminLayout from './components/admin/AdminLayout.jsx';
import AnalyticsOverview from './components/admin/AnalyticsOverview.jsx';
import EventManager from './components/admin/EventManager.jsx';
import RegistrationsManager from './components/admin/RegistrationsManager.jsx';
import AnnouncementBroadcast from './components/admin/AnnouncementBroadcast.jsx';
import TicketScannerModal from './components/admin/TicketScannerModal.jsx';

// Auth Hook & Modals
import { useAuth } from './context/useAuth.js';
import { useToast } from './context/ToastContext.jsx';
import AuthModal from './components/auth/AuthModal.jsx';
import UserProfileModal from './components/auth/UserProfileModal.jsx';

export default function App() {
  const { 
    role: authRole, 
    user,
    isAuthModalOpen,
    closeAuthModal,
    authModalTab,
    openAuthModal,
    isProfileModalOpen,
    closeProfileModal,
    openProfileModal
  } = useAuth();
  const toast = useToast();

  // Navigation View: 'events' | 'admin' | 'login' | 'signup'
  const [currentView, setCurrentView] = useState(() => {
    const hash = window.location.hash.replace('#/', '').replace('#', '');
    if (['events', 'admin', 'login', 'signup'].includes(hash)) {
      return hash;
    }
    return 'events';
  });

  const [adminTab, setAdminTab] = useState('overview'); // 'overview' | 'events' | 'registrations' | 'announcements' | 'scanner'
  const [adminEventFilter, setAdminEventFilter] = useState('All');

  // Modals state
  const [registeringEvent, setRegisteringEvent] = useState(null);
  const [activeTicketPass, setActiveTicketPass] = useState(null);
  const [isMyTicketsOpen, setIsMyTicketsOpen] = useState(false);

  // Sync hash with browser URL
  const handleNavigate = (view) => {
    setCurrentView(view);
    window.location.hash = `#/${view}`;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Listen to popstate (browser back/forward buttons)
  useEffect(() => {
    const handlePopState = () => {
      const hash = window.location.hash.replace('#/', '').replace('#', '');
      if (['events', 'admin', 'login', 'signup'].includes(hash)) {
        setCurrentView(hash);
      } else {
        setCurrentView('events');
      }
    };
    window.addEventListener('popstate', handlePopState);
    window.addEventListener('hashchange', handlePopState);
    return () => {
      window.removeEventListener('popstate', handlePopState);
      window.removeEventListener('hashchange', handlePopState);
    };
  }, []);

  // If user signs out while in admin view, revert to events view
  useEffect(() => {
    if (authRole !== 'admin' && currentView === 'admin') {
      handleNavigate('events');
    }
  }, [authRole, currentView]);

  const handleRegisterEvent = (event) => {
    setRegisteringEvent(event);
  };

  const handleRegistrationSuccess = (issuedTicket) => {
    setRegisteringEvent(null);
    setActiveTicketPass(issuedTicket);
    toast.success(
      `Pass issued for "${issuedTicket.event_title || issuedTicket.title || 'Event'}"! Ticket Code: ${issuedTicket.ticket_code}`,
      'Registration Confirmed'
    );
  };

  const handleOpenMyTickets = () => {
    setIsMyTicketsOpen(true);
  };

  const handleViewPassFromLookup = (pass) => {
    setIsMyTicketsOpen(false);
    setActiveTicketPass(pass);
  };

  const handleManageEventRegistrations = (eventId) => {
    setAdminEventFilter(eventId);
    setAdminTab('registrations');
  };

  const handleAuthSuccess = (authedUser) => {
    toast.success(
      `Signed in as ${authedUser.name} (${authedUser.role === 'admin' ? (authedUser.roleTitle || 'Organizer') : 'Student'})`,
      'Welcome to EventFlow'
    );
    if (authedUser.role === 'admin') {
      handleNavigate('admin');
    } else {
      handleNavigate('events');
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans text-slate-800 antialiased selection:bg-brand-500 selection:text-white">
      
      {/* Show Top Navbar on all views except full admin dashboard which has its own sidebar layout */}
      {currentView !== 'admin' && (
        <Navbar
          currentView={currentView}
          onNavigate={handleNavigate}
          onOpenMyTickets={handleOpenMyTickets}
        />
      )}

      {/* Main View Router */}
      {currentView === 'events' && (
        <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 pt-6">
          <ParticipantPortal
            onRegisterEvent={handleRegisterEvent}
            onOpenMyTickets={handleOpenMyTickets}
          />
        </main>
      )}

      {currentView === 'login' && (
        <main className="flex-1 w-full">
          <LoginPage
            onNavigate={handleNavigate}
            onSuccess={handleAuthSuccess}
          />
        </main>
      )}

      {currentView === 'signup' && (
        <main className="flex-1 w-full">
          <SignupPage
            onNavigate={handleNavigate}
            onSuccess={handleAuthSuccess}
          />
        </main>
      )}

      {currentView === 'admin' && (
        <AdminLayout
          activeTab={adminTab}
          setActiveTab={(tab) => {
            if (tab !== 'registrations') setAdminEventFilter('All');
            setAdminTab(tab);
          }}
          onSwitchToParticipant={() => handleNavigate('events')}
        >
          {adminTab === 'overview' && <AnalyticsOverview />}
          {adminTab === 'events' && (
            <EventManager onManageRegistrations={handleManageEventRegistrations} />
          )}
          {adminTab === 'registrations' && (
            <RegistrationsManager initialEventId={adminEventFilter} />
          )}
          {adminTab === 'announcements' && <AnnouncementBroadcast />}
          {adminTab === 'scanner' && <TicketScannerModal />}
        </AdminLayout>
      )}

      {/* Footer (shown on non-admin views) */}
      {currentView !== 'admin' && (
        <footer className="bg-navy-950 border-t border-slate-800 text-slate-400 py-8 px-4 text-center text-xs space-y-2 mt-auto">
          <div className="flex items-center justify-center gap-2">
            <span className="font-display text-xs tracking-wider text-slate-200">EVENTFLOW</span>
            <span>•</span>
            <span className="font-heading font-medium text-slate-400">Campus Event Coordination Operating System</span>
          </div>
          <p className="text-slate-400 text-xs">
            Smart Campus Event Registration & Management Portal. Built for college organizers, department societies, and student attendees.
          </p>
        </footer>
      )}

      {/* Shared Modals */}
      <RegistrationModal
        event={registeringEvent}
        isOpen={!!registeringEvent}
        onClose={() => setRegisteringEvent(null)}
        onRegistrationSuccess={handleRegistrationSuccess}
      />

      <TicketPassModal
        ticket={activeTicketPass}
        isOpen={!!activeTicketPass}
        onClose={() => setActiveTicketPass(null)}
      />

      <MyTicketsModal
        isOpen={isMyTicketsOpen}
        onClose={() => setIsMyTicketsOpen(false)}
        onViewPass={handleViewPassFromLookup}
      />

      {/* Contextual Auth Modal for in-place actions (e.g. clicking Register while logged out) */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={closeAuthModal}
        initialTab={authModalTab}
        onSuccess={(authedUser) => {
          closeAuthModal();
          handleAuthSuccess(authedUser);
        }}
      />

      {/* Global User Profile Modal */}
      <UserProfileModal
        isOpen={isProfileModalOpen}
        onClose={closeProfileModal}
        onOpenMyTickets={handleOpenMyTickets}
        onSwitchUser={() => {
          closeProfileModal();
          handleNavigate('login');
        }}
      />

    </div>
  );
}
