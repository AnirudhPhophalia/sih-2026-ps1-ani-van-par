import React from 'react';
import { Bell, Shield, ChevronRight, Calendar, Landmark } from 'lucide-react';

const TAB_TITLES = {
  dashboard: { title: "Executive Collateral Dashboard", code: "MOD-01", desc: "National Technical Education Statutory Deposit Custody" },
  repository: { title: "Centralized FDR Repository", code: "MOD-02", desc: "Statutory Fixed Deposit Collateral & Document Ledger" },
  scrutiny: { title: "Forensic Document Scrutiny Desk", code: "MOD-03", desc: "Automated OCR Extraction, ELA Forensics & Discrepancy Matrix" },
  'bank-gateway': { title: "Tri-Modal Bank Gateway", code: "MOD-04", desc: "Core Banking System (CBS) SFMS & NeSL Information Utility" },
  maturity: { title: "Validity & Maturity Matrix", code: "MOD-05", desc: "Statutory Lock-in Milestones & Multi-Tier Escalations" },
  release: { title: "Statutory Lien Discharge", code: "MOD-06", desc: "Maker-Checker-Authorizer Workflow with Aadhaar e-Sign" },
  audit: { title: "Cryptographic Audit Ledger", code: "MOD-07", desc: "Tamper-Evident SHA-256 Merkle Chaining & Forensic Log" },
};

export default function Header({ activeTab, unresolvedAlertsCount, onOpenAlerts, activePersonaObj }) {
  const current = TAB_TITLES[activeTab] || { title: "AICTE Portal", code: "MOD-00", desc: "" };

  return (
    <header className="sticky top-0 z-20 bg-white/95 backdrop-blur-xs border-b border-slate-200 px-6 py-3 flex items-center justify-between">
      {/* Indian national tricolor strip: thin, 2.5px */}
      <div className="absolute top-0 left-0 right-0 tricolor-strip"></div>

      {/* Page Title & Breadcrumb */}
      <div>
        <div className="flex items-center space-x-2 text-[10.5px] text-slate-500 font-medium">
          <span className="text-slate-600 font-semibold">AICTE Statutory Portal</span>
          <ChevronRight className="h-3 w-3 text-slate-400" />
          <span className="font-mono text-slate-400">{current.code}</span>
          <ChevronRight className="h-3 w-3 text-slate-400" />
          <span className="text-blue-900 font-bold capitalize">{activeTab.replace('-', ' ')}</span>
        </div>
        <h1 className="text-base md:text-lg font-bold text-slate-900 tracking-tight mt-0.5">
          {current.title}
        </h1>
      </div>

      {/* Right Controls */}
      <div className="flex items-center space-x-2.5">
        {/* Session / Fiscal Pill */}
        <div className="hidden lg:flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-slate-50 border border-slate-200 text-[11px] text-slate-600">
          <Calendar className="h-3.5 w-3.5 text-slate-400" />
          <span className="font-medium">FY 2024–25 (Q3)</span>
        </div>

        {/* Ministry Badge */}
        <div className="hidden sm:flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-slate-50 border border-slate-200 text-[11px] font-medium text-slate-700">
          <Landmark className="h-3.5 w-3.5 text-blue-900" />
          <span>Govt. of India</span>
        </div>

        {/* Notifications Button */}
        <button
          onClick={onOpenAlerts}
          className="relative flex h-8 w-8 items-center justify-center rounded-md border border-slate-200 bg-white hover:bg-slate-50 text-slate-600 hover:text-slate-900 transition-colors"
          title="Statutory Notices"
        >
          <Bell className="h-4 w-4" />
          {unresolvedAlertsCount > 0 && (
            <span className="absolute -top-1 -right-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-rose-600 px-1 text-[9px] font-bold text-white">
              {unresolvedAlertsCount}
            </span>
          )}
        </button>
      </div>
    </header>
  );
}
