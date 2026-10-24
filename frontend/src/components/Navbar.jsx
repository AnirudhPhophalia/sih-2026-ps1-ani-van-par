import React, { useState } from 'react';
import { 
  ShieldCheck, Landmark, Building2, Bell, CheckCircle2, 
  ChevronDown, RefreshCw, UserCheck, AlertTriangle, KeyRound
} from 'lucide-react';

export const PERSONAS = [
  {
    role: "INSTITUTION_ADMIN",
    title: "Institution Admin",
    name: "Dr. R. K. Saxena",
    desc: "Principal / Trust Secretary",
    badge: "bg-blue-50 text-blue-700 border-blue-200"
  },
  {
    role: "SCRUTINY_OFFICER",
    title: "Scrutiny Officer",
    name: "Smt. Sunita Rao",
    desc: "AICTE Regulation Bureau Desk",
    badge: "bg-emerald-50 text-emerald-700 border-emerald-200"
  },
  {
    role: "REGIONAL_OFFICER",
    title: "Regional Officer (RO)",
    name: "Dr. R. K. Verma",
    desc: "Head of Regional Directorate (NWRO)",
    badge: "bg-indigo-50 text-indigo-700 border-indigo-200"
  },
  {
    role: "BUREAU_CHIEF",
    title: "Bureau Chief / Member Sec.",
    name: "Prof. Rajive Kumar",
    desc: "Competent Authority (Authorizer)",
    badge: "bg-amber-50 text-amber-700 border-amber-200"
  },
  {
    role: "BANK_AUDITOR",
    title: "Bank Branch Manager",
    name: "Shri Amit Kapoor",
    desc: "Authorized Bank Signatory (SBI)",
    badge: "bg-cyan-50 text-cyan-700 border-cyan-200"
  },
  {
    role: "CISO_AUDITOR",
    title: "System Auditor & CISO",
    name: "Dr. Arvind Swaminathan",
    desc: "Vigilance & Cryptographic Audit",
    badge: "bg-purple-50 text-purple-700 border-purple-200"
  }
];

export default function Navbar({ 
  currentPersona, 
  setCurrentPersona, 
  activeTab, 
  setActiveTab,
  unresolvedAlertsCount,
  onOpenAlerts,
  onOpenNewFDR
}) {
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const activePersonaObj = PERSONAS.find(p => p.role === currentPersona) || PERSONAS[0];

  const navItems = [
    { id: 'dashboard', label: 'Executive Dashboard', icon: Landmark },
    { id: 'repository', label: 'FDR Repository', icon: Building2 },
    { id: 'scrutiny', label: 'AI Scrutiny Desk', icon: ShieldCheck },
    { id: 'bank-gateway', label: 'Bank Gateway', icon: KeyRound },
    { id: 'maturity', label: 'Maturity & Escalations', icon: AlertTriangle },
    { id: 'release', label: 'Release Workflow', icon: CheckCircle2 },
    { id: 'audit', label: 'Cryptographic Ledger', icon: RefreshCw },
  ];

  return (
    <header className="sticky top-0 z-40 w-full bg-white border-b border-slate-200 shadow-xs">
      {/* Indian National Tricolor Bar */}
      <div className="tricolor-strip w-full"></div>

      {/* Top Banner / Govt Header */}
      <div className="border-b border-slate-100 bg-slate-50/80 px-4 py-1.5 text-xs text-slate-600">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="flex h-2 w-2 rounded-full bg-emerald-600 animate-pulse"></span>
            <span className="font-semibold text-slate-800">भारत सरकार | Government of India</span>
            <span className="text-slate-300">|</span>
            <span className="hidden sm:inline font-medium text-slate-700">शिक्षा मंत्रालय • Ministry of Education</span>
            <span className="text-slate-300 hidden sm:inline">|</span>
            <span className="rounded bg-amber-100 px-2 py-0.5 text-[10px] font-bold text-amber-800 border border-amber-200">
              AICTE ZERO-TRUST STATUTORY REPOSITORY
            </span>
          </div>

          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center space-x-1.5 text-slate-600">
              <span className="text-[11px]">Ledger Integrity:</span>
              <span className="font-mono text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 text-[10px]">
                MERKLE_CHAIN_VALID
              </span>
            </div>
            
            <button
              onClick={() => onOpenNewFDR()}
              className="rounded-lg bg-amber-600 hover:bg-amber-700 px-3 py-1 text-xs font-semibold text-white shadow-xs transition"
            >
              + Pledge New FDR
            </button>
          </div>
        </div>
      </div>

      {/* Main Bar */}
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        {/* Brand */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-slate-900 to-indigo-950 shadow-sm border border-slate-800 text-amber-400">
            <Landmark className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-lg font-black tracking-tight text-slate-900">
                AICTE <span className="text-amber-600 font-extrabold">FDR-PORTAL</span>
              </span>
              <span className="rounded bg-slate-100 px-1.5 py-0.5 text-[10px] font-mono font-bold text-slate-700 border border-slate-200">
                v2.0
              </span>
            </div>
            <p className="text-[11px] text-slate-500 font-medium leading-none mt-0.5">
              All India Council for Technical Education • Security Deposit Lifecycle Portal
            </p>
          </div>
        </div>

        {/* Persona Switcher & Alerts */}
        <div className="flex items-center space-x-3">
          {/* Alert Notification Trigger */}
          <button 
            onClick={onOpenAlerts}
            className="relative flex h-9 w-9 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-600 hover:text-slate-900 hover:border-slate-300 hover:bg-slate-50 shadow-xs transition"
            title="Maturity & Escalation Alerts"
          >
            <Bell className="h-4 w-4" />
            {unresolvedAlertsCount > 0 && (
              <span className="absolute -top-1 -right-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-rose-600 px-1 text-[10px] font-bold text-white shadow-xs">
                {unresolvedAlertsCount}
              </span>
            )}
          </button>

          {/* Role Switcher Menu */}
          <div className="relative">
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="flex items-center space-x-2.5 rounded-xl border border-slate-200 bg-white px-3 py-1.5 text-left text-xs shadow-xs hover:border-slate-300 hover:bg-slate-50 transition"
            >
              <div className="h-7 w-7 rounded-full bg-gradient-to-tr from-amber-500 to-indigo-600 flex items-center justify-center font-bold text-white text-xs shadow-xs">
                {activePersonaObj.name[0]}
              </div>
              <div className="hidden sm:block">
                <div className="font-semibold text-slate-800 leading-tight">{activePersonaObj.name}</div>
                <div className="text-[10px] font-medium text-amber-700">{activePersonaObj.title}</div>
              </div>
              <ChevronDown className="h-3.5 w-3.5 text-slate-400" />
            </button>

            {dropdownOpen && (
              <div className="absolute right-0 mt-2 w-72 rounded-xl border border-slate-200 bg-white p-2 shadow-xl z-50">
                <div className="px-2 py-1.5 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                  Switch Role Persona (Demo)
                </div>
                <div className="space-y-1">
                  {PERSONAS.map(p => (
                    <button
                      key={p.role}
                      onClick={() => {
                        setCurrentPersona(p.role);
                        setDropdownOpen(false);
                      }}
                      className={`w-full flex items-start space-x-2.5 rounded-lg p-2 text-left transition ${
                        currentPersona === p.role 
                          ? 'bg-amber-50 border border-amber-200 text-amber-900' 
                          : 'hover:bg-slate-50 text-slate-700'
                      }`}
                    >
                      <UserCheck className={`h-4 w-4 mt-0.5 ${currentPersona === p.role ? 'text-amber-600' : 'text-slate-400'}`} />
                      <div className="flex-1">
                        <div className="text-xs font-bold text-slate-900">{p.title}</div>
                        <div className="text-[11px] text-slate-600">{p.name}</div>
                        <div className="text-[10px] text-slate-400">{p.desc}</div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="border-t border-slate-200 bg-slate-50/60 px-4">
        <div className="mx-auto flex max-w-7xl space-x-1.5 overflow-x-auto py-1.5">
          {navItems.map(item => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-2 whitespace-nowrap rounded-lg px-3 py-2 text-xs font-medium transition ${
                  isActive
                    ? 'bg-white text-slate-900 border border-slate-300 font-bold shadow-xs'
                    : 'text-slate-600 hover:bg-white hover:text-slate-900'
                }`}
              >
                <Icon className={`h-3.5 w-3.5 ${isActive ? 'text-amber-600' : 'text-slate-500'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}
