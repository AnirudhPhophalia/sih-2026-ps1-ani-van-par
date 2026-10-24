import React, { useState, useEffect } from 'react';
import Sidebar, { PERSONAS } from './components/Sidebar';
import Header from './components/Header';
import DashboardView from './components/DashboardView';
import FDRRepositoryView from './components/FDRRepositoryView';
import ScrutinyDeskView from './components/ScrutinyDeskView';
import BankGatewayView from './components/BankGatewayView';
import MaturityTrackingView from './components/MaturityTrackingView';
import ReleaseWorkflowView from './components/ReleaseWorkflowView';
import AuditLedgerView from './components/AuditLedgerView';
import NewFDRModal from './components/NewFDRModal';
import AlertsDrawerModal from './components/AlertsDrawerModal';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentPersona, setCurrentPersona] = useState('SCRUTINY_OFFICER');

  // Shared state
  const [analytics, setAnalytics] = useState(null);
  const [fdrs, setFdrs] = useState([]);
  const [institutions, setInstitutions] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modals
  const [newFdrOpen, setNewFdrOpen] = useState(false);
  const [alertsDrawerOpen, setAlertsDrawerOpen] = useState(false);
  const [sweepLoading, setSweepLoading] = useState(false);

  const fetchAllData = async () => {
    try {
      const [analyticsRes, fdrsRes, instRes, alertsRes] = await Promise.all([
        fetch('/api/analytics/dashboard'),
        fetch('/api/fdrs'),
        fetch('/api/institutions'),
        fetch('/api/maturity/alerts')
      ]);

      if (analyticsRes.ok) setAnalytics(await analyticsRes.json());
      if (fdrsRes.ok) {
        const d = await fdrsRes.json();
        setFdrs(d.fdrs || []);
      }
      if (instRes.ok) {
        const d = await instRes.json();
        setInstitutions(d.institutions || []);
      }
      if (alertsRes.ok) {
        const d = await alertsRes.json();
        setAlerts(d.alerts || []);
      }
    } catch (err) {
      console.error("Error fetching data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllData();
  }, []);

  const handleRunGlobalSweep = async (simDate = null) => {
    setSweepLoading(true);
    try {
      const res = await fetch('/api/maturity/run-sweep', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ simulated_date: simDate || undefined })
      });
      if (res.ok) {
        await fetchAllData();
      }
    } catch (err) {
      console.error("Global sweep failed:", err);
    } finally {
      setSweepLoading(false);
    }
  };

  const handleResolveAlert = async (alertId) => {
    try {
      const res = await fetch(`/api/maturity/alerts/${alertId}/resolve`, { method: 'POST' });
      if (res.ok) {
        fetchAllData();
      }
    } catch (err) {
      console.error("Resolve failed:", err);
    }
  };

  const unresolvedAlertsCount = alerts.filter(a => !a.is_resolved).length;
  const activePersonaObj = PERSONAS.find(p => p.role === currentPersona) || PERSONAS[0];

  return (
    <div className="min-h-screen flex bg-canvas-pattern text-slate-800 font-sans selection:bg-blue-900 selection:text-white">
      {/* Sleek Vertical Institutional Sidebar */}
      <Sidebar
        currentPersona={currentPersona}
        setCurrentPersona={setCurrentPersona}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        unresolvedAlertsCount={unresolvedAlertsCount}
        onOpenAlerts={() => setAlertsDrawerOpen(true)}
        onOpenNewFDR={() => setNewFdrOpen(true)}
      />

      {/* Main View Area */}
      <div className="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto">
        {/* Top Institutional Header */}
        <Header
          activeTab={activeTab}
          unresolvedAlertsCount={unresolvedAlertsCount}
          onOpenAlerts={() => setAlertsDrawerOpen(true)}
          activePersonaObj={activePersonaObj}
        />

        {/* Content Canvas */}
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-32 space-y-3">
              <div className="h-8 w-8 animate-spin rounded-full border-2 border-blue-900 border-t-transparent"></div>
              <p className="text-xs text-slate-500 font-medium">Synchronizing with AICTE Statutory Collateral Registry...</p>
            </div>
          ) : (
            <div className="animate-entrance">
              {activeTab === 'dashboard' && (
                <DashboardView
                  analytics={analytics}
                  onNavigateTab={(tab) => setActiveTab(tab)}
                  onRunSweep={() => handleRunGlobalSweep()}
                  sweepLoading={sweepLoading}
                  activePersona={activePersonaObj}
                />
              )}

              {activeTab === 'repository' && (
                <FDRRepositoryView
                  fdrs={fdrs}
                  onOpenNewFDR={() => setNewFdrOpen(true)}
                  onNavigateTab={(tab) => setActiveTab(tab)}
                />
              )}

              {activeTab === 'scrutiny' && (
                <ScrutinyDeskView onRefreshAll={fetchAllData} />
              )}

              {activeTab === 'bank-gateway' && (
                <BankGatewayView fdrs={fdrs} onRefreshAll={fetchAllData} />
              )}

              {activeTab === 'maturity' && (
                <MaturityTrackingView alerts={alerts} onRefreshAll={fetchAllData} />
              )}

              {activeTab === 'release' && (
                <ReleaseWorkflowView onRefreshAll={fetchAllData} />
              )}

              {activeTab === 'audit' && (
                <AuditLedgerView />
              )}
            </div>
          )}
        </main>

        {/* Institutional Minimal Footer */}
        <footer className="border-t border-slate-200/90 bg-white/95 py-3.5 px-8 text-xs text-slate-500">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-slate-700">All India Council for Technical Education</span>
              <span className="text-slate-300">|</span>
              <span>Ministry of Education, Government of India</span>
            </div>
            <div className="flex items-center space-x-3 text-[11px] text-slate-500 font-medium">
              <span>Section 10(k) AICTE Act 1987</span>
              <span>•</span>
              <span>DPDP Act 2023 Compliant</span>
              <span>•</span>
              <span className="font-mono text-blue-900 font-semibold">256-bit Immutable Audit</span>
            </div>
          </div>
        </footer>
      </div>

      {/* New FDR Modal */}
      <NewFDRModal
        isOpen={newFdrOpen}
        onClose={() => setNewFdrOpen(false)}
        institutions={institutions}
        onCreated={() => fetchAllData()}
      />

      {/* Alerts Drawer */}
      <AlertsDrawerModal
        isOpen={alertsDrawerOpen}
        onClose={() => setAlertsDrawerOpen(false)}
        alerts={alerts}
        onResolveAlert={handleResolveAlert}
      />
    </div>
  );
}
