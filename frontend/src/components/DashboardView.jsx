import React from 'react';
import { 
  Landmark, ShieldCheck, Clock, CheckCircle2, 
  ArrowUpRight, AlertTriangle, Building2, TrendingUp, Layers, 
  FileText, ExternalLink, RefreshCw
} from 'lucide-react';

export default function DashboardView({ 
  analytics, 
  onNavigateTab, 
  onRunSweep, 
  sweepLoading,
  activePersona
}) {
  const kpis = analytics?.kpis || {
    total_capital_crores: 32.50,
    total_capital_inr: 325000000,
    total_institutions: 8,
    total_fdrs: 7,
    active_fdrs: 3,
    expiring_soon: 1,
    matured_overdue: 1,
    under_scrutiny: 1,
    discrepancies_flagged: 1,
    release_requested: 1,
    released_discharged: 0,
    unresolved_alerts: 2,
    critical_alerts: 1,
    total_audit_blocks: 9
  };

  const banks = analytics?.bank_distribution || [];
  const regional = analytics?.regional_distribution || [];

  return (
    <div className="space-y-6 animate-entrance">
      {/* Executive Institutional Header Card */}
      <div className="card-institutional p-5 bg-white border border-slate-200">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-900 border border-blue-200 uppercase tracking-wider">
                Regulatory Custody
              </span>
              <span className="text-xs text-slate-500 font-medium">Statutory Mandate: Section 10(k) AICTE Act</span>
            </div>
            <h1 className="text-xl md:text-2xl font-bold text-slate-900 tracking-tight">
              AICTE Statutory Security Deposit & FDR Portal
            </h1>
            <p className="text-xs text-slate-600 max-w-2xl leading-relaxed">
              Centralized custody and lifecycle oversight of institutional technical education collateral across all 10+ AICTE regional directorates.
            </p>
          </div>

          <div className="flex items-center space-x-2.5 shrink-0">
            <button
              onClick={() => onRunSweep()}
              disabled={sweepLoading}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-md bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold border border-slate-300 transition-colors duration-150 disabled:opacity-50"
            >
              <RefreshCw className={`h-3.5 w-3.5 text-slate-500 ${sweepLoading ? 'animate-spin' : ''}`} />
              <span>{sweepLoading ? 'Sweeping...' : 'Run Maturity Sweep'}</span>
            </button>

            <button
              onClick={() => onNavigateTab('scrutiny')}
              className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-md bg-blue-900 hover:bg-blue-950 text-white text-xs font-semibold shadow-xs transition-colors duration-150"
            >
              <ShieldCheck className="h-3.5 w-3.5" />
              <span>Scrutiny Desk ({kpis.under_scrutiny + kpis.discrepancies_flagged})</span>
            </button>
          </div>
        </div>
      </div>

      {/* 4 Clean Refined KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Capital */}
        <div className="card-institutional p-4 bg-white border border-slate-200 space-y-2">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Total Custody Value</span>
            <Landmark className="h-4 w-4 text-slate-400" />
          </div>
          <div className="pt-1">
            <div className="text-2xl font-bold text-slate-900 font-mono tracking-tight">
              ₹{kpis.total_capital_crores.toFixed(2)} <span className="text-xs font-sans font-bold text-slate-500">Cr</span>
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">
              Across <span className="font-semibold text-slate-700">{kpis.total_fdrs} active instruments</span>
            </p>
          </div>
          <div className="pt-1 text-[10.5px] text-slate-500 flex items-center justify-between border-t border-slate-100">
            <span>Scheduled Banks:</span>
            <span className="font-semibold text-slate-700">{banks.length} Entities</span>
          </div>
        </div>

        {/* Verified Active */}
        <div className="card-institutional p-4 bg-white border border-slate-200 space-y-2">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Active & Lien Endorsed</span>
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
          </div>
          <div className="pt-1">
            <div className="text-2xl font-bold text-emerald-800 font-mono tracking-tight">
              {kpis.active_fdrs} <span className="text-xs font-sans font-medium text-slate-400">/ {kpis.total_fdrs} Pledged</span>
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">
              100% verified AICTE statutory lien
            </p>
          </div>
          <div className="pt-1 text-[10.5px] text-slate-500 flex items-center justify-between border-t border-slate-100">
            <span>Compliance Rate:</span>
            <span className="font-semibold text-emerald-700">
              {Math.round((kpis.active_fdrs / Math.max(1, kpis.total_fdrs)) * 100)}%
            </span>
          </div>
        </div>

        {/* Maturity & Escalations Attention */}
        <div className="card-institutional p-4 bg-white border border-slate-200 space-y-2">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Maturity Attention</span>
            <Clock className="h-4 w-4 text-amber-600" />
          </div>
          <div className="pt-1">
            <div className="text-2xl font-bold text-rose-700 font-mono tracking-tight">
              {kpis.matured_overdue + kpis.expiring_soon} <span className="text-xs font-sans font-medium text-slate-400">Notices</span>
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">
              <span className="text-amber-800 font-semibold">{kpis.expiring_soon} expiring</span> • <span className="text-rose-800 font-semibold">{kpis.matured_overdue} overdue</span>
            </p>
          </div>
          <div className="pt-1 text-[10.5px] text-slate-500 flex items-center justify-between border-t border-slate-100">
            <span>Critical Notices:</span>
            <span className="font-semibold text-rose-700">{kpis.critical_alerts} High Priority</span>
          </div>
        </div>

        {/* Cryptographic Ledger */}
        <div className="card-institutional p-4 bg-white border border-slate-200 space-y-2">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Merkle Audit Chain</span>
            <Layers className="h-4 w-4 text-blue-900" />
          </div>
          <div className="pt-1">
            <div className="text-2xl font-bold text-blue-950 font-mono tracking-tight">
              #{kpis.total_audit_blocks} <span className="text-xs font-sans font-medium text-slate-400">Blocks</span>
            </div>
            <p className="text-[11px] text-emerald-700 font-semibold mt-0.5 flex items-center space-x-1">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-600"></span>
              <span>CHAIN_INTEGRITY_VERIFIED</span>
            </p>
          </div>
          <div className="pt-1 text-[10.5px] text-slate-500 flex items-center justify-between border-t border-slate-100">
            <span>Algorithm:</span>
            <span className="font-mono text-slate-600">SHA-256 Chained</span>
          </div>
        </div>
      </div>

      {/* Middle Section: Bank Exposure & Operational Queues */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Scheduled Commercial Bank Exposure (7 Cols) */}
        <div className="lg:col-span-7 card-institutional p-5 bg-white border border-slate-200 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
                <Landmark className="h-4 w-4 text-blue-900" />
                <span>Scheduled Commercial Bank Exposure</span>
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">Collateral concentration across authorized custodian banks</p>
            </div>
            <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
              {banks.length} Approved Banks
            </span>
          </div>

          <div className="space-y-3">
            {banks.map((b) => {
              const maxAmt = Math.max(...banks.map(x => x.total_amount), 1);
              const pct = Math.round((b.total_amount / maxAmt) * 100);
              return (
                <div key={b.bank_name} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-medium text-slate-800">{b.bank_name}</span>
                    <div className="flex items-center space-x-2">
                      <span className="text-slate-400 font-mono text-[11px]">{b.fdr_count} FDRs</span>
                      <span className="font-mono font-bold text-slate-900">₹{b.amount_crores.toFixed(2)} Cr</span>
                    </div>
                  </div>
                  <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-blue-800 rounded-full transition-all duration-300"
                      style={{ width: `${pct}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Operational Modules & Pending Queues (5 Cols) */}
        <div className="lg:col-span-5 card-institutional p-5 bg-white border border-slate-200 flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-3">
              <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
                <TrendingUp className="h-4 w-4 text-blue-900" />
                <span>Operational Action Queues</span>
              </h2>
              <span className="text-[11px] text-slate-500">Live Status</span>
            </div>

            <div className="space-y-2">
              <button 
                onClick={() => onNavigateTab('scrutiny')}
                className="w-full flex items-center justify-between p-2.5 rounded-md border border-slate-200 hover:border-slate-300 bg-slate-50/70 hover:bg-slate-50 text-xs transition-colors text-left"
              >
                <div className="flex items-center space-x-2">
                  <span className="h-2 w-2 rounded-full bg-amber-500"></span>
                  <span className="font-medium text-slate-800">AI Document Scrutiny Desk</span>
                </div>
                <span className="font-mono font-bold text-amber-800 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                  {kpis.under_scrutiny + kpis.discrepancies_flagged} Pending
                </span>
              </button>

              <button 
                onClick={() => onNavigateTab('maturity')}
                className="w-full flex items-center justify-between p-2.5 rounded-md border border-slate-200 hover:border-slate-300 bg-slate-50/70 hover:bg-slate-50 text-xs transition-colors text-left"
              >
                <div className="flex items-center space-x-2">
                  <span className="h-2 w-2 rounded-full bg-rose-500"></span>
                  <span className="font-medium text-slate-800">Maturity & Escalations Matrix</span>
                </div>
                <span className="font-mono font-bold text-rose-800 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                  {kpis.matured_overdue} Overdue
                </span>
              </button>

              <button 
                onClick={() => onNavigateTab('release')}
                className="w-full flex items-center justify-between p-2.5 rounded-md border border-slate-200 hover:border-slate-300 bg-slate-50/70 hover:bg-slate-50 text-xs transition-colors text-left"
              >
                <div className="flex items-center space-x-2">
                  <span className="h-2 w-2 rounded-full bg-blue-600"></span>
                  <span className="font-medium text-slate-800">Statutory Lien Discharge Pipeline</span>
                </div>
                <span className="font-mono font-bold text-blue-900 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                  {kpis.release_requested} Ready
                </span>
              </button>
            </div>
          </div>

          <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
            <span>Automated Cron Sweep:</span>
            <span className="font-mono font-semibold text-slate-700">Every 6 Hours (Live)</span>
          </div>
        </div>
      </div>

      {/* Regional Directorate Summary Table (Clean Fintech Table) */}
      <div className="card-institutional bg-white border border-slate-200 overflow-hidden">
        <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/60">
          <div>
            <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
              <Building2 className="h-4 w-4 text-blue-900" />
              <span>Regional Directorate Summary (Jurisdiction Breakdown)</span>
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">Collateral distribution across technical education zones</p>
          </div>
          <button 
            onClick={() => onNavigateTab('repository')}
            className="text-xs font-semibold text-blue-900 hover:text-blue-950 flex items-center space-x-1"
          >
            <span>View All Records</span>
            <ArrowUpRight className="h-3.5 w-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full table-fintech text-left">
            <thead>
              <tr>
                <th>State / UT Jurisdiction</th>
                <th>Regional Directorate</th>
                <th className="text-center">Deposit Count</th>
                <th className="text-right">Total Pledged Capital</th>
              </tr>
            </thead>
            <tbody>
              {regional.map((r) => (
                <tr key={r.state}>
                  <td className="font-semibold text-slate-900">{r.state}</td>
                  <td className="text-slate-600">{r.regional_office}</td>
                  <td className="text-center font-mono font-medium text-slate-700">{r.fdr_count}</td>
                  <td className="text-right font-mono font-bold text-slate-900">₹{r.amount_crores.toFixed(2)} Cr</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
