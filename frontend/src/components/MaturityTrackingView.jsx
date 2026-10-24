import React, { useState, useEffect } from 'react';
import { 
  AlertTriangle, Clock, ShieldAlert, CheckCircle2, RefreshCw, 
  Send, Bell, Calendar, ChevronRight, Check, AlertCircle
} from 'lucide-react';

export default function MaturityTrackingView({ alerts, onRefreshAll }) {
  const [activeAlerts, setActiveAlerts] = useState(alerts || []);
  const [sweepLoading, setSweepLoading] = useState(false);
  const [sweepResult, setSweepResult] = useState(null);
  const [simulatedDate, setSimulatedDate] = useState('');

  const fetchAlerts = async () => {
    try {
      const res = await fetch('/api/maturity/alerts');
      if (res.ok) {
        const data = await res.json();
        setActiveAlerts(data.alerts || []);
      }
    } catch (err) {
      console.error("Failed to load alerts:", err);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, [alerts]);

  const handleRunSweep = async () => {
    setSweepLoading(true);
    setSweepResult(null);
    try {
      const res = await fetch('/api/maturity/run-sweep', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          simulated_date: simulatedDate || undefined
        })
      });
      if (res.ok) {
        const data = await res.json();
        setSweepResult(data);
        fetchAlerts();
        onRefreshAll?.();
      }
    } catch (err) {
      console.error("Sweep failed:", err);
    } finally {
      setSweepLoading(false);
    }
  };

  const handleResolveAlert = async (alertId) => {
    try {
      const res = await fetch(`/api/maturity/alerts/${alertId}/resolve`, {
        method: 'POST'
      });
      if (res.ok) {
        fetchAlerts();
        onRefreshAll?.();
      }
    } catch (err) {
      console.error("Resolve failed:", err);
    }
  };

  const getUrgencyBadge = (urgency) => {
    switch (urgency) {
      case 'CRITICAL':
        return <span className="inline-flex items-center px-1.5 py-0.2 rounded text-[10px] font-bold bg-rose-50 text-rose-800 border border-rose-200">CRITICAL</span>;
      case 'HIGH':
        return <span className="inline-flex items-center px-1.5 py-0.2 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200">HIGH</span>;
      case 'MEDIUM':
        return <span className="inline-flex items-center px-1.5 py-0.2 rounded text-[10px] font-bold bg-blue-50 text-blue-900 border border-blue-200">MEDIUM</span>;
      default:
        return <span className="inline-flex items-center px-1.5 py-0.2 rounded text-[10px] font-medium bg-slate-100 text-slate-700">ROUTINE</span>;
    }
  };

  return (
    <div className="space-y-5 animate-entrance">
      {/* Top Sweep / Simulation Card */}
      <div className="card-institutional p-5 bg-white border border-slate-200 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
              <Clock className="h-4 w-4 text-blue-900" />
              <span>Autonomous Maturity Engine & Simulation Sandbox</span>
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Continuously computes maturity countdowns and triggers multi-channel statutory alerts (T-180, T-90, T-30, D-Day)
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="date"
              value={simulatedDate}
              onChange={(e) => setSimulatedDate(e.target.value)}
              className="px-2.5 py-1.5 rounded border border-slate-300 bg-white text-xs font-mono font-medium text-slate-800 focus:border-blue-900 focus:outline-none"
            />
            <button
              onClick={handleRunSweep}
              disabled={sweepLoading}
              className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-md bg-blue-900 hover:bg-blue-950 text-white font-semibold text-xs shadow-xs transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${sweepLoading ? 'animate-spin' : ''}`} />
              <span>{sweepLoading ? 'Evaluating...' : 'Execute Sweep'}</span>
            </button>
          </div>
        </div>

        {sweepResult && (
          <div className="p-3 rounded border border-slate-200 bg-slate-50/70 text-xs space-y-1 font-mono">
            <div className="flex items-center justify-between text-slate-700 font-sans font-bold">
              <span className="text-emerald-800">Maturity Sweep Complete</span>
              <span>Effective Date: {sweepResult.effective_date}</span>
            </div>
            <div className="text-[11px] text-slate-600 font-sans">
              Evaluated <span className="font-semibold text-slate-800">{sweepResult.evaluated_instruments}</span> instruments. Dispatched <span className="font-semibold text-rose-700">{sweepResult.alerts_generated}</span> statutory notices.
            </div>
          </div>
        )}
      </div>

      {/* 4 Clean Milestone Horizon Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <div className="card-institutional p-3.5 bg-white border border-slate-200 space-y-1">
          <div className="flex items-center justify-between text-[11px] font-bold text-slate-500">
            <span>T-180 DAYS</span>
            <span className="px-1.5 py-0.2 rounded bg-slate-100 text-slate-700 text-[10px]">Tier 1</span>
          </div>
          <div className="text-xs font-bold text-slate-900">First Advisory Notice</div>
          <p className="text-[10.5px] text-slate-500 leading-normal">
            Automated SMS & Portal notification requesting renewal pledge or closure NOC paperwork.
          </p>
        </div>

        <div className="card-institutional p-3.5 bg-white border border-slate-200 space-y-1">
          <div className="flex items-center justify-between text-[11px] font-bold text-slate-500">
            <span>T-90 DAYS</span>
            <span className="px-1.5 py-0.2 rounded bg-amber-50 text-amber-800 text-[10px] border border-amber-200">Tier 2</span>
          </div>
          <div className="text-xs font-bold text-slate-900">Regional Directorate Notice</div>
          <p className="text-[10.5px] text-slate-500 leading-normal">
            Copy marked to Principal and Regional Officer. Bank informed of mandatory renewal requirement.
          </p>
        </div>

        <div className="card-institutional p-3.5 bg-white border border-slate-200 space-y-1">
          <div className="flex items-center justify-between text-[11px] font-bold text-slate-500">
            <span>T-30 DAYS</span>
            <span className="px-1.5 py-0.2 rounded bg-rose-50 text-rose-800 text-[10px] border border-rose-200">Tier 3</span>
          </div>
          <div className="text-xs font-bold text-slate-900">Urgent Statutory Summons</div>
          <p className="text-[10.5px] text-slate-500 leading-normal">
            Mandatory personal appearance before Scrutiny Officer; warning of EoA hold for next academic year.
          </p>
        </div>

        <div className="card-institutional p-3.5 bg-white border border-slate-200 space-y-1">
          <div className="flex items-center justify-between text-[11px] font-bold text-slate-500">
            <span>D-DAY & OVERDUE</span>
            <span className="px-1.5 py-0.2 rounded bg-rose-100 text-rose-900 text-[10px] border border-rose-300 font-bold">Default</span>
          </div>
          <div className="text-xs font-bold text-rose-900">Encashment / Show Cause</div>
          <p className="text-[10.5px] text-slate-500 leading-normal">
            Immediate invocation of AICTE regulatory lien under Section 10(k) AICTE Act 1987.
          </p>
        </div>
      </div>

      {/* Active Notices Queue (Clean Fintech Table) */}
      <div className="card-institutional bg-white border border-slate-200 overflow-hidden">
        <div className="p-3.5 border-b border-slate-200 flex items-center justify-between bg-slate-50/60">
          <div>
            <h3 className="text-xs font-bold text-slate-900">Active Regulatory Notices & Dispatch Ledger</h3>
            <p className="text-[11px] text-slate-500">Pending statutory actions requiring acknowledgment</p>
          </div>
          <span className="text-[11px] font-semibold text-slate-700 bg-white px-2 py-0.5 rounded border border-slate-200">
            {activeAlerts.filter(a => !a.is_resolved).length} Pending Acknowledgment
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full table-fintech text-left">
            <thead>
              <tr>
                <th>Notice Type & Urgency</th>
                <th>Institution & State</th>
                <th>Days to Maturity</th>
                <th>Dispatch Channels</th>
                <th>Dispatched At</th>
                <th className="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              {activeAlerts.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-slate-500 text-xs">
                    No active maturity notices. All pledged collateral instruments within compliant validity horizon.
                  </td>
                </tr>
              ) : (
                activeAlerts.map((a) => (
                  <tr key={a.id} className={a.is_resolved ? 'opacity-60 bg-slate-50/40' : ''}>
                    <td>
                      <div className="flex items-center space-x-1.5">
                        {getUrgencyBadge(a.urgency)}
                        <span className="font-semibold text-slate-900 text-xs">{a.alert_type}</span>
                      </div>
                      <div className="text-[10.5px] text-slate-500 font-mono mt-0.5">FDR: {a.fdr?.fdr_number || "FDR-COLLATERAL"}</div>
                    </td>

                    <td>
                      <div className="font-medium text-slate-800 text-xs">{a.institution_name}</div>
                      <div className="text-[10px] text-slate-500">PID: {a.fdr?.institution?.pid || "N/A"}</div>
                    </td>

                    <td>
                      <span className={`font-mono font-bold text-xs ${
                        a.days_to_maturity < 0 ? 'text-rose-700' : a.days_to_maturity <= 30 ? 'text-amber-700' : 'text-slate-800'
                      }`}>
                        {a.days_to_maturity < 0 ? `${Math.abs(a.days_to_maturity)} Days OVERDUE` : `${a.days_to_maturity} Days Remaining`}
                      </span>
                    </td>

                    <td>
                      <div className="text-[10.5px] text-slate-600 font-mono">
                        {a.channels_dispatched || "PORTAL, EMAIL, SMS"}
                      </div>
                    </td>

                    <td>
                      <div className="text-[10.5px] text-slate-500 font-mono">
                        {new Date(a.created_at).toLocaleDateString()}
                      </div>
                    </td>

                    <td className="text-center">
                      {a.is_resolved ? (
                        <span className="inline-flex items-center text-[10.5px] text-emerald-700 font-semibold space-x-1">
                          <Check className="h-3 w-3" />
                          <span>Resolved</span>
                        </span>
                      ) : (
                        <button
                          onClick={() => handleResolveAlert(a.id)}
                          className="px-2 py-1 rounded border border-slate-300 bg-white hover:bg-slate-50 text-[11px] font-medium text-slate-700 hover:text-blue-900 transition-colors"
                        >
                          Acknowledge
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
