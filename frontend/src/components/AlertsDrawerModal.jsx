import React from 'react';
import { X, Bell, AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

export default function AlertsDrawerModal({ isOpen, onClose, alerts, onResolveAlert }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-end bg-slate-900/40 backdrop-blur-xs">
      <div className="bg-white h-full w-full max-w-md border-l border-slate-300 p-5 flex flex-col justify-between shadow-2xl overflow-y-auto animate-modal">
        <div className="space-y-4">
          <div className="flex items-center justify-between border-b border-slate-200 pb-2.5">
            <div className="flex items-center space-x-2">
              <Bell className="h-4 w-4 text-blue-900" />
              <h2 className="text-sm font-bold text-slate-900">Statutory Notifications & Escalations</h2>
            </div>
            <button onClick={onClose} className="rounded p-1 text-slate-400 hover:text-slate-700 transition-colors">
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="space-y-2 max-h-[82vh] overflow-y-auto pr-1">
            {(!alerts || alerts.length === 0) ? (
              <div className="py-16 text-center text-xs text-slate-500">
                All statutory alerts have been acknowledged.
              </div>
            ) : (
              alerts.map((alert) => (
                <div
                  key={alert.id}
                  className={`p-3 rounded-md border text-xs space-y-1.5 ${
                    alert.severity === 'CRITICAL' || alert.severity === 'ESCALATION'
                      ? 'bg-rose-50/70 border-rose-200 text-rose-950'
                      : alert.severity === 'WARNING'
                      ? 'bg-amber-50/70 border-amber-200 text-amber-950'
                      : 'bg-slate-50 border-slate-200 text-slate-800'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className={`px-1.5 py-0.2 rounded text-[9.5px] font-bold ${
                      alert.severity === 'ESCALATION'
                        ? 'bg-rose-700 text-white'
                        : alert.severity === 'CRITICAL'
                        ? 'bg-rose-100 text-rose-900 border border-rose-200'
                        : 'bg-amber-100 text-amber-900 border border-amber-200'
                    }`}>
                      {alert.severity} • TIER {alert.escalation_tier}
                    </span>
                    <span className="font-mono text-[10px] text-slate-500">
                      {new Date(alert.created_at).toLocaleDateString()}
                    </span>
                  </div>

                  <div className="font-bold text-slate-900 text-xs">{alert.fdr_number} ({alert.institution_name})</div>
                  <p className="text-[11px] text-slate-700 leading-normal">{alert.message}</p>

                  <div className="flex items-center justify-between pt-1 border-t border-slate-200/60">
                    <span className="text-[10px] text-slate-500 font-mono">
                      Channels: {(alert.channels_sent || []).join(', ')}
                    </span>
                    {!alert.is_resolved && (
                      <button
                        onClick={() => onResolveAlert?.(alert.id)}
                        className="rounded bg-white border border-slate-300 hover:bg-slate-50 px-2 py-0.5 text-[10.5px] font-medium text-slate-700 transition-colors"
                      >
                        Acknowledge
                      </button>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        <button
          onClick={onClose}
          className="w-full mt-3 py-1.5 rounded-md bg-slate-100 text-slate-700 text-xs font-semibold hover:bg-slate-200 transition-colors"
        >
          Close Drawer
        </button>
      </div>
    </div>
  );
}
