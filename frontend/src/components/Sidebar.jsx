import React, { useState } from 'react';
import { 
  LayoutDashboard, FolderKey, ShieldCheck, Landmark, 
  Clock, FileCheck, Layers, ChevronRight, UserCheck, 
  Plus, Bell, ChevronDown, CheckCircle2, Shield
} from 'lucide-react';

export const PERSONAS = [
  {
    role: "SCRUTINY_OFFICER",
    title: "Scrutiny Officer",
    name: "Smt. Sunita Rao",
    department: "Regulation Bureau",
    initials: "SR",
    badgeColor: "bg-slate-700 text-white"
  },
  {
    role: "INSTITUTION_ADMIN",
    title: "Institution Admin",
    name: "Dr. R. K. Saxena",
    department: "Principal / Trust Secretary",
    initials: "RS",
    badgeColor: "bg-slate-600 text-white"
  },
  {
    role: "REGIONAL_OFFICER",
    title: "Regional Officer",
    name: "Dr. R. K. Verma",
    department: "Directorate (NWRO)",
    initials: "RV",
    badgeColor: "bg-slate-700 text-white"
  },
  {
    role: "BUREAU_CHIEF",
    title: "Bureau Chief",
    name: "Prof. Rajive Kumar",
    department: "Member Secretary",
    initials: "RK",
    badgeColor: "bg-slate-800 text-white"
  },
  {
    role: "BANK_AUDITOR",
    title: "Branch Manager",
    name: "Shri Amit Kapoor",
    department: "State Bank of India",
    initials: "AK",
    badgeColor: "bg-slate-600 text-white"
  },
  {
    role: "CISO_AUDITOR",
    title: "Vigilance Lead",
    name: "Dr. Arvind Swaminathan",
    department: "Cryptographic Cell",
    initials: "AS",
    badgeColor: "bg-slate-700 text-white"
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
    { id: 'scrutiny', label: 'Forensic Scrutiny', icon: ShieldCheck, badge: 'AI' },
    { id: 'bank-gateway', label: 'Bank CBS Gateway', icon: Landmark },
    { id: 'maturity', label: 'Maturity Tracking', icon: Clock },
    { id: 'release', label: 'Release Workflow', icon: FileCheck },
    { id: 'audit', label: 'Audit Ledger', icon: Layers },
  ];

  return (
    <aside className="w-56 shrink-0 bg-white border-r border-slate-200/80 flex flex-col justify-between min-h-screen select-none sticky top-0 h-screen z-30">
      {/* Top Branding Section */}
      <div>
        {/* Emblem & Title */}
        <div className="p-3.5 border-b border-slate-100">
          <div className="flex items-center space-x-2.5 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="h-8 w-8 rounded bg-slate-800 flex items-center justify-center text-slate-200">
              <Shield className="h-4 w-4" />
            </div>
            <div>
              <div className="flex items-center space-x-1">
                <span className="font-bold tracking-tight text-slate-800 text-xs">AICTE</span>
                <span className="text-[9.5px] font-medium text-slate-400 uppercase tracking-wider">REGISTRY</span>
              </div>
              <p className="text-[10px] text-slate-400">Collateral Management</p>
            </div>
          </div>
        </div>

        {/* Primary Action Button - Calmer, Softer */}
        <div className="p-2.5">
          <button
            onClick={onOpenNewFDR}
            className="w-full flex items-center justify-center space-x-1.5 py-1.5 px-3 rounded bg-slate-800 hover:bg-slate-900 text-white text-xs font-medium transition-colors"
          >
            <Plus className="h-3.5 w-3.5 text-slate-300" />
            <span>Pledge New FDR</span>
          </button>
        </div>

        {/* Navigation Links */}
        <nav className="px-2 space-y-0.5">
          <div className="px-2 py-1 text-[9.5px] font-semibold text-slate-400 uppercase tracking-wider">
            Modules
          </div>

          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded text-xs transition-colors group ${
                  isActive
                    ? 'bg-slate-100 text-slate-900 font-semibold border-l-2 border-slate-700'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50/80 font-normal'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <Icon className={`h-3.5 w-3.5 shrink-0 transition-colors ${isActive ? 'text-slate-800' : 'text-slate-400 group-hover:text-slate-600'}`} />
                  <span className="truncate text-[11.5px]">{item.label}</span>
                </div>

                {item.badge && (
                  <span className={`text-[9px] font-medium px-1 py-0.2 rounded ${
                    isActive ? 'bg-slate-200 text-slate-800' : 'bg-slate-100 text-slate-500'
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
      <div className="p-2.5 border-t border-slate-100 space-y-1.5 bg-slate-50/40">
        {/* Alerts Button */}
        <button
          onClick={onOpenAlerts}
          className="w-full flex items-center justify-between px-2 py-1.5 rounded border border-slate-200/80 bg-white hover:bg-slate-50 text-xs text-slate-600 transition-colors"
        >
          <div className="flex items-center space-x-1.5">
            <Bell className="h-3 w-3 text-slate-400" />
            <span className="text-[11px]">Maturity Notices</span>
          </div>
          {unresolvedAlertsCount > 0 ? (
            <span className="h-3.5 min-w-3.5 rounded-full bg-rose-500 text-white font-bold text-[8.5px] flex items-center justify-center px-1">
              {unresolvedAlertsCount}
            </span>
          ) : (
            <span className="text-[9.5px] text-slate-400">0</span>
          )}
        </button>

        {/* Persona Switcher */}
        <div className="relative">
          <button
            onClick={() => setPersonaOpen(!personaOpen)}
            className="w-full flex items-center justify-between p-1.5 rounded border border-slate-200/80 bg-white hover:border-slate-300 transition-colors text-left"
          >
            <div className="flex items-center space-x-1.5 truncate">
              <div className={`h-5 w-5 rounded ${activePersonaObj.badgeColor} font-semibold text-[9px] flex items-center justify-center shrink-0`}>
                {activePersonaObj.initials}
              </div>
              <div className="truncate">
                <div className="text-[10.5px] font-semibold text-slate-700 truncate leading-tight">{activePersonaObj.name}</div>
                <div className="text-[9px] text-slate-400 truncate">{activePersonaObj.title}</div>
              </div>
            </div>
            <ChevronDown className="h-3 w-3 text-slate-400 shrink-0 ml-1" />
          </button>

          {personaOpen && (
            <div className="absolute bottom-full left-0 mb-1 w-64 rounded border border-slate-200 bg-white p-1.5 shadow-md z-50 animate-modal">
              <div className="px-1.5 py-0.5 text-[9px] font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-100 mb-1">
                Select Role Persona
              </div>
              <div className="space-y-0.5 max-h-52 overflow-y-auto">
                {PERSONAS.map(p => (
                  <button
                    key={p.role}
                    onClick={() => {
                      setCurrentPersona(p.role);
                      setPersonaOpen(false);
                    }}
                    className={`w-full flex items-start space-x-2 p-1.5 rounded text-left text-xs transition-colors ${
                      currentPersona === p.role 
                        ? 'bg-slate-100 text-slate-900 font-semibold' 
                        : 'hover:bg-slate-50 text-slate-600'
                    }`}
                  >
                    <div className={`h-4.5 w-4.5 rounded ${p.badgeColor} font-semibold text-[8.5px] flex items-center justify-center shrink-0 mt-0.5`}>
                      {p.initials}
                    </div>
                    <div className="flex-1 truncate">
                      <div className="font-semibold text-slate-800 truncate text-[10.5px]">{p.title}</div>
                      <div className="text-[9.5px] text-slate-400 truncate">{p.name}</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Security Stamp */}
        <div className="flex items-center justify-between px-1 text-[9px] text-slate-400">
          <span className="flex items-center space-x-1">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
            <span>Zero-Trust Linked</span>
          </span>
          <span className="font-mono">Govt. of India</span>
        </div>
      </div>
    </aside>
  );
}
