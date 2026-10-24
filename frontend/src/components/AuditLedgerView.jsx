import React, { useState, useEffect } from 'react';
import { 
  RefreshCw, ShieldCheck, ShieldAlert, Layers, CheckCircle2, 
  AlertTriangle, Lock, Eye, X, Terminal, Cpu, ArrowRight, Shield
} from 'lucide-react';

export default function AuditLedgerView() {
  const [records, setRecords] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [verificationResult, setVerificationResult] = useState(null);
  const [verifying, setVerifying] = useState(false);
  const [selectedBlock, setSelectedBlock] = useState(null);
  const [tamperLoading, setTamperLoading] = useState(false);
  const [tamperNotice, setTamperNotice] = useState(null);

  const fetchLedger = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/audit/ledger?limit=50');
      if (res.ok) {
        const data = await res.json();
        setRecords(data.records || []);
        setTotal(data.total || 0);
      }
    } catch (err) {
      console.error("Failed to load audit ledger:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLedger();
    handleVerifyChain();
  }, []);

  const handleVerifyChain = async () => {
    setVerifying(true);
    try {
      const res = await fetch('/api/audit/verify-chain');
      if (res.ok) {
        const data = await res.json();
        setVerificationResult(data);
      }
    } catch (err) {
      console.error("Verification failed:", err);
    } finally {
      setVerifying(false);
    }
  };

  const handleTamperSimulation = async () => {
    if (!records.length) return;
    setTamperLoading(true);
    setTamperNotice(null);
    try {
      const targetId = records[Math.floor(records.length / 2)].id;
      const res = await fetch(`/api/audit/simulate-tamper/${targetId}`, {
        method: 'POST'
      });
      if (res.ok) {
        const data = await res.json();
        setTamperNotice(data);
        await fetchLedger();
        await handleVerifyChain();
      }
    } catch (err) {
      console.error("Tamper simulation failed:", err);
    } finally {
      setTamperLoading(false);
    }
  };

  return (
    <div className="space-y-5 animate-entrance">
      {/* Top Hero Integrity Status Card */}
      <div className={`p-4 rounded-md border bg-white ${
        verificationResult?.is_valid
          ? 'border-emerald-300'
          : 'border-rose-300 bg-rose-50/30'
      }`}>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start space-x-3">
            <div className={`h-10 w-10 rounded-md flex items-center justify-center shrink-0 ${
              verificationResult?.is_valid ? 'bg-emerald-700 text-white' : 'bg-rose-700 text-white'
            }`}>
              {verificationResult?.is_valid ? <ShieldCheck className="h-5 w-5" /> : <ShieldAlert className="h-5 w-5" />}
            </div>

            <div>
              <div className="flex items-center space-x-2">
                <h2 className="text-sm md:text-base font-bold text-slate-900 tracking-tight">
                  {verificationResult?.is_valid
                    ? 'Cryptographic Hash Chain: Untampered & Verified'
                    : 'Security Alert: Ledger Tampering Detected!'}
                </h2>
                <span className={`px-2 py-0.2 rounded text-[10px] font-bold ${
                  verificationResult?.is_valid ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                }`}>
                  {verificationResult?.total_records || records.length} Linked Blocks
                </span>
              </div>
              <p className="text-xs text-slate-600 mt-0.5 max-w-2xl leading-normal">
                Every transaction is cryptographically sealed using SHA-256 forward-secure Merkle hash chaining. Out-of-band database modifications immediately break mathematical integrity.
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2 shrink-0">
            <button
              onClick={handleVerifyChain}
              disabled={verifying}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-md bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`h-3.5 w-3.5 text-slate-500 ${verifying ? 'animate-spin' : ''}`} />
              <span>{verifying ? 'Checking...' : 'Re-verify Chain'}</span>
            </button>

            <button
              onClick={handleTamperSimulation}
              disabled={tamperLoading}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-md bg-white border border-rose-300 hover:bg-rose-50 text-rose-800 text-xs font-semibold transition-colors disabled:opacity-50"
            >
              <ShieldAlert className="h-3.5 w-3.5 text-rose-600" />
              <span>Simulate Tamper Attack</span>
            </button>
          </div>
        </div>
      </div>

      {tamperNotice && (
        <div className="p-3 rounded-md border border-rose-300 bg-rose-50/80 text-xs text-rose-900 space-y-1">
          <div className="font-bold flex items-center space-x-1.5">
            <AlertTriangle className="h-4 w-4 text-rose-600 shrink-0" />
            <span>Out-of-band Tamper Injection Executed (Record #{tamperNotice.record_id})</span>
          </div>
          <p className="text-[11px] leading-normal">
            Direct database modification without updating previous SHA-256 forward hashes has broken the chain proof at block #{tamperNotice.record_id}. The system flagged the tampering immediately.
          </p>
        </div>
      )}

      {/* Merkle Block Table */}
      <div className="card-institutional bg-white border border-slate-200 overflow-hidden">
        <div className="p-3.5 border-b border-slate-200 flex items-center justify-between bg-slate-50/60">
          <div>
            <h3 className="text-xs font-bold text-slate-900 flex items-center space-x-1.5">
              <Layers className="h-4 w-4 text-blue-900" />
              <span>Immutable Ledger Blocks (Reverse Chronological)</span>
            </h3>
            <p className="text-[11px] text-slate-500 mt-0.5">SHA-256 cryptographic sequence verifying every statutory collateral operation</p>
          </div>
          <span className="font-mono text-[11px] text-slate-600 bg-white px-2 py-0.5 rounded border border-slate-200">
            {records.length} Blocks Recorded
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full table-fintech text-left">
            <thead>
              <tr>
                <th>Seq #</th>
                <th>Timestamp</th>
                <th>Operation / Event</th>
                <th>Actor & IP</th>
                <th>Current SHA-256 Digest</th>
                <th>Previous Hash Link</th>
                <th className="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              {records.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-xs text-slate-500">
                    No audit records found.
                  </td>
                </tr>
              ) : (
                records.map((r, idx) => (
                  <tr key={r.id}>
                    <td className="font-mono font-bold text-slate-900 text-xs">
                      #{r.id}
                    </td>

                    <td className="font-mono text-slate-500 text-[10.5px]">
                      {new Date(r.timestamp).toLocaleString()}
                    </td>

                    <td>
                      <span className="font-semibold text-slate-800 text-xs block">{r.action}</span>
                      <span className="text-[10px] text-slate-500">{r.entity_type} • ID {r.entity_id}</span>
                    </td>

                    <td className="text-slate-600 text-xs">
                      <div>{r.actor_id}</div>
                      <div className="text-[10px] text-slate-400 font-mono">{r.ip_address}</div>
                    </td>

                    <td className="font-mono text-[10.5px] text-slate-800">
                      <span className="bg-slate-100 px-1 py-0.5 rounded text-blue-950 font-bold border border-slate-200">
                        {r.current_hash?.substring(0, 16)}...
                      </span>
                    </td>

                    <td className="font-mono text-[10.5px] text-slate-500">
                      {r.previous_hash === 'GENESIS_BLOCK_0000000000000000000000000000000000000000000000000000000000000000' ? (
                        <span className="text-emerald-700 font-bold">GENESIS</span>
                      ) : (
                        <span>{r.previous_hash?.substring(0, 12)}...</span>
                      )}
                    </td>

                    <td className="text-center">
                      <button
                        onClick={() => setSelectedBlock(r)}
                        className="px-2 py-1 rounded border border-slate-300 bg-white hover:bg-slate-50 text-[11px] font-medium text-slate-700 hover:text-blue-900 transition-colors"
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Block Inspector Modal */}
      {selectedBlock && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4 overflow-y-auto">
          <div className="bg-white w-full max-w-2xl rounded-md border border-slate-300 p-5 shadow-xl space-y-3.5 my-6 animate-modal">
            <div className="flex items-center justify-between border-b border-slate-200 pb-2.5">
              <div className="flex items-center space-x-2">
                <span className="font-mono font-bold text-sm text-slate-900">Block #{selectedBlock.id}</span>
                <span className="px-1.5 py-0.2 rounded bg-slate-100 text-slate-700 text-[10px] font-mono border border-slate-200 font-bold">
                  {selectedBlock.action}
                </span>
              </div>
              <button onClick={() => setSelectedBlock(null)} className="text-slate-400 hover:text-slate-700">
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="space-y-2 text-xs">
              <div className="p-2.5 rounded bg-slate-50 border border-slate-200 space-y-1 font-mono text-[11px]">
                <div className="text-slate-500 font-sans font-semibold text-[10.5px]">Cryptographic Hashes:</div>
                <div className="break-all"><span className="text-slate-500">Current Hash: </span><span className="text-blue-950 font-bold">{selectedBlock.current_hash}</span></div>
                <div className="break-all"><span className="text-slate-500">Previous Hash: </span><span>{selectedBlock.previous_hash}</span></div>
                <div className="break-all"><span className="text-slate-500">Merkle Root: </span><span className="text-emerald-800">{selectedBlock.merkle_root}</span></div>
              </div>

              <div>
                <span className="text-[10.5px] font-bold text-slate-600 block mb-1">Block Event Payload:</span>
                <pre className="p-2.5 rounded bg-slate-900 text-slate-100 font-mono text-[11px] overflow-x-auto max-h-56">
                  {JSON.stringify(selectedBlock.payload, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
