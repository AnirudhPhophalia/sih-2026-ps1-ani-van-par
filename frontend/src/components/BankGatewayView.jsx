import React, { useState } from 'react';
import { 
  KeyRound, Landmark, ShieldCheck, ExternalLink, CheckCircle2, 
  RefreshCw, Send, AlertTriangle, FileCheck, Layers, Copy, Check
} from 'lucide-react';

export default function BankGatewayView({ fdrs, onRefreshAll }) {
  const [selectedFdrId, setSelectedFdrId] = useState(fdrs?.[0]?.id || '');
  const [activeMode, setActiveMode] = useState('cbs'); // cbs, token, nesl

  // Mode 1 state
  const [cbsLoading, setCbsLoading] = useState(false);
  const [cbsResponse, setCbsResponse] = useState(null);

  // Mode 2 state
  const [branchEmail, setBranchEmail] = useState('chief.manager.01001@sbi.co.in');
  const [tokenLoading, setTokenLoading] = useState(false);
  const [generatedToken, setGeneratedToken] = useState(null);
  const [deskModalOpen, setDeskModalOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  // Branch Manager Desk Form inside Modal
  const [bmName, setBmName] = useState('Shri Amit Kapoor');
  const [bmEmpId, setBmEmpId] = useState('SBI-BM-48910');
  const [bmApproved, setBmApproved] = useState(true);
  const [bmNotes, setBmNotes] = useState('Statutory lien endorsed in bank CBS register under A/C ledger.');
  const [bmSubmitting, setBmSubmitting] = useState(false);
  const [bmSuccess, setBmSuccess] = useState(null);

  // Mode 3 state
  const [neslLoading, setNeslLoading] = useState(false);
  const [neslResponse, setNeslResponse] = useState(null);

  const selectedFdr = (fdrs || []).find(f => f.id === selectedFdrId) || fdrs?.[0];

  const handleCbsQuery = async () => {
    if (!selectedFdr) return;
    setCbsLoading(true);
    setCbsResponse(null);
    try {
      const res = await fetch(`/api/bank-gateway/cbs-verify/${selectedFdr.id}`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setCbsResponse(data);
        onRefreshAll?.();
      }
    } catch (err) {
      console.error("CBS query failed:", err);
    } finally {
      setCbsLoading(false);
    }
  };

  const handleGenerateToken = async () => {
    if (!selectedFdr) return;
    setTokenLoading(true);
    try {
      const res = await fetch('/api/bank-gateway/generate-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fdr_id: selectedFdr.id,
          branch_email: branchEmail
        })
      });
      if (res.ok) {
        const data = await res.json();
        setGeneratedToken(data);
      }
    } catch (err) {
      console.error("Token generation failed:", err);
    } finally {
      setTokenLoading(false);
    }
  };

  const handleBmSubmit = async () => {
    if (!generatedToken) return;
    setBmSubmitting(true);
    try {
      const res = await fetch(`/api/bank-gateway/desk/${generatedToken.token}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          manager_name: bmName,
          manager_emp_id: bmEmpId,
          is_approved: bmApproved,
          notes: bmNotes
        })
      });
      if (res.ok) {
        const data = await res.json();
        setBmSuccess(data);
        onRefreshAll?.();
      }
    } catch (err) {
      console.error("BM verification submit failed:", err);
    } finally {
      setBmSubmitting(false);
    }
  };

  const handleNeslQuery = async () => {
    if (!selectedFdr) return;
    setNeslLoading(true);
    setNeslResponse(null);
    try {
      const res = await fetch(`/api/bank-gateway/nesl-verify/${selectedFdr.id}`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setNeslResponse(data);
        onRefreshAll?.();
      }
    } catch (err) {
      console.error("NeSL query failed:", err);
    } finally {
      setNeslLoading(false);
    }
  };

  return (
    <div className="space-y-5 animate-entrance">
      {/* Title */}
      <div>
        <h1 className="text-sm md:text-base font-semibold text-slate-800 flex items-center space-x-2">
          <KeyRound className="h-4 w-4 text-slate-600" />
          <span>Tri-Modal Bank Verification Gateway & CBS Simulator</span>
        </h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Statutory banking integration via Open Banking CBS/SFMS endpoints, digital tokens, and NeSL Information Utility
        </p>
      </div>

      {/* Target Instrument Selector */}
      <div className="card-institutional p-3.5 bg-white border border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div className="flex-1">
          <label className="text-[11px] font-semibold text-slate-700 uppercase tracking-wider block mb-1">
            Target Fixed Deposit Instrument for Bank Telemetry
          </label>
          <select
            value={selectedFdrId}
            onChange={(e) => {
              setSelectedFdrId(e.target.value);
              setCbsResponse(null);
              setGeneratedToken(null);
              setNeslResponse(null);
            }}
            className="select-institutional w-full font-mono text-xs py-1.5"
          >
            {fdrs?.map(f => (
              <option key={f.id} value={f.id}>
                {f.fdr_number} • {f.bank_name} • ₹{(f.deposit_amount / 100000).toFixed(1)}L • {f.institution_name} ({f.status})
              </option>
            ))}
          </select>
        </div>

        {selectedFdr && (
          <div className="flex items-center space-x-3 text-xs bg-slate-50 p-2.5 rounded border border-slate-200">
            <div>
              <span className="text-[10px] text-slate-500 block font-medium">Current Status:</span>
              <span className="font-medium text-slate-800">{selectedFdr.status}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-500 block font-medium">Verification Protocol:</span>
              <span className="font-medium text-slate-800">{selectedFdr.verification_level}</span>
            </div>
          </div>
        )}
      </div>

      {/* Mode Selection Tabs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <button
          onClick={() => setActiveMode('cbs')}
          className={`p-3.5 rounded border text-left transition-colors ${
            activeMode === 'cbs' 
              ? 'bg-slate-100/90 border-slate-400' 
              : 'bg-white border-slate-200 hover:border-slate-300'
          }`}
        >
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-800 mb-1">
            <Landmark className="h-4 w-4 text-slate-600" />
            <span>Mode 1: CBS / SFMS Real-Time API</span>
          </div>
          <p className="text-[11px] text-slate-500 leading-normal">
            Real-time query to simulated Core Banking System API (SBI, PNB, HDFC, Canara, BoB). Reconciles live ledger balance and statutory lien status.
          </p>
        </button>

        <button
          onClick={() => setActiveMode('token')}
          className={`p-3.5 rounded border text-left transition-colors ${
            activeMode === 'token' 
              ? 'bg-slate-100/90 border-slate-400' 
              : 'bg-white border-slate-200 hover:border-slate-300'
          }`}
        >
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-800 mb-1">
            <Send className="h-4 w-4 text-slate-600" />
            <span>Mode 2: Signed Branch Token Link</span>
          </div>
          <p className="text-[11px] text-slate-500 leading-normal">
            Dispatches authenticated one-time link to Branch Manager's official bank email for digital certification and signature.
          </p>
        </button>

        <button
          onClick={() => setActiveMode('nesl')}
          className={`p-3.5 rounded border text-left transition-colors ${
            activeMode === 'nesl' 
              ? 'bg-slate-100/90 border-slate-400' 
              : 'bg-white border-slate-200 hover:border-slate-300'
          }`}
        >
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-800 mb-1">
            <FileCheck className="h-4 w-4 text-slate-600" />
            <span>Mode 3: NeSL & DigiLocker DDE</span>
          </div>
          <p className="text-[11px] text-slate-500 leading-normal">
            National E-Governance Services Ltd (NeSL) Information Utility & DigiLocker e-Stamp certification registry.
          </p>
        </button>
      </div>

      {/* Mode 1 Content: CBS API Simulator */}
      {activeMode === 'cbs' && (
        <div className="card-institutional p-4 bg-white border border-slate-200 space-y-3.5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-xs font-bold text-slate-900 flex items-center space-x-2">
                <Landmark className="h-4 w-4 text-blue-900" />
                <span>Simulate Open Banking Core Banking System (CBS) Query</span>
              </h2>
              <p className="text-[11px] text-slate-500 font-mono mt-0.5">POST /api/bank-gateway/cbs-verify/{'{fdr_id}'}</p>
            </div>

            <button
              onClick={handleCbsQuery}
              disabled={cbsLoading}
              className="flex items-center space-x-1.5 rounded bg-slate-800 hover:bg-slate-900 px-3.5 py-1.5 text-xs font-medium text-white disabled:opacity-50 transition-colors"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${cbsLoading ? 'animate-spin' : ''}`} />
              <span>{cbsLoading ? 'Querying CBS...' : 'Execute Live CBS Query'}</span>
            </button>
          </div>

          {cbsResponse && (
            <div className="rounded border border-slate-200 bg-slate-50 p-3 space-y-2.5 font-mono text-xs">
              <div className="flex items-center justify-between text-slate-700 border-b border-slate-200 pb-2">
                <span className="text-emerald-800 font-bold">200 OK • CBS_SFMS_GATEWAY_SUCCESS</span>
                <span className="text-slate-500">Ref: {cbsResponse.transaction_ref}</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 font-sans">
                <div className="p-2.5 rounded bg-white border border-slate-200">
                  <span className="text-[10px] text-slate-500 block font-semibold">Lien Status Confirmed</span>
                  <span className="font-bold text-emerald-800 text-xs">{cbsResponse.lien_status}</span>
                </div>
                <div className="p-2.5 rounded bg-white border border-slate-200">
                  <span className="text-[10px] text-slate-500 block font-semibold">CBS Confirmed Balance</span>
                  <span className="font-bold text-slate-900 text-xs font-mono">₹{cbsResponse.confirmed_amount?.toLocaleString('en-IN')}</span>
                </div>
                <div className="p-2.5 rounded bg-white border border-slate-200">
                  <span className="text-[10px] text-slate-500 block font-semibold">Updated Regulatory Status</span>
                  <span className="font-bold text-blue-900 text-xs">{cbsResponse.instrument_status}</span>
                </div>
              </div>

              <pre className="text-[11px] text-slate-700 bg-white p-2.5 rounded border border-slate-200 overflow-x-auto">
                {JSON.stringify(cbsResponse, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}

      {/* Mode 2 Content: Branch Manager Token */}
      {activeMode === 'token' && (
        <div className="card-institutional p-4 bg-white border border-slate-200 space-y-3.5">
          <div>
            <h2 className="text-xs font-bold text-slate-900 flex items-center space-x-2">
              <Send className="h-4 w-4 text-blue-900" />
              <span>Bank Official Verification Token Dispatcher</span>
            </h2>
            <p className="text-[11px] text-slate-500 mt-0.5">
              Generates an authenticated one-time cryptographic verification link for the bank branch manager
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-12 gap-2.5 items-end">
            <div className="md:col-span-8">
              <label className="text-[11px] font-semibold text-slate-700 block mb-1">Branch Manager Official Bank Email</label>
              <input
                type="email"
                value={branchEmail}
                onChange={(e) => setBranchEmail(e.target.value)}
                className="input-institutional text-xs py-1.5"
              />
            </div>
            <div className="md:col-span-4">
              <button
                onClick={handleGenerateToken}
                disabled={tokenLoading}
                className="w-full rounded bg-slate-800 hover:bg-slate-900 px-3.5 py-1.5 text-xs font-medium text-white disabled:opacity-50 transition-colors"
              >
                {tokenLoading ? 'Generating Token...' : 'Dispatch Token Link'}
              </button>
            </div>
          </div>

          {generatedToken && (
            <div className="rounded border border-slate-200 bg-slate-50/70 p-3 space-y-2.5 text-xs">
              <div className="flex items-center justify-between text-slate-800 font-semibold">
                <span className="flex items-center space-x-1.5">
                  <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                  <span>One-Time Signed Branch Manager Token Active</span>
                </span>
                <span className="font-mono text-[10px] text-slate-500">EXPIRES_IN: 72_HOURS</span>
              </div>

              <div className="flex items-center space-x-2 bg-white p-2 rounded border border-slate-200 font-mono text-slate-700 text-[11px]">
                <span className="truncate flex-1">{window.location.origin}/bank-verification/{generatedToken.token}</span>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(`${window.location.origin}/bank-verification/${generatedToken.token}`);
                    setCopied(true);
                    setTimeout(() => setCopied(false), 2000);
                  }}
                  className="p-1 rounded hover:bg-slate-100 text-slate-600 transition-colors"
                  title="Copy link"
                >
                  {copied ? <Check className="h-3.5 w-3.5 text-emerald-600" /> : <Copy className="h-3.5 w-3.5" />}
                </button>
              </div>

              <div className="flex items-center justify-between pt-1">
                <span className="text-slate-500 text-[11px]">Simulate Branch Manager Experience:</span>
                <button
                  onClick={() => {
                    setBmSuccess(null);
                    setDeskModalOpen(true);
                  }}
                  className="rounded bg-slate-800 hover:bg-slate-900 px-3 py-1 text-xs font-medium text-white transition-colors"
                >
                  Open Branch Manager Verification Desk →
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Mode 3 Content: NeSL */}
      {activeMode === 'nesl' && (
        <div className="card-institutional p-4 bg-white border border-slate-200 space-y-3.5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-xs font-semibold text-slate-800 flex items-center space-x-2">
                <FileCheck className="h-4 w-4 text-slate-600" />
                <span>NeSL Information Utility & DigiLocker e-Stamp Validation</span>
              </h2>
              <p className="text-[11px] text-slate-500 mt-0.5">Validates against Digital Document Execution (DDE) e-Stamping registry</p>
            </div>

            <button
              onClick={handleNeslQuery}
              disabled={neslLoading}
              className="flex items-center space-x-1.5 rounded bg-slate-800 hover:bg-slate-900 px-3.5 py-1.5 text-xs font-medium text-white disabled:opacity-50 transition-colors"
            >
              <FileCheck className={`h-3.5 w-3.5 ${neslLoading ? 'animate-spin' : ''}`} />
              <span>{neslLoading ? 'Querying NeSL DDE...' : 'Verify via NeSL DDE'}</span>
            </button>
          </div>

          {neslResponse && (
            <div className="rounded border border-blue-200 bg-blue-50/40 p-3 space-y-2 text-xs font-mono">
              <div className="flex items-center justify-between text-blue-950 font-bold font-sans">
                <span>NeSL DDE & DigiLocker Certification Verified</span>
                <span className="text-emerald-700">STATUS: AUTHENTICATED</span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-slate-800">
                <div className="p-2 rounded bg-white border border-slate-200">
                  <span className="text-[10px] text-slate-500 block font-sans font-semibold">e-Stamp Certificate No:</span>
                  <span className="text-blue-950 font-bold">{neslResponse.estamp_certificate}</span>
                </div>
                <div className="p-2 rounded bg-white border border-slate-200">
                  <span className="text-[10px] text-slate-500 block font-sans font-semibold">DigiLocker URI:</span>
                  <span className="text-slate-800">{neslResponse.digilocker_uri}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Mode 2 Interactive Desk Modal */}
      {deskModalOpen && selectedFdr && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4 overflow-y-auto">
          <div className="bg-white w-full max-w-xl rounded-md border border-slate-300 p-5 shadow-xl space-y-3.5 my-6 animate-modal">
            <div className="flex items-center justify-between border-b border-slate-200 pb-2.5">
              <div>
                <span className="rounded bg-blue-50 text-blue-950 px-2 py-0.5 text-[10px] font-bold border border-blue-200 uppercase">
                  BRANCH MANAGER VERIFICATION DESK
                </span>
                <h3 className="text-sm font-bold text-slate-900 mt-1">Official Lien Certification Portal</h3>
              </div>
              <button onClick={() => setDeskModalOpen(false)} className="text-slate-400 hover:text-slate-700 text-xs font-semibold">Close</button>
            </div>

            {bmSuccess ? (
              <div className="p-5 rounded border border-emerald-300 bg-emerald-50 text-center space-y-2.5">
                <CheckCircle2 className="h-8 w-8 text-emerald-600 mx-auto" />
                <h4 className="text-xs font-bold text-emerald-950">Bank Verification Digitally Signed</h4>
                <p className="text-xs text-slate-600">
                  The statutory lien has been officially certified. Instrument {bmSuccess.fdr_number} updated to {bmSuccess.instrument_status}.
                </p>
                <button
                  onClick={() => setDeskModalOpen(false)}
                  className="rounded bg-emerald-700 hover:bg-emerald-800 px-3.5 py-1 text-xs font-semibold text-white shadow-xs"
                >
                  Return to Portal
                </button>
              </div>
            ) : (
              <div className="space-y-3 text-xs">
                <div className="p-2.5 rounded bg-slate-50 border border-slate-200 space-y-0.5">
                  <div className="text-[10.5px] text-slate-500 font-semibold">Verifying Instrument:</div>
                  <div className="font-mono font-bold text-slate-900 text-xs">{selectedFdr.fdr_number} • ₹{selectedFdr.deposit_amount?.toLocaleString('en-IN')}</div>
                  <div className="text-slate-600 text-[11px]">{selectedFdr.institution_name} • {selectedFdr.bank_name}</div>
                </div>

                <div className="grid grid-cols-2 gap-2.5">
                  <div>
                    <label className="text-[10.5px] font-semibold text-slate-600 block mb-1">Branch Manager Name</label>
                    <input
                      type="text"
                      value={bmName}
                      onChange={(e) => setBmName(e.target.value)}
                      className="input-institutional text-xs py-1.5"
                    />
                  </div>
                  <div>
                    <label className="text-[10.5px] font-semibold text-slate-600 block mb-1">Bank Employee ID</label>
                    <input
                      type="text"
                      value={bmEmpId}
                      onChange={(e) => setBmEmpId(e.target.value)}
                      className="input-institutional text-xs py-1.5 font-mono"
                    />
                  </div>
                </div>

                <div>
                  <label className="text-[10.5px] font-semibold text-slate-600 block mb-1">Official Bank Certification Remarks</label>
                  <textarea
                    rows={2}
                    value={bmNotes}
                    onChange={(e) => setBmNotes(e.target.value)}
                    className="input-institutional text-xs py-1.5"
                  />
                </div>

                <div className="flex items-center space-x-2 pt-1">
                  <button
                    onClick={() => setBmApproved(true)}
                    className={`flex-1 py-1.5 rounded text-xs font-semibold border transition-colors ${
                      bmApproved ? 'bg-emerald-50 text-emerald-900 border-emerald-300 font-bold' : 'bg-slate-50 text-slate-600 border-slate-200'
                    }`}
                  >
                    Confirm Statutory AICTE Lien
                  </button>
                  <button
                    onClick={() => setBmApproved(false)}
                    className={`flex-1 py-1.5 rounded text-xs font-semibold border transition-colors ${
                      !bmApproved ? 'bg-rose-50 text-rose-900 border-rose-300 font-bold' : 'bg-slate-50 text-slate-600 border-slate-200'
                    }`}
                  >
                    Reject / Flag Discrepancy
                  </button>
                </div>

                <button
                  onClick={handleBmSubmit}
                  disabled={bmSubmitting}
                  className="w-full py-2 rounded-md bg-blue-900 hover:bg-blue-950 font-semibold text-white text-xs shadow-xs transition-colors disabled:opacity-50"
                >
                  {bmSubmitting ? 'Signing Digital Token...' : 'Digitally Sign & Certify Lien'}
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
