import React, { useState } from 'react';
import { X, Building2, Landmark, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function NewFDRModal({ isOpen, onClose, institutions, onCreated }) {
  if (!isOpen) return null;

  const [institutionId, setInstitutionId] = useState(institutions?.[0]?.id || '');
  const [fdrNumber, setFdrNumber] = useState(`FDR-2026-SBI-${Math.floor(10000 + Math.random() * 90000)}`);
  const [accountNumber, setAccountNumber] = useState(`30${Math.floor(100000000 + Math.random() * 900000000)}`);
  const [bankName, setBankName] = useState('State Bank of India');
  const [branchName, setBranchName] = useState('Parliament Street Branch, New Delhi');
  const [ifscCode, setIfscCode] = useState('SBIN0001001');
  const [depositAmount, setDepositAmount] = useState(5000000);
  const [rateOfInterest, setRateOfInterest] = useState(7.25);
  const [issueDate, setIssueDate] = useState('2026-04-01');
  const [maturityDate, setMaturityDate] = useState('2034-04-01');
  const [lockInYears, setLockInYears] = useState(8);
  const [lienMarked, setLienMarked] = useState(true);

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg(null);

    try {
      const res = await fetch('/api/fdrs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          institution_id: institutionId,
          fdr_number: fdrNumber,
          account_number: accountNumber,
          bank_name: bankName,
          branch_name: branchName,
          ifsc_code: ifscCode,
          deposit_amount: Number(depositAmount),
          rate_of_interest: Number(rateOfInterest),
          issue_date: issueDate,
          maturity_date: maturityDate,
          statutory_lock_in_years: Number(lockInYears),
          statutory_lock_in_end_date: maturityDate,
          lien_marked: lienMarked,
          lien_reference_number: `AICTE/REG/FDR-LIEN/${fdrNumber.slice(-5)}`
        })
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to pledge FDR");
      }

      const result = await res.json();
      onCreated?.(result);
      onClose();
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleBankChange = (name) => {
    setBankName(name);
    if (name === 'State Bank of India') {
      setIfscCode('SBIN0001001');
      setBranchName('Parliament Street, New Delhi');
    } else if (name === 'Punjab National Bank') {
      setIfscCode('PUNB0021300');
      setBranchName('Hazratganj, Lucknow');
    } else if (name === 'HDFC Bank') {
      setIfscCode('HDFC0000240');
      setBranchName('Anna Salai, Chennai');
    } else if (name === 'Canara Bank') {
      setIfscCode('CNRB0000123');
      setBranchName('MG Road, Bangalore');
    } else if (name === 'Bank of Baroda') {
      setIfscCode('BARB0BANJAR');
      setBranchName('Banjara Hills, Hyderabad');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="bg-white w-full max-w-2xl rounded-md border border-slate-300 p-5 shadow-xl relative my-6 animate-modal">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 rounded p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700 transition-colors"
        >
          <X className="h-4 w-4" />
        </button>

        <div className="border-b border-slate-200 pb-2.5 mb-3">
          <span className="rounded bg-blue-50 text-blue-950 px-2 py-0.5 text-[10px] font-bold border border-blue-200 uppercase">
            STATUTORY COLLATERAL SUBMISSION
          </span>
          <h2 className="text-sm font-bold text-slate-900 mt-1">Pledge Fixed Deposit Receipt (FDR) to AICTE</h2>
          <p className="text-xs text-slate-500">
            Submit new deposit instrument for joint regulatory lien custody under Approval Process Handbook (APH)
          </p>
        </div>

        {errorMsg && (
          <div className="rounded border border-rose-300 bg-rose-50 p-2.5 text-xs text-rose-800 mb-3 flex items-center space-x-2 font-medium">
            <AlertTriangle className="h-4 w-4 text-rose-600 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3.5 text-xs">
          {/* Institution Selector */}
          <div>
            <label className="text-[11px] font-semibold text-slate-700 block mb-1">
              Select Depositor Technical Institution
            </label>
            <select
              value={institutionId}
              onChange={(e) => setInstitutionId(e.target.value)}
              className="select-institutional w-full py-1.5"
              required
            >
              {institutions?.map((inst) => (
                <option key={inst.id} value={inst.id}>
                  {inst.name} (PID: {inst.pid} • {inst.state})
                </option>
              ))}
            </select>
          </div>

          {/* FDR Number & Account Number */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <div>
              <label className="text-[11px] font-semibold text-slate-700 block mb-1">FDR Receipt Number</label>
              <input
                type="text"
                value={fdrNumber}
                onChange={(e) => setFdrNumber(e.target.value)}
                className="input-institutional py-1.5 font-mono font-bold"
                required
              />
            </div>

            <div>
              <label className="text-[11px] font-semibold text-slate-700 block mb-1">Bank Account Number</label>
              <input
                type="text"
                value={accountNumber}
                onChange={(e) => setAccountNumber(e.target.value)}
                className="input-institutional py-1.5 font-mono font-bold"
                required
              />
            </div>
          </div>

          {/* Bank Selection, Branch & IFSC */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
            <div>
              <label className="text-[11px] font-semibold text-slate-700 block mb-1">Custodian Bank</label>
              <select
                value={bankName}
                onChange={(e) => handleBankChange(e.target.value)}
                className="select-institutional w-full py-1.5"
              >
                <option value="State Bank of India">State Bank of India</option>
                <option value="Punjab National Bank">Punjab National Bank</option>
                <option value="HDFC Bank">HDFC Bank</option>
                <option value="Canara Bank">Canara Bank</option>
                <option value="Bank of Baroda">Bank of Baroda</option>
              </select>
            </div>

            <div>
              <label className="text-[11px] font-semibold text-slate-700 block mb-1">Branch Name</label>
              <input
                type="text"
                value={branchName}
                onChange={(e) => setBranchName(e.target.value)}
                className="input-institutional py-1.5"
                required
              />
            </div>

            <div>
              <label className="text-[11px] font-semibold text-slate-700 block mb-1">IFSC Code</label>
              <input
                type="text"
                value={ifscCode}
                onChange={(e) => setIfscCode(e.target.value)}
                className="input-institutional py-1.5 font-mono font-bold"
                required
              />
            </div>
          </div>

          {/* Financial Amounts & Rates */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <div>
              <label className="text-[11px] font-semibold text-slate-700 block mb-1">Deposit Principal (INR)</label>
              <input
                type="number"
                value={depositAmount}
                onChange={(e) => setDepositAmount(e.target.value)}
                className="input-institutional py-1.5 font-mono text-xs font-bold"
                required
                min={100000}
                step={50000}
              />
            </div>

            <div>
              <label className="text-[11px] font-semibold text-slate-700 block mb-1">Interest Rate (% p.a.)</label>
              <input
                type="number"
                value={rateOfInterest}
                onChange={(e) => setRateOfInterest(e.target.value)}
                className="input-institutional py-1.5 font-mono font-bold"
                step={0.05}
                required
              />
            </div>
          </div>

          {/* Dates & Tenure */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
            <div>
              <label className="text-[11px] font-semibold text-slate-700 block mb-1">Issue Date</label>
              <input
                type="date"
                value={issueDate}
                onChange={(e) => setIssueDate(e.target.value)}
                className="input-institutional py-1.5 font-mono font-medium"
                required
              />
            </div>

            <div>
              <label className="text-[11px] font-semibold text-slate-700 block mb-1">Maturity Date</label>
              <input
                type="date"
                value={maturityDate}
                onChange={(e) => setMaturityDate(e.target.value)}
                className="input-institutional py-1.5 font-mono font-medium"
                required
              />
            </div>

            <div>
              <label className="text-[11px] font-semibold text-slate-700 block mb-1">Statutory Lock-in</label>
              <select
                value={lockInYears}
                onChange={(e) => setLockInYears(e.target.value)}
                className="select-institutional w-full py-1.5"
              >
                <option value={8}>8 Academic Cycles</option>
                <option value={10}>10 Academic Cycles</option>
              </select>
            </div>
          </div>

          {/* Lien Checkbox */}
          <div className="p-3 rounded bg-slate-50 border border-slate-200 flex items-center space-x-2.5">
            <input
              type="checkbox"
              id="lienMarkedCheck"
              checked={lienMarked}
              onChange={(e) => setLienMarked(e.target.checked)}
              className="h-4 w-4 rounded border-slate-300 text-blue-900 focus:ring-blue-900"
            />
            <label htmlFor="lienMarkedCheck" className="text-[11px] text-slate-700">
              <span className="font-semibold text-slate-900">Statutory Lien Endorsement: </span>
              Lien endorsed in favor of Member Secretary, AICTE, New Delhi. No premature encashment or loan permitted.
            </label>
          </div>

          <div className="flex items-center justify-end space-x-2.5 pt-2 border-t border-slate-200">
            <button
              type="button"
              onClick={onClose}
              className="px-3.5 py-1.5 rounded text-slate-600 font-medium hover:bg-slate-100 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="rounded bg-blue-900 hover:bg-blue-950 px-4 py-1.5 font-semibold text-white text-xs shadow-xs transition-colors disabled:opacity-50"
            >
              {loading ? 'Submitting & Pledging...' : 'Pledge FDR to AICTE Registry'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
