import React, { useState } from 'react';
import { 
  LayoutDashboard, FolderKey, ShieldCheck, Landmark, 
  Clock, FileCheck, Layers, ChevronRight, UserCheck, 
  Plus, Bell, ChevronDown, CheckCircle2, Shield, Building2
} from 'lucide-react';

export const PERSONAS = [
  {
    role: "SCRUTINY_OFFICER",
    title: "Scrutiny Officer",
    name: "Smt. Sunita Rao",
    department: "Regulation Bureau, New Delhi",
    initials: "SR",
    badgeColor: "bg-blue-900 text-white"
  },
  {
    role: "INSTITUTION_ADMIN",
    title: "Institution Admin",
    name: "Dr. R. K. Saxena",
    department: "Principal / Trust Secretary",
    initials: "RS",
    badgeColor: "bg-slate-800 text-white"
  },
  {
    role: "REGIONAL_OFFICER",
    title: "Regional Officer (RO)",
    name: "Dr. R. K. Verma",
    department: "Directorate (NWRO)",
    initials: "RV",
    badgeColor: "bg-blue-800 text-white"
  },
  {
    role: "BUREAU_CHIEF",
    title: "Bureau Chief (Authorizer)",
    name: "Prof. Rajive Kumar",
    department: "Member Secretary / Directorate",
    initials: "RK",
    badgeColor: "bg-indigo-900 text-white"
  },
  {
    role: "BANK_AUDITOR",
    title: "Bank Branch Manager",
    name: "Shri Amit Kapoor",
    department: "Chief Manager, State Bank of India",
    initials: "AK",
    badgeColor: "bg-slate-700 text-white"
  },
  {
    role: "CISO_AUDITOR",
    title: "Vigilance & CISO Auditor",
    name: "Dr. Arvind Swaminathan",
    department: "Cryptographic Audit Cell",
    initials: "AS",
    badgeColor: "bg-slate-900 text-white"
  }
];

export default function Sidebar({ 
  currentPersona, 
  setCurrentPersona, 
  activeTab, 
  setActiveTab,
  unresolvedAlertsCount,
  onOpenAlerts,
  onOpenNewFDR
}) {
  const [personaOpen, setPersonaOpen] = useState(false);
  const activePersonaObj = PERSONAS.find(p => p.role === currentPersona) || PERSONAS[0];

  const navItems = [
    { id: 'dashboard', label: 'Executive Dashboard', icon: LayoutDashboard },
    { id: 'repository', label: 'FDR Repository', icon: FolderKey },
    { id: 'scrutiny', label: 'Forensic Scrutiny', icon: ShieldCheck, badge: 'AI-OCR' },
    { id: 'bank-gateway', label: 'Bank CBS Gateway', icon: Landmark },
    { id: 'maturity', label: 'Maturity Tracking', icon: Clock },
    { id: 'release', label: 'Release Workflow', icon: FileCheck },
    { id: 'audit', label: 'Audit Ledger', icon: Layers },
  ];

  return (
    <aside className="w-60 shrink-0 bg-white border-r border-slate-200 flex flex-col justify-between min-h-screen select-none sticky top-0 h-screen z-30 shadow-[1px_0_2px_rgba(0,0,0,0.02)]">
      {/* Top Branding Section */}
      <div>
        {/* Emblem & Title */}
        <div className="p-4 border-b border-slate-200">
          <div className="flex items-center space-x-2.5 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="h-9 w-9 rounded-md bg-blue-950 flex items-center justify-center text-amber-400 shadow-xs border border-blue-900">
              <Shield className="h-4 w-4" />
            </div>
            <div>
              <div className="flex items-center space-x-1.5">
                <span className="font-extrabold tracking-tight text-blue-950 text-sm">AICTE</span>
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">COLLATERAL</span>
              </div>
              <p className="text-[10.5px] text-slate-500 font-medium">Security Deposit Portal</p>
            </div>
          </div>
        </div>

        {/* Primary Action Button */}
        <div className="p-3">
          <button
            onClick={onOpenNewFDR}
            className="w-full flex items-center justify-center space-x-1.5 py-2 px-3 rounded-md bg-blue-900 hover:bg-blue-950 text-white text-xs font-semibold shadow-xs transition-colors duration-150"
          >
            <Plus className="h-3.5 w-3.5" />
            <span>Pledge New FDR</span>
          </button>
        </div>

        {/* Navigation Links */}
        <nav className="px-2 space-y-0.5">
          <div className="px-2 py-1 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
            Regulatory Modules
          </div>

          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-2.5 py-2 rounded-md text-xs font-medium transition-colors duration-150 group ${
                  isActive
                    ? 'bg-blue-50/90 text-blue-950 font-bold border-l-2 border-blue-900 shadow-2xs'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <div className="flex items-center space-x-2.5">
                  <Icon className={`h-4 w-4 shrink-0 transition-colors ${isActive ? 'text-blue-900' : 'text-slate-400 group-hover:text-slate-600'}`} />
                  <span className="truncate">{item.label}</span>
                </div>

                {item.badge && (
                  <span className={`text-[9.5px] font-bold px-1.5 py-0.2 rounded ${
                    isActive ? 'bg-blue-200 text-blue-950' : 'bg-slate-100 text-slate-500'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Section: Persona Card & Status */}
      <div className="p-3 border-t border-slate-200 space-y-2 bg-slate-50/60">
        {/* Alerts Button */}
        <button
          onClick={onOpenAlerts}
          className="w-full flex items-center justify-between px-2.5 py-1.5 rounded-md border border-slate-200 bg-white hover:bg-slate-50 text-xs text-slate-700 transition-colors"
        >
          <div className="flex items-center space-x-2">
            <Bell className="h-3.5 w-3.5 text-slate-500" />
            <span className="font-medium text-[11.5px]">Maturity Notices</span>
          </div>
          {unresolvedAlertsCount > 0 ? (
            <span className="h-4 min-w-4 rounded-full bg-rose-600 text-white font-bold text-[9px] flex items-center justify-center px-1">
              {unresolvedAlertsCount}
            </span>
          ) : (
            <span className="text-[10px] text-slate-400">0 Active</span>
          )}
        </button>

        {/* Persona Switcher */}
        <div className="relative">
          <button
            onClick={() => setPersonaOpen(!personaOpen)}
            className="w-full flex items-center justify-between p-2 rounded-md border border-slate-200 bg-white hover:border-slate-300 transition-colors text-left"
          >
            <div className="flex items-center space-x-2 truncate">
              <div className={`h-6 w-6 rounded ${activePersonaObj.badgeColor} font-bold text-[10px] flex items-center justify-center shrink-0`}>
                {activePersonaObj.initials}
              </div>
              <div className="truncate">
                <div className="text-[11px] font-bold text-slate-900 truncate leading-tight">{activePersonaObj.name}</div>
                <div className="text-[9.5px] text-slate-500 truncate">{activePersonaObj.title}</div>
              </div>
            </div>
            <ChevronDown className="h-3.5 w-3.5 text-slate-400 shrink-0 ml-1" />
          </button>

          {personaOpen && (
            <div className="absolute bottom-full left-0 mb-1.5 w-72 rounded-md border border-slate-200 bg-white p-2 shadow-lg z-50 animate-modal">
              <div className="px-2 py-1 text-[9.5px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-100 mb-1">
                Role Persona Switcher
              </div>
              <div className="space-y-0.5 max-h-60 overflow-y-auto pr-1">
                {PERSONAS.map(p => (
                  <button
                    key={p.role}
                    onClick={() => {
                      setCurrentPersona(p.role);
                      setPersonaOpen(false);
                    }}
                    className={`w-full flex items-start space-x-2 p-1.5 rounded text-left text-xs transition-colors ${
                      currentPersona === p.role 
                        ? 'bg-blue-50 text-blue-950 font-semibold' 
                        : 'hover:bg-slate-50 text-slate-700'
                    }`}
                  >
                    <div className={`h-5 w-5 rounded ${p.badgeColor} font-bold text-[9px] flex items-center justify-center shrink-0 mt-0.5`}>
                      {p.initials}
                    </div>
                    <div className="flex-1 truncate">
                      <div className="font-bold text-slate-900 truncate text-[11px]">{p.title}</div>
                      <div className="text-[10px] text-slate-500 truncate">{p.name} • {p.department}</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Security & Cryptographic Stamp */}
        <div className="flex items-center justify-between px-1 text-[9.5px] text-slate-400">
          <span className="flex items-center space-x-1">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-600"></span>
            <span className="font-medium text-slate-600">SHA-256 Verified</span>
          </span>
          <span className="font-mono text-slate-400">Govt. of India</span>
        </div>
      </div>
    </aside>
  );
}
