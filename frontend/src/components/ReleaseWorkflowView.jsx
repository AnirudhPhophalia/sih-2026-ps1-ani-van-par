import React, { useState, useEffect } from 'react';
import { 
  CheckCircle2, FileText, Download, ShieldCheck, UserCheck, 
  ArrowRight, Key, AlertCircle, RefreshCw, X, FileCheck, Check
} from 'lucide-react';

export default function ReleaseWorkflowView({ onRefreshAll }) {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedReq, setSelectedReq] = useState(null);

  const [makerComments, setMakerComments] = useState('Lock-in period of 10 years fulfilled. Verified zero outstanding fee complaints or court cases.');
  const [roComments, setRoComments] = useState('Regional office concurs with scrutiny. Bank lien confirmed clear for discharge.');
  const [esignPin, setEsignPin] = useState('123456');
  const [actionLoading, setActionLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null);

  const fetchRequests = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/release/requests');
      if (res.ok) {
        const data = await res.json();
        setRequests(data.requests || []);
        if (data.requests?.length > 0 && !selectedReq) {
          setSelectedReq(data.requests[0]);
        }
      }
    } catch (err) {
      console.error("Failed to load release requests:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRequests();
  }, []);

  const handleMakerSubmit = async (reqId, approve) => {
    setActionLoading(true);
    try {
      const res = await fetch(`/api/release/${reqId}/scrutiny`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          officer_name: "Smt. Sunita Rao (Scrutiny Officer)",
          is_approved: approve,
          comments: makerComments
        })
      });
      if (res.ok) {
        setStatusMessage("Tier 1 Scrutiny Officer decision submitted.");
        fetchRequests();
        onRefreshAll?.();
      }
    } catch (err) {
      console.error("Maker submit failed:", err);
    } finally {
      setActionLoading(false);
    }
  };

  const handleCheckerSubmit = async (reqId, approve) => {
    setActionLoading(true);
    try {
      const res = await fetch(`/api/release/${reqId}/ro-approval`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ro_name: "Dr. R. K. Verma (Regional Officer NWRO)",
          is_approved: approve,
          comments: roComments
        })
      });
      if (res.ok) {
        setStatusMessage("Tier 2 Regional Director administrative concurrence recorded.");
        fetchRequests();
        onRefreshAll?.();
      }
    } catch (err) {
      console.error("Checker submit failed:", err);
    } finally {
      setActionLoading(false);
    }
  };

  const handleAuthorizerSubmit = async (reqId) => {
    setActionLoading(true);
    try {
      const res = await fetch(`/api/release/${reqId}/authorize-esign`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          authority_name: "Prof. Rajive Kumar (Member Secretary)",
          esign_pin: esignPin
        })
      });
      if (res.ok) {
        const data = await res.json();
        setStatusMessage(`Statutory Lien Officially Discharged! AICTE NOC ${data.noc_number} Issued.`);
        fetchRequests();
        onRefreshAll?.();
      }
    } catch (err) {
      console.error("Authorizer submit failed:", err);
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="space-y-5 animate-entrance">
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-lg font-bold text-slate-900 flex items-center space-x-2">
            <FileCheck className="h-4 w-4 text-blue-900" />
            <span>Maker-Checker-Authorizer Statutory Lien Discharge Pipeline</span>
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Three-tier statutory lien discharge: Scrutiny Officer → Regional Director → Bureau Chief e-Sign
          </p>
        </div>

        <button
          onClick={fetchRequests}
          className="flex items-center space-x-1.5 rounded-md bg-white border border-slate-300 hover:bg-slate-50 px-3 py-1.5 text-xs text-slate-700 font-medium transition-colors"
        >
          <RefreshCw className={`h-3.5 w-3.5 text-slate-500 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Pipeline ({requests.length})</span>
        </button>
      </div>

      {statusMessage && (
        <div className="rounded-md border border-emerald-300 bg-emerald-50 p-3 text-xs font-semibold text-emerald-900 flex items-center space-x-2 shadow-2xs">
          <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
          <span>{statusMessage}</span>
        </div>
      )}

      {/* Main Grid: Left List (4 Cols) & Right Inspection (8 Cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Col: Requests Queue */}
        <div className="lg:col-span-4 card-institutional p-4 bg-white border border-slate-200 space-y-3">
          <div className="text-xs font-bold text-slate-800 border-b border-slate-200 pb-2">
            Active Discharge Applications
          </div>

          <div className="space-y-2 max-h-[520px] overflow-y-auto pr-1">
            {requests.length === 0 ? (
              <div className="py-12 text-center text-xs text-slate-500">
                No active release requests.
              </div>
            ) : (
              requests.map((r) => {
                const isSelected = selectedReq?.id === r.id;
                return (
                  <div
                    key={r.id}
                    onClick={() => setSelectedReq(r)}
                    className={`p-3 rounded-md border text-xs cursor-pointer transition-colors ${
                      isSelected
                        ? 'bg-blue-50/80 border-blue-900 text-slate-900 shadow-2xs'
                        : 'bg-white border-slate-200 text-slate-700 hover:border-slate-300 hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-mono font-bold text-slate-900">{r.request_number}</span>
                      <span className="text-[10px] text-slate-500 font-mono">
                        {new Date(r.created_at).toLocaleDateString()}
                      </span>
                    </div>

                    <div className="font-medium text-slate-800 truncate mt-1">
                      {r.institution?.name}
                    </div>

                    <div className="text-[10.5px] text-slate-500 flex items-center justify-between mt-1.5">
                      <span className="font-mono">FDR: {r.fdr?.fdr_number}</span>
                      <span className={`px-1.5 py-0.2 rounded text-[9.5px] font-semibold ${
                        r.status === 'RELEASED'
                          ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                          : 'bg-blue-50 text-blue-900 border border-blue-200'
                      }`}>
                        {r.status}
                      </span>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Col: Stepper & Action Controls (8 Cols) */}
        <div className="lg:col-span-8 space-y-4">
          {!selectedReq ? (
            <div className="card-institutional p-12 text-center text-xs text-slate-500 border border-slate-200">
              Select an application from the queue to process statutory discharge.
            </div>
          ) : (
            <div className="card-institutional p-5 bg-white border border-slate-200 space-y-5">
              {/* Request Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 pb-3">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-sm font-bold text-slate-900">{selectedReq.request_number}</span>
                    <span className="text-xs text-slate-500 font-medium">({selectedReq.fdr?.bank_name})</span>
                  </div>
                  <p className="text-xs text-slate-600 mt-0.5">
                    {selectedReq.institution?.name} • AICTE PID: <span className="font-mono font-medium">{selectedReq.institution?.pid}</span>
                  </p>
                </div>

                <div className="text-right">
                  <span className="text-[10px] text-slate-400 block uppercase font-medium">Pledged Principal:</span>
                  <span className="font-mono text-sm font-bold text-slate-900">
                    ₹{selectedReq.fdr?.deposit_amount?.toLocaleString('en-IN')}
                  </span>
                </div>
              </div>

              {/* 3-Tier Stepper (Government Statutory Pipeline) */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {/* Step 1: Maker */}
                <div className={`p-3 rounded border text-xs space-y-1 ${
                  selectedReq.maker_scrutiny_completed 
                    ? 'bg-emerald-50/60 border-emerald-300' 
                    : 'bg-slate-50 border-slate-200'
                }`}>
                  <div className="flex items-center justify-between font-bold text-slate-800 text-[11px]">
                    <span>1. Scrutiny Officer (Maker)</span>
                    {selectedReq.maker_scrutiny_completed ? (
                      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                    ) : (
                      <span className="h-2 w-2 rounded-full bg-slate-300"></span>
                    )}
                  </div>
                  <div className="text-[10.5px] text-slate-600">
                    {selectedReq.maker_scrutiny_completed ? (
                      <span className="text-emerald-800 font-medium">Passed by {selectedReq.maker_officer_name}</span>
                    ) : "Pending Compliance Check"}
                  </div>
                </div>

                {/* Step 2: Checker */}
                <div className={`p-3 rounded border text-xs space-y-1 ${
                  selectedReq.checker_ro_approved 
                    ? 'bg-emerald-50/60 border-emerald-300' 
                    : selectedReq.maker_scrutiny_completed 
                      ? 'bg-blue-50/60 border-blue-200' 
                      : 'bg-slate-50 border-slate-200 opacity-60'
                }`}>
                  <div className="flex items-center justify-between font-bold text-slate-800 text-[11px]">
                    <span>2. Regional Officer (Checker)</span>
                    {selectedReq.checker_ro_approved ? (
                      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                    ) : (
                      <span className="h-2 w-2 rounded-full bg-slate-300"></span>
                    )}
                  </div>
                  <div className="text-[10.5px] text-slate-600">
                    {selectedReq.checker_ro_approved ? (
                      <span className="text-emerald-800 font-medium">Concurred by {selectedReq.checker_ro_name}</span>
                    ) : selectedReq.maker_scrutiny_completed ? "Ready for RO Concurrence" : "Awaiting Maker"}
                  </div>
                </div>

                {/* Step 3: Authorizer */}
                <div className={`p-3 rounded border text-xs space-y-1 ${
                  selectedReq.authority_authorized 
                    ? 'bg-emerald-50/60 border-emerald-300' 
                    : selectedReq.checker_ro_approved 
                      ? 'bg-blue-50/60 border-blue-200' 
                      : 'bg-slate-50 border-slate-200 opacity-60'
                }`}>
                  <div className="flex items-center justify-between font-bold text-slate-800 text-[11px]">
                    <span>3. Bureau Chief (Authorizer)</span>
                    {selectedReq.authority_authorized ? (
                      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600" />
                    ) : (
                      <span className="h-2 w-2 rounded-full bg-slate-300"></span>
                    )}
                  </div>
                  <div className="text-[10.5px] text-slate-600">
                    {selectedReq.authority_authorized ? (
                      <span className="text-emerald-800 font-medium">Aadhaar e-Signed by {selectedReq.authority_name}</span>
                    ) : selectedReq.checker_ro_approved ? "Ready for e-Sign" : "Awaiting RO"}
                  </div>
                </div>
              </div>

              {/* Action Section based on Active Stage */}
              <div className="space-y-4 pt-1">
                {/* Stage 1: Maker Action */}
                {!selectedReq.maker_scrutiny_completed && (
                  <div className="p-4 rounded border border-slate-200 bg-slate-50/70 space-y-3">
                    <h4 className="text-xs font-bold text-slate-900">
                      Tier 1: Scrutiny Officer Verification & Compliance Checklist
                    </h4>
                    <p className="text-[11px] text-slate-600">
                      Verify that the statutory lock-in period (minimum 8–10 years) has concluded and no judicial stays or university complaints exist.
                    </p>
                    <textarea
                      rows={2}
                      value={makerComments}
                      onChange={(e) => setMakerComments(e.target.value)}
                      className="input-institutional text-xs py-1.5"
                    />
                    <div className="flex items-center justify-end space-x-2 pt-1">
                      <button
                        onClick={() => handleMakerSubmit(selectedReq.id, false)}
                        disabled={actionLoading}
                        className="px-3 py-1.5 rounded border border-rose-300 bg-white text-rose-800 text-xs font-semibold hover:bg-rose-50 transition-colors"
                      >
                        Reject Application
                      </button>
                      <button
                        onClick={() => handleMakerSubmit(selectedReq.id, true)}
                        disabled={actionLoading}
                        className="px-4 py-1.5 rounded bg-slate-800 hover:bg-slate-900 text-white text-xs font-medium transition-colors"
                      >
                        Approve & Forward to Regional Officer →
                      </button>
                    </div>
                  </div>
                )}

                {/* Stage 2: Checker Action */}
                {selectedReq.maker_scrutiny_completed && !selectedReq.checker_ro_approved && (
                  <div className="p-4 rounded border border-slate-200 bg-slate-50/70 space-y-3">
                    <h4 className="text-xs font-bold text-slate-800">
                      Tier 2: Regional Directorate Administrative Review
                    </h4>
                    <p className="text-[11px] text-slate-600">
                      Regional Officer review of territorial jurisdiction and institutional good standing.
                    </p>
                    <textarea
                      rows={2}
                      value={roComments}
                      onChange={(e) => setRoComments(e.target.value)}
                      className="input-institutional text-xs py-1.5"
                    />
                    <div className="flex items-center justify-end space-x-2 pt-1">
                      <button
                        onClick={() => handleCheckerSubmit(selectedReq.id, false)}
                        disabled={actionLoading}
                        className="px-3 py-1.5 rounded border border-rose-300 bg-white text-rose-800 text-xs font-semibold hover:bg-rose-50 transition-colors"
                      >
                        Reject Concurrence
                      </button>
                      <button
                        onClick={() => handleCheckerSubmit(selectedReq.id, true)}
                        disabled={actionLoading}
                        className="px-4 py-1.5 rounded bg-slate-800 hover:bg-slate-900 text-white text-xs font-medium transition-colors"
                      >
                        Record Concurrence & Forward to Bureau Chief →
                      </button>
                    </div>
                  </div>
                )}

                {/* Stage 3: Authorizer Action */}
                {selectedReq.checker_ro_approved && !selectedReq.authority_authorized && (
                  <div className="p-4 rounded border border-blue-200 bg-blue-50/30 space-y-3">
                    <h4 className="text-xs font-bold text-blue-950 flex items-center space-x-1.5">
                      <Key className="h-3.5 w-3.5 text-blue-900" />
                      <span>Tier 3: Bureau Chief / Member Secretary Aadhaar e-Sign Authorization</span>
                    </h4>
                    <p className="text-[11px] text-slate-600">
                      Affixes Section 10(k) statutory discharge seal and generates digitally signed AICTE No Objection Certificate (NOC).
                    </p>
                    <div className="flex items-center space-x-3 pt-1">
                      <input
                        type="password"
                        placeholder="Enter 6-digit Aadhaar e-Sign PIN"
                        value={esignPin}
                        onChange={(e) => setEsignPin(e.target.value)}
                        className="input-institutional text-xs py-1.5 max-w-xs font-mono"
                      />
                      <button
                        onClick={() => handleAuthorizerSubmit(selectedReq.id)}
                        disabled={actionLoading}
                        className="px-4 py-1.5 rounded bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-semibold shadow-xs transition-colors"
                      >
                        Authorize & Issue Official NOC
                      </button>
                    </div>
                  </div>
                )}

                {/* Stage 4: Discharge Completed */}
                {selectedReq.status === 'RELEASED' && (
                  <div className="p-4 rounded border border-emerald-300 bg-emerald-50/80 space-y-3">
                    <div className="flex items-center space-x-2 text-emerald-950 font-bold text-xs">
                      <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                      <span>Statutory Lien Discharged & NOC Dispatched to Custodian Bank</span>
                    </div>
                    <div className="text-[11px] text-slate-700 space-y-1">
                      <div>Official NOC Number: <span className="font-mono font-bold text-slate-900">{selectedReq.noc_number}</span></div>
                      <div>Authorized By: <span className="font-medium text-slate-900">{selectedReq.authority_name}</span></div>
                    </div>

                    <a
                      href={`/static/noc_${selectedReq.noc_number}.pdf`}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center space-x-1.5 rounded bg-emerald-700 hover:bg-emerald-800 px-3.5 py-1.5 text-xs font-semibold text-white shadow-xs transition-colors"
                    >
                      <Download className="h-3.5 w-3.5" />
                      <span>Download AICTE Release NOC (PDF)</span>
                    </a>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
