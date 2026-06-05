import { useState, useEffect } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  ResponsiveContainer, ReferenceLine, Legend,
} from "recharts";

const API = "http://localhost:8000";

const PATIENTS = [
  { id: 1, label: "Patient 1", condition: "Diabetes",      color: "#E85D24" },
  { id: 2, label: "Patient 2", condition: "Hypertension",  color: "#185fa5" },
  { id: 3, label: "Patient 3", condition: "Cardiac",       color: "#6b30b8" },
];

const RISK_COLORS = {
  LOW: "#16a34a", MEDIUM: "#d97706", HIGH: "#dc2626", CRITICAL: "#7f1d1d",
};

function RiskBadge({ text }) {
  const level = ["CRITICAL", "HIGH", "MEDIUM", "LOW"].find(l => text?.toUpperCase().includes(l)) || "LOW";
  return (
    <span style={{
      background: RISK_COLORS[level], color: "white",
      padding: "2px 10px", borderRadius: 99, fontSize: 12, fontWeight: 700,
    }}>
      {level}
    </span>
  );
}

function StatCard({ label, value, unit, hi, lo }) {
  const num = parseFloat(value);
  const alert = num > hi || num < lo;
  return (
    <div style={{
      background: alert ? "#fff1f0" : "#f0faf6",
      border: `1px solid ${alert ? "#fca5a5" : "#6ee7b7"}`,
      borderRadius: 10, padding: "12px 16px", minWidth: 120,
    }}>
      <div style={{ fontSize: 11, color: "#666", marginBottom: 2 }}>{label}</div>
      <div style={{ fontSize: 22, fontWeight: 700, color: alert ? "#dc2626" : "#065f46" }}>
        {value} <span style={{ fontSize: 12 }}>{unit}</span>
      </div>
      {alert && <div style={{ fontSize: 10, color: "#dc2626", marginTop: 2 }}>⚠ Out of range</div>}
    </div>
  );
}

export default function App() {
  const [patientId, setPatientId]   = useState(1);
  const [vitals, setVitals]         = useState([]);
  const [summary, setSummary]       = useState(null);
  const [result, setResult]         = useState(null);
  const [loading, setLoading]       = useState(false);
  const [activeTab, setActiveTab]   = useState("charts");

  useEffect(() => {
    setResult(null);
    fetch(`${API}/patient/${patientId}/vitals?limit=80`)
      .then(r => r.json()).then(d => setVitals(d.vitals || []));
    fetch(`${API}/patient/${patientId}/summary`)
      .then(r => r.json()).then(setSummary);
  }, [patientId]);

  const runAnalysis = () => {
    setLoading(true);
    setActiveTab("alerts");
    fetch(`${API}/patient/${patientId}/monitor`)
      .then(r => r.json())
      .then(d => { setResult(d); setLoading(false); })
      .catch(() => setLoading(false));
  };

  const patient = PATIENTS.find(p => p.id === patientId);
  const latest = vitals[vitals.length - 1] || {};

  return (
    <div style={{ fontFamily: "'Segoe UI', sans-serif", background: "#f8fafc", minHeight: "100vh" }}>
      {/* Header */}
      <div style={{ background: "#0f172a", color: "white", padding: "16px 32px", display: "flex", alignItems: "center", gap: 16 }}>
        <div style={{ fontSize: 22, fontWeight: 800 }}>🫀 CareWatch AI</div>
        <div style={{ fontSize: 13, color: "#94a3b8" }}>Chronic Disease Monitoring · IBM Granite + watsonx.ai</div>
      </div>

      <div style={{ maxWidth: 1000, margin: "0 auto", padding: "24px 16px" }}>
        {/* Patient selector */}
        <div style={{ display: "flex", gap: 10, marginBottom: 20, flexWrap: "wrap" }}>
          {PATIENTS.map(p => (
            <button key={p.id} onClick={() => setPatientId(p.id)} style={{
              padding: "8px 20px", borderRadius: 8, border: "none", cursor: "pointer", fontWeight: 600,
              background: patientId === p.id ? p.color : "#e2e8f0",
              color: patientId === p.id ? "white" : "#334155",
              transition: "all 0.15s",
            }}>
              {p.label} — {p.condition}
            </button>
          ))}
          <button onClick={runAnalysis} disabled={loading} style={{
            marginLeft: "auto", padding: "8px 24px", borderRadius: 8, border: "none",
            background: loading ? "#94a3b8" : "#0f6e56", color: "white",
            fontWeight: 700, cursor: loading ? "not-allowed" : "pointer", fontSize: 14,
          }}>
            {loading ? "⏳ Running agents..." : "▶ Run AI Analysis"}
          </button>
        </div>

        {/* Stat cards */}
        {latest.glucose && (
          <div style={{ display: "flex", gap: 12, marginBottom: 20, flexWrap: "wrap" }}>
            <StatCard label="Glucose"     value={latest.glucose}    unit="mg/dL" hi={140} lo={70} />
            <StatCard label="Systolic BP" value={latest.bp_sys}     unit="mmHg"  hi={120} lo={90} />
            <StatCard label="Heart Rate"  value={latest.heart_rate} unit="bpm"   hi={100} lo={60} />
            {summary && (
              <div style={{ background: "#f0f4ff", border: "1px solid #c7d2fe", borderRadius: 10, padding: "12px 16px", minWidth: 120 }}>
                <div style={{ fontSize: 11, color: "#666", marginBottom: 2 }}>Anomalies detected</div>
                <div style={{ fontSize: 22, fontWeight: 700, color: "#4338ca" }}>{summary.anomaly_count}</div>
                <div style={{ fontSize: 10, color: "#666" }}>of {summary.total_readings} readings</div>
              </div>
            )}
          </div>
        )}

        {/* Tabs */}
        <div style={{ display: "flex", gap: 0, marginBottom: 16, borderBottom: "2px solid #e2e8f0" }}>
          {["charts", "alerts"].map(tab => (
            <button key={tab} onClick={() => setActiveTab(tab)} style={{
              padding: "8px 20px", border: "none", background: "transparent", cursor: "pointer",
              fontWeight: 600, fontSize: 14, color: activeTab === tab ? patient.color : "#64748b",
              borderBottom: activeTab === tab ? `2px solid ${patient.color}` : "2px solid transparent",
              marginBottom: -2,
            }}>
              {tab === "charts" ? "📈 Vitals Charts" : "🔔 AI Alerts"}
            </button>
          ))}
        </div>

        {/* Charts tab */}
        {activeTab === "charts" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            {[
              { key: "glucose",    label: "Glucose (mg/dL)",    color: "#E85D24", hi: 140, lo: 70  },
              { key: "bp_sys",     label: "Systolic BP (mmHg)", color: "#185fa5", hi: 120, lo: 90  },
              { key: "heart_rate", label: "Heart Rate (bpm)",   color: "#6b30b8", hi: 100, lo: 60  },
            ].map(({ key, label, color, hi, lo }) => (
              <div key={key} style={{ background: "white", borderRadius: 12, padding: 20, boxShadow: "0 1px 3px rgba(0,0,0,.08)" }}>
                <div style={{ fontWeight: 700, marginBottom: 12, color: "#0f172a" }}>{label}</div>
                <ResponsiveContainer width="100%" height={180}>
                  <LineChart data={vitals}>
                    <XAxis dataKey="timestamp" hide />
                    <YAxis domain={[lo * 0.8, hi * 1.4]} width={45} />
                    <Tooltip formatter={v => [v.toFixed(1), label]} labelFormatter={() => ""} />
                    <ReferenceLine y={hi} stroke="#fca5a5" strokeDasharray="4 4" label={{ value: `Hi ${hi}`, fontSize: 10 }} />
                    <ReferenceLine y={lo} stroke="#86efac" strokeDasharray="4 4" label={{ value: `Lo ${lo}`, fontSize: 10 }} />
                    <Line type="monotone" dataKey={key} stroke={color} dot={false} strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            ))}
          </div>
        )}

        {/* Alerts tab */}
        {activeTab === "alerts" && (
          <div>
            {!result && !loading && (
              <div style={{ textAlign: "center", padding: 60, color: "#94a3b8" }}>
                Click <strong>Run AI Analysis</strong> to trigger the multi-agent pipeline.
              </div>
            )}
            {loading && (
              <div style={{ textAlign: "center", padding: 60, color: "#64748b" }}>
                <div style={{ fontSize: 32, marginBottom: 12 }}>⚙️</div>
                <div style={{ fontWeight: 600 }}>Running 4-agent pipeline…</div>
                <div style={{ fontSize: 13, marginTop: 8, color: "#94a3b8" }}>
                  Ingestion → Analysis → RAG Knowledge → Alert Generation
                </div>
              </div>
            )}
            {result && !loading && (
              <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                {/* Patient alert */}
                <div style={{ background: "#f0fdf4", border: "1px solid #86efac", borderRadius: 12, padding: 20 }}>
                  <div style={{ fontWeight: 700, color: "#065f46", marginBottom: 8, fontSize: 15 }}>
                    🙋 Patient Alert
                  </div>
                  <div style={{ color: "#1e293b", lineHeight: 1.7, whiteSpace: "pre-wrap" }}>
                    {result.alerts?.split("---DOCTOR_SUMMARY---")[0]
                      ?.replace("---PATIENT_ALERT---", "").trim() || result.alerts}
                  </div>
                </div>
                {/* Doctor summary */}
                <div style={{ background: "#eff6ff", border: "1px solid #93c5fd", borderRadius: 12, padding: 20 }}>
                  <div style={{ fontWeight: 700, color: "#1e40af", marginBottom: 8, fontSize: 15 }}>
                    🩺 Doctor Summary <RiskBadge text={result.risk_assessment} />
                  </div>
                  <div style={{ color: "#1e293b", lineHeight: 1.7, whiteSpace: "pre-wrap", fontFamily: "monospace", fontSize: 13 }}>
                    {result.alerts?.split("---DOCTOR_SUMMARY---")[1]?.trim() || ""}
                  </div>
                </div>
                {/* Clinical guidance */}
                {result.clinical_guidance && (
                  <div style={{ background: "#fefce8", border: "1px solid #fde047", borderRadius: 12, padding: 20 }}>
                    <div style={{ fontWeight: 700, color: "#854d0e", marginBottom: 8, fontSize: 15 }}>
                      📚 Evidence-Based Guidance
                    </div>
                    <div style={{ color: "#1e293b", lineHeight: 1.7, whiteSpace: "pre-wrap", fontSize: 13 }}>
                      {result.clinical_guidance}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
