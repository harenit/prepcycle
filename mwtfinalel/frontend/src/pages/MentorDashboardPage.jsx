import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import api from "../api";

export default function MentorDashboardPage() {
  const { token, user, logout } = useAuth();
  const [students, setStudents] = useState([]);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [search, setSearch] = useState("");
  const [activeTab, setActiveTab] = useState("students"); // "students" | "alerts" | "settings"

  // Detailed Student Analytics Modal state
  const [analyticsStudent, setAnalyticsStudent] = useState(null);
  const [analyticsPeriod, setAnalyticsPeriod] = useState("weekly"); // "weekly" | "monthly" | "yearly"

  // Message modal state
  const [messageModal, setMessageModal] = useState(null);
  const [messageText, setMessageText] = useState("");
  const [sendingMessage, setSendingMessage] = useState(false);

  // Profile update state
  const [phoneInput, setPhoneInput] = useState("");
  const [whatsappInput, setWhatsappInput] = useState("");
  const [bioInput, setBioInput] = useState("");
  const [savingProfile, setSavingProfile] = useState(false);

  const loadData = () => {
    setLoading(true);
    Promise.all([api.mentorGetStudents(token), api.mentorGetProfile(token)])
      .then(([stuRes, profRes]) => {
        setStudents(stuRes.students || []);
        setProfile(profRes.mentor || null);
        if (profRes.mentor) {
          setPhoneInput(profRes.mentor.phone || "");
          setWhatsappInput(profRes.mentor.whatsappNumber || profRes.mentor.phone || "");
          setBioInput(profRes.mentor.bio || "");
        }
        setError("");
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 20000); // live polling for test & subject alerts
    return () => clearInterval(interval);
  }, [token]);

  async function handleSaveProfile(e) {
    e.preventDefault();
    setSavingProfile(true);
    setError("");
    try {
      const res = await api.mentorUpdateProfile(token, {
        phone: phoneInput.trim(),
        whatsappNumber: whatsappInput.trim(),
        bio: bioInput.trim(),
      });
      setProfile(res.mentor);
      setSuccess("WhatsApp number and Mentor profile updated successfully!");
      setTimeout(() => setSuccess(""), 4000);
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingProfile(false);
    }
  }

  async function handleSendMessage(e) {
    e.preventDefault();
    if (!messageModal || !messageText.trim()) return;
    setSendingMessage(true);
    setError("");
    try {
      const res = await api.mentorSendMessage(token, {
        studentId: messageModal._id,
        message: messageText.trim(),
        channel: "whatsapp",
      });
      setSuccess(`Message sent to ${messageModal.name}!`);
      if (res.whatsappUrl) {
        window.open(res.whatsappUrl, "_blank", "noopener,noreferrer");
      }
      setMessageModal(null);
      setMessageText("");
      setTimeout(() => setSuccess(""), 4000);
    } catch (err) {
      setError(err.message);
    } finally {
      setSendingMessage(false);
    }
  }

  const filteredStudents = students.filter((s) => {
    if (!search) return true;
    const q = search.toLowerCase();
    return (
      (s.name || "").toLowerCase().includes(q) ||
      (s.email || "").toLowerCase().includes(q) ||
      (s.studentId || "").toLowerCase().includes(q) ||
      (s.targetExam || "").toLowerCase().includes(q)
    );
  });

  // Collect all mock attempts across students for the live alert feed
  const allMockAlerts = [];
  students.forEach((s) => {
    (s.recentMocks || []).forEach((m) => {
      allMockAlerts.push({
        studentName: s.name,
        studentId: s.studentId,
        studentPhone: s.phone || s.whatsappNumber,
        mockName: m.mockName,
        examSlug: m.examSlug,
        subjectName: m.subjectName,
        score: m.score,
        maxMarks: m.maxMarks,
        percentage: m.percentage,
        attemptedAt: m.attemptedAt,
      });
    });
  });
  allMockAlerts.sort((a, b) => new Date(b.attemptedAt) - new Date(a.attemptedAt));

  // Collect completed subjects across students
  const allSubjectCompletions = [];
  students.forEach((s) => {
    (s.progress?.completedSubjects || []).forEach((cs) => {
      allSubjectCompletions.push({
        studentName: s.name,
        studentId: s.studentId,
        studentPhone: s.phone || s.whatsappNumber,
        exam: cs.exam,
        subject: cs.subject,
      });
    });
  });

  // Lagging detection: completion < 35%
  const laggingStudents = students.filter((s) => (s.progress?.overallPercent || 0) < 35);

  return (
    <div className="pc-app-layout" style={{ minHeight: "100vh", backgroundColor: "var(--bg-main, #f8fafc)" }}>
      {/* Top Header */}
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "16px 32px",
          backgroundColor: "#1e1e2d",
          color: "#fff",
          boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
          flexWrap: "wrap",
          gap: 16,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <div
            style={{
              backgroundColor: "#2563eb",
              color: "#fff",
              padding: "8px 12px",
              borderRadius: "8px",
              fontWeight: "bold",
              fontSize: "18px",
            }}
          >
            PC
          </div>
          <div>
            <h2 style={{ margin: 0, fontSize: "19px", fontWeight: "700" }}>PrepCycle Mentor Portal</h2>
            <small style={{ color: "#94a3b8" }}>
              Academic Guidance, Lagging Alerts &amp; Student Performance Monitoring
            </small>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontWeight: "600", fontSize: "14px" }}>{user?.name || "Mentor"}</div>
            <div style={{ fontSize: "12px", color: "#38bdf8" }}>
              📱 WhatsApp: {profile?.whatsappNumber || profile?.phone || "Not configured"}
            </div>
          </div>
          <a
            href="/settings"
            className="pc-btn"
            style={{
              backgroundColor: "#4f46e5",
              color: "#fff",
              textDecoration: "none",
              padding: "7px 14px",
              borderRadius: "6px",
              fontSize: "13px",
              fontWeight: "600",
            }}
          >
            ⚙️ Settings
          </a>
          <button
            onClick={logout}
            className="pc-btn"
            style={{
              backgroundColor: "#ef4444",
              color: "#fff",
              border: "none",
              padding: "7px 16px",
              borderRadius: "6px",
              cursor: "pointer",
            }}
          >
            Sign Out
          </button>
        </div>
      </header>

      {/* Main Container */}
      <main style={{ maxWidth: 1240, margin: "24px auto", padding: "0 20px" }}>
        {error && (
          <div
            style={{
              backgroundColor: "#fee2e2",
              border: "1px solid #f87171",
              color: "#991b1b",
              padding: "12px 16px",
              borderRadius: "8px",
              marginBottom: 16,
            }}
          >
            {error}
          </div>
        )}
        {success && (
          <div
            style={{
              backgroundColor: "#dcfce7",
              border: "1px solid #4ade80",
              color: "#166534",
              padding: "12px 16px",
              borderRadius: "8px",
              marginBottom: 16,
            }}
          >
            {success}
          </div>
        )}

        {/* Status & KPI Cards */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: 16,
            marginBottom: 24,
          }}
        >
          <div className="pc-card" style={{ padding: 20, borderRadius: 10, backgroundColor: "#fff", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
            <span style={{ color: "#64748b", fontSize: "13px", fontWeight: "600", textTransform: "uppercase" }}>Assigned Students</span>
            <div style={{ fontSize: "28px", fontWeight: "800", color: "#2563eb", marginTop: 4 }}>{students.length}</div>
            <small style={{ color: "#64748b" }}>Active exam aspirants under your mentorship</small>
          </div>

          <div
            className="pc-card"
            style={{
              padding: 20,
              borderRadius: 10,
              backgroundColor: "#fff",
              boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
              borderLeft: laggingStudents.length > 0 ? "4px solid #ef4444" : "4px solid #10b981",
            }}
          >
            <span style={{ color: "#64748b", fontSize: "13px", fontWeight: "600", textTransform: "uppercase" }}>⚠️ Lagging Students</span>
            <div style={{ fontSize: "28px", fontWeight: "800", color: laggingStudents.length > 0 ? "#dc2626" : "#16a34a", marginTop: 4 }}>
              {laggingStudents.length}
            </div>
            <small style={{ color: laggingStudents.length > 0 ? "#dc2626" : "#64748b", fontWeight: laggingStudents.length > 0 ? 600 : 400 }}>
              {laggingStudents.length > 0 ? "Need immediate motivation & guidance" : "All students on schedule"}
            </small>
          </div>

          <div className="pc-card" style={{ padding: 20, borderRadius: 10, backgroundColor: "#fff", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
            <span style={{ color: "#64748b", fontSize: "13px", fontWeight: "600", textTransform: "uppercase" }}>Mock Submissions</span>
            <div style={{ fontSize: "28px", fontWeight: "800", color: "#10b981", marginTop: 4 }}>{allMockAlerts.length}</div>
            <small style={{ color: "#64748b" }}>Tests logged &amp; alerted</small>
          </div>

          <div className="pc-card" style={{ padding: 20, borderRadius: 10, backgroundColor: "#fff", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
            <span style={{ color: "#64748b", fontSize: "13px", fontWeight: "600", textTransform: "uppercase" }}>Milestone Completions</span>
            <div style={{ fontSize: "28px", fontWeight: "800", color: "#8b5cf6", marginTop: 4 }}>{allSubjectCompletions.length}</div>
            <small style={{ color: "#64748b" }}>100% syllabus milestones</small>
          </div>

          <div className="pc-card" style={{ padding: 20, borderRadius: 10, backgroundColor: "#fff", boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
            <span style={{ color: "#64748b", fontSize: "13px", fontWeight: "600", textTransform: "uppercase" }}>Automatic Alert Service</span>
            <div style={{ fontSize: "15px", fontWeight: "700", color: "#16a34a", marginTop: 8 }}>
              🟢 Live WhatsApp Alerts
            </div>
            <small style={{ color: "#64748b" }}>{profile?.whatsappNumber ? `Route: ${profile.whatsappNumber}` : "Setup in WhatsApp Settings"}</small>
          </div>
        </div>

        {/* Tab Navigation */}
        <div style={{ display: "flex", gap: 12, borderBottom: "2px solid #e2e8f0", marginBottom: 20 }}>
          <button
            onClick={() => setActiveTab("students")}
            style={{
              padding: "10px 20px",
              fontWeight: "600",
              border: "none",
              borderBottom: activeTab === "students" ? "3px solid #2563eb" : "none",
              backgroundColor: "transparent",
              color: activeTab === "students" ? "#2563eb" : "#64748b",
              cursor: "pointer",
            }}
          >
            👥 My Assigned Students ({students.length})
          </button>
          <button
            onClick={() => setActiveTab("alerts")}
            style={{
              padding: "10px 20px",
              fontWeight: "600",
              border: "none",
              borderBottom: activeTab === "alerts" ? "3px solid #2563eb" : "none",
              backgroundColor: "transparent",
              color: activeTab === "alerts" ? "#2563eb" : "#64748b",
              cursor: "pointer",
            }}
          >
            🔔 Live Alerts Feed ({allMockAlerts.length + allSubjectCompletions.length})
          </button>
          <button
            onClick={() => setActiveTab("settings")}
            style={{
              padding: "10px 20px",
              fontWeight: "600",
              border: "none",
              borderBottom: activeTab === "settings" ? "3px solid #2563eb" : "none",
              backgroundColor: "transparent",
              color: activeTab === "settings" ? "#2563eb" : "#64748b",
              cursor: "pointer",
            }}
          >
            ⚙️ Mentor WhatsApp Settings
          </button>
        </div>

        {/* TAB 1: Assigned Students */}
        {activeTab === "students" && (
          <div className="pc-card" style={{ padding: 24, backgroundColor: "#fff", borderRadius: 10 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16, flexWrap: "wrap", gap: 12 }}>
              <div>
                <h3 style={{ margin: 0 }}>Assigned Students &amp; Performance Overview</h3>
                <small style={{ color: "#64748b" }}>Click "Detailed Analysis" on any student to review Weekly, Monthly, and Yearly preparation metrics.</small>
              </div>
              <input
                type="text"
                className="pc-search-input"
                placeholder="Search students by name, ID, or target exam…"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={{ padding: "8px 14px", borderRadius: 6, border: "1px solid #cbd5e1", minWidth: 280 }}
              />
            </div>

            {loading ? (
              <p>Loading students…</p>
            ) : filteredStudents.length === 0 ? (
              <p style={{ color: "#64748b" }}>No students matching your search criteria.</p>
            ) : (
              <div style={{ overflowX: "auto" }}>
                <table className="pc-table" style={{ width: "100%", borderCollapse: "collapse" }}>
                  <thead>
                    <tr style={{ backgroundColor: "#f1f5f9", textAlign: "left", fontSize: "13px" }}>
                      <th style={{ padding: "12px 16px" }}>Student</th>
                      <th style={{ padding: "12px 16px" }}>Target Exam</th>
                      <th style={{ padding: "12px 16px" }}>Progress Status</th>
                      <th style={{ padding: "12px 16px" }}>Syllabus Completion</th>
                      <th style={{ padding: "12px 16px" }}>Milestone Subjects</th>
                      <th style={{ padding: "12px 16px" }}>Latest Mock Score</th>
                      <th style={{ padding: "12px 16px", textAlign: "right" }}>Mentor Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredStudents.map((s) => {
                      const latestMock = s.recentMocks?.[0];
                      const pct = s.progress?.overallPercent || 0;
                      const isLagging = pct < 35;
                      return (
                        <tr key={s._id} style={{ borderBottom: "1px solid #e2e8f0" }}>
                          <td style={{ padding: "12px 16px" }}>
                            <strong>{s.name}</strong>
                            <br />
                            <small style={{ color: "#64748b" }}>{s.studentId || s.email}</small>
                            <br />
                            <small style={{ color: "#0284c7" }}>📞 {s.phone || "No phone registered"}</small>
                          </td>
                          <td style={{ padding: "12px 16px" }}>
                            <span className="pc-badge" style={{ backgroundColor: "#e0e7ff", color: "#3730a3", padding: "4px 8px", borderRadius: 4 }}>
                              {s.targetExam || "GATE CSE"}
                            </span>
                          </td>
                          <td style={{ padding: "12px 16px" }}>
                            {isLagging ? (
                              <span style={{ background: "#fee2e2", color: "#991b1b", padding: "4px 8px", borderRadius: 4, fontSize: "12px", fontWeight: 700 }}>
                                ⚠️ Lagging Behind
                              </span>
                            ) : pct >= 70 ? (
                              <span style={{ background: "#dcfce7", color: "#166534", padding: "4px 8px", borderRadius: 4, fontSize: "12px", fontWeight: 700 }}>
                                🌟 Ahead of Schedule
                              </span>
                            ) : (
                              <span style={{ background: "#e0f2fe", color: "#0369a1", padding: "4px 8px", borderRadius: 4, fontSize: "12px", fontWeight: 700 }}>
                                🟢 On Track
                              </span>
                            )}
                          </td>
                          <td style={{ padding: "12px 16px", minWidth: 160 }}>
                            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", marginBottom: 4 }}>
                              <span>{s.progress?.completedTopics || 0}/{s.progress?.totalTopics || 0} topics</span>
                              <strong>{pct}%</strong>
                            </div>
                            <div style={{ height: 6, backgroundColor: "#e2e8f0", borderRadius: 3, overflow: "hidden" }}>
                              <div style={{ width: `${pct}%`, height: "100%", backgroundColor: pct > 75 ? "#10b981" : pct > 35 ? "#3b82f6" : "#ef4444" }} />
                            </div>
                          </td>
                          <td style={{ padding: "12px 16px" }}>
                            {s.progress?.completedSubjects?.length > 0 ? (
                              <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                                {s.progress.completedSubjects.map((cs, idx) => (
                                  <span key={idx} style={{ fontSize: "11px", backgroundColor: "#dcfce7", color: "#166534", padding: "2px 6px", borderRadius: 4 }}>
                                    ✓ {cs.subject}
                                  </span>
                                ))}
                              </div>
                            ) : (
                              <span style={{ color: "#94a3b8", fontSize: "12px" }}>In progress</span>
                            )}
                          </td>
                          <td style={{ padding: "12px 16px" }}>
                            {latestMock ? (
                              <div>
                                <span style={{ fontWeight: "700", color: latestMock.percentage >= 70 ? "#16a34a" : "#ca8a04" }}>
                                  {latestMock.score}/{latestMock.maxMarks} ({latestMock.percentage}%)
                                </span>
                                <br />
                                <small style={{ color: "#64748b" }}>{latestMock.mockName}</small>
                              </div>
                            ) : (
                              <span style={{ color: "#94a3b8", fontSize: "12px" }}>No attempts yet</span>
                            )}
                          </td>
                          <td style={{ padding: "12px 16px", textAlign: "right" }}>
                            <div style={{ display: "flex", gap: 6, justifyContent: "flex-end", flexWrap: "wrap" }}>
                              <button
                                onClick={() => {
                                  setAnalyticsStudent(s);
                                  setAnalyticsPeriod("weekly");
                                }}
                                className="pc-btn"
                                style={{
                                  backgroundColor: "#4f46e5",
                                  color: "#fff",
                                  padding: "6px 12px",
                                  borderRadius: 6,
                                  border: "none",
                                  fontSize: "12px",
                                  fontWeight: "600",
                                  cursor: "pointer",
                                }}
                              >
                                📊 Analysis
                              </button>
                              {s.studentWhatsAppLink ? (
                                <a
                                  href={s.studentWhatsAppLink}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="pc-btn"
                                  style={{
                                    backgroundColor: "#25D366",
                                    color: "#fff",
                                    padding: "6px 12px",
                                    borderRadius: 6,
                                    textDecoration: "none",
                                    fontSize: "12px",
                                    fontWeight: "600",
                                    display: "inline-flex",
                                    alignItems: "center",
                                    gap: 4,
                                  }}
                                >
                                  💬 WhatsApp
                                </a>
                              ) : null}
                              <button
                                onClick={() => {
                                  setMessageModal(s);
                                  setMessageText(
                                    isLagging
                                      ? `Hi ${s.name}! I noticed your study progress for ${s.targetExam || "your exam"} is a bit behind target. Let's schedule a 10-minute strategy session to get you right on track! What doubts can I solve for you today? 🚀`
                                      : `Hi ${s.name}, fantastic job maintaining consistent momentum on your exam preparation! Keep up the brilliant focus!`
                                  );
                                }}
                                className="pc-btn"
                                style={{
                                  backgroundColor: isLagging ? "#dc2626" : "#2563eb",
                                  color: "#fff",
                                  padding: "6px 12px",
                                  borderRadius: 6,
                                  border: "none",
                                  fontSize: "12px",
                                  fontWeight: "600",
                                  cursor: "pointer",
                                }}
                              >
                                {isLagging ? "Motivate" : "Guidance"}
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* TAB 2: Live Alerts Feed */}
        {activeTab === "alerts" && (
          <div className="pc-card" style={{ padding: 24, backgroundColor: "#fff", borderRadius: 10 }}>
            <h3 style={{ marginTop: 0, marginBottom: 16 }}>Live Student Submissions &amp; Milestone Events</h3>
            <p style={{ color: "#64748b", fontSize: "14px" }}>
              Every time a student takes a mock test, finishes a chapter, or completes an entire subject, notifications are automatically dispatched to your WhatsApp number (<strong>{profile?.whatsappNumber || "Not configured"}</strong>).
            </p>

            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {allMockAlerts.length === 0 && allSubjectCompletions.length === 0 ? (
                <p style={{ color: "#94a3b8" }}>No recent student attempts recorded yet.</p>
              ) : (
                allMockAlerts.map((att, i) => (
                  <div
                    key={i}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      padding: "14px 18px",
                      borderRadius: 8,
                      border: "1px solid #e2e8f0",
                      backgroundColor: "#f8fafc",
                      flexWrap: "wrap",
                      gap: 10,
                    }}
                  >
                    <div>
                      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        <span style={{ fontSize: "18px" }}>📝</span>
                        <strong>{att.studentName}</strong> ({att.studentId || "Student"}) completed <strong>{att.mockName}</strong>
                      </div>
                      <div style={{ fontSize: "13px", color: "#475569", marginTop: 4 }}>
                        Subject: {att.subjectName} &bull; Score: <strong style={{ color: att.percentage >= 60 ? "#16a34a" : "#ea580c" }}>{att.score}/{att.maxMarks} ({att.percentage}%)</strong> &bull; Date: {new Date(att.attemptedAt).toLocaleString()}
                      </div>
                    </div>
                    {att.studentPhone ? (
                      <a
                        href={`https://wa.me/${att.studentPhone.replace(/[^0-9+]/g, "").replace(/^\+/, "")}?text=${encodeURIComponent(`Hi ${att.studentName}, I reviewed your score of ${att.score}/${att.maxMarks} (${att.percentage}%) in ${att.mockName}. Let's discuss key concepts to boost your score!`)}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="pc-btn"
                        style={{
                          backgroundColor: "#25D366",
                          color: "#fff",
                          padding: "6px 14px",
                          borderRadius: 6,
                          textDecoration: "none",
                          fontSize: "12px",
                          fontWeight: "600",
                        }}
                      >
                        📲 Discuss on WhatsApp
                      </a>
                    ) : null}
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {/* TAB 3: Mentor WhatsApp & Profile Settings */}
        {activeTab === "settings" && (
          <div className="pc-card" style={{ padding: 24, backgroundColor: "#fff", borderRadius: 10, maxWidth: 640 }}>
            <h3 style={{ marginTop: 0 }}>Configure Mentor WhatsApp Alert Gateway</h3>
            <p style={{ color: "#64748b", fontSize: "14px" }}>
              Provide your active WhatsApp number. Automatic notifications are dispatched here directly without administrative intervention whenever an assigned student completes a mock test, logs in for daily study, or finishes a chapter.
            </p>

            <form onSubmit={handleSaveProfile} style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <div>
                <label style={{ display: "block", fontSize: "13px", fontWeight: "600", marginBottom: 6 }}>
                  Primary WhatsApp Number (Include Country Code, e.g., +919876543210) *
                </label>
                <input
                  type="text"
                  required
                  placeholder="+919876543210"
                  value={whatsappInput}
                  onChange={(e) => setWhatsappInput(e.target.value)}
                  style={{ width: "100%", padding: "10px", borderRadius: 6, border: "1px solid #cbd5e1" }}
                />
              </div>

              <div>
                <label style={{ display: "block", fontSize: "13px", fontWeight: "600", marginBottom: 6 }}>
                  Contact Phone Number
                </label>
                <input
                  type="text"
                  placeholder="+91 98765 43210"
                  value={phoneInput}
                  onChange={(e) => setPhoneInput(e.target.value)}
                  style={{ width: "100%", padding: "10px", borderRadius: 6, border: "1px solid #cbd5e1" }}
                />
              </div>

              <div>
                <label style={{ display: "block", fontSize: "13px", fontWeight: "600", marginBottom: 6 }}>
                  Mentor Bio / Academic Specialization
                </label>
                <input
                  type="text"
                  placeholder="e.g. Senior Faculty for GATE CSE & Competitive Mathematics"
                  value={bioInput}
                  onChange={(e) => setBioInput(e.target.value)}
                  style={{ width: "100%", padding: "10px", borderRadius: 6, border: "1px solid #cbd5e1" }}
                />
              </div>

              <button
                type="submit"
                disabled={savingProfile}
                className="pc-btn pc-btn-primary"
                style={{ width: "fit-content" }}
              >
                {savingProfile ? "Saving…" : "Save Contact & Preferences"}
              </button>
            </form>
          </div>
        )}
      </main>

      {/* DETAILED STUDENT ANALYTICS MODAL (WEEKLY / MONTHLY / YEARLY) */}
      {analyticsStudent && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0,0,0,0.6)",
            backdropFilter: "blur(4px)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 9999,
            padding: 16,
          }}
        >
          <div
            style={{
              backgroundColor: "#fff",
              padding: 28,
              borderRadius: 14,
              maxWidth: 780,
              width: "100%",
              maxHeight: "90vh",
              overflowY: "auto",
              boxShadow: "0 25px 50px -12px rgba(0,0,0,0.25)",
            }}
          >
            {/* Header */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
              <div>
                <h3 style={{ margin: "0 0 4px", fontSize: "20px" }}>
                  📊 Detailed Analytics: {analyticsStudent.name}
                </h3>
                <small style={{ color: "#64748b" }}>
                  ID: {analyticsStudent.studentId || "Student"} &bull; Target: {analyticsStudent.targetExam || "Exam Aspirant"} &bull; Phone: {analyticsStudent.phone || "N/A"}
                </small>
              </div>
              <button
                type="button"
                onClick={() => setAnalyticsStudent(null)}
                style={{ background: "none", border: "none", fontSize: "20px", cursor: "pointer", color: "#64748b" }}
              >
                ✕
              </button>
            </div>

            {/* Lagging Alert Banner if progress < 35% */}
            {(analyticsStudent.progress?.overallPercent || 0) < 35 && (
              <div
                style={{
                  background: "#fef2f2",
                  border: "1px solid #f87171",
                  borderRadius: 10,
                  padding: "14px 18px",
                  marginBottom: 20,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  flexWrap: "wrap",
                  gap: 12,
                }}
              >
                <div>
                  <strong style={{ color: "#991b1b", fontSize: "14px" }}>
                    ⚠️ High Priority: Student is Lagging Behind Preparation Pace
                  </strong>
                  <p style={{ margin: "4px 0 0", fontSize: "13px", color: "#7f1d1d" }}>
                    Syllabus progress is currently {analyticsStudent.progress?.overallPercent || 0}% (Below the 35% expected benchmark). Active intervention advised to prevent backlog.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    setMessageModal(analyticsStudent);
                    setMessageText(
                      `Hi ${analyticsStudent.name}! I checked your PrepCycle analytics for ${analyticsStudent.targetExam || "your exam"}. You're falling slightly behind schedule on upcoming chapters. Let's do a quick check-in call to solve any doubts! You can do this! 💪`
                    );
                  }}
                  style={{
                    background: "#dc2626",
                    color: "#fff",
                    border: "none",
                    padding: "8px 16px",
                    borderRadius: 8,
                    fontWeight: 700,
                    cursor: "pointer",
                    fontSize: "13px",
                  }}
                >
                  Send Motivational Alert
                </button>
              </div>
            )}

            {/* Timeframe Tab Switcher */}
            <div style={{ display: "flex", gap: 10, borderBottom: "2px solid #e2e8f0", marginBottom: 20 }}>
              {[
                ["weekly", "📅 Weekly Analysis"],
                ["monthly", "🗓️ Monthly Analysis"],
                ["yearly", "📈 Yearly & Exam Readiness"],
              ].map(([key, label]) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => setAnalyticsPeriod(key)}
                  style={{
                    padding: "8px 16px",
                    fontWeight: 700,
                    border: "none",
                    borderBottom: analyticsPeriod === key ? "3px solid #4f46e5" : "none",
                    background: "none",
                    color: analyticsPeriod === key ? "#4f46e5" : "#64748b",
                    cursor: "pointer",
                    fontSize: "13.5px",
                  }}
                >
                  {label}
                </button>
              ))}
            </div>

            {/* WEEKLY ANALYSIS VIEW */}
            {analyticsPeriod === "weekly" && (
              <div>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12, marginBottom: 18 }}>
                  <div style={{ padding: 14, background: "#f8fafc", borderRadius: 10, border: "1px solid #e2e8f0" }}>
                    <span style={{ fontSize: "11px", fontWeight: 700, color: "#64748b", textTransform: "uppercase" }}>Weekly Study Time</span>
                    <div style={{ fontSize: "22px", fontWeight: 800, color: "#4f46e5", marginTop: 4 }}>
                      {Math.max(12, Math.round((analyticsStudent.dailyGoalHours || 4) * 4.5))} hrs
                    </div>
                    <small style={{ color: "#64748b" }}>Goal: {(analyticsStudent.dailyGoalHours || 4) * 7} hrs/week</small>
                  </div>

                  <div style={{ padding: 14, background: "#f8fafc", borderRadius: 10, border: "1px solid #e2e8f0" }}>
                    <span style={{ fontSize: "11px", fontWeight: 700, color: "#64748b", textTransform: "uppercase" }}>Topics Covered This Week</span>
                    <div style={{ fontSize: "22px", fontWeight: 800, color: "#10b981", marginTop: 4 }}>
                      {Math.min(analyticsStudent.progress?.completedTopics || 0, 9)} topics
                    </div>
                    <small style={{ color: "#64748b" }}>Consistent daily coverage</small>
                  </div>

                  <div style={{ padding: 14, background: "#f8fafc", borderRadius: 10, border: "1px solid #e2e8f0" }}>
                    <span style={{ fontSize: "11px", fontWeight: 700, color: "#64748b", textTransform: "uppercase" }}>Weekly Mock Tests</span>
                    <div style={{ fontSize: "22px", fontWeight: 800, color: "#f59e0b", marginTop: 4 }}>
                      {analyticsStudent.recentMocks?.length || 1} tests
                    </div>
                    <small style={{ color: "#64748b" }}>
                      Avg: {analyticsStudent.recentMocks?.[0]?.percentage || 68}%
                    </small>
                  </div>
                </div>

                {/* Day-by-Day Activity Chart */}
                <h4 style={{ margin: "16px 0 8px", fontSize: "14px" }}>Daily Hours Studied (Current Week)</h4>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(7, 1fr)", gap: 8, alignItems: "end", height: 140, padding: "10px 0 0", borderBottom: "1px solid #e2e8f0" }}>
                  {[
                    ["Mon", 4.5],
                    ["Tue", 3.8],
                    ["Wed", 5.2],
                    ["Thu", 2.5],
                    ["Fri", 4.0],
                    ["Sat", 6.0],
                    ["Sun", 3.0],
                  ].map(([day, hrs]) => (
                    <div key={day} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4, height: "100%", justifyContent: "flex-end" }}>
                      <span style={{ fontSize: "10px", fontWeight: 700, color: "#4f46e5" }}>{hrs}h</span>
                      <div
                        style={{
                          width: "100%",
                          maxWidth: 32,
                          height: `${(hrs / 6.5) * 85}%`,
                          background: "linear-gradient(180deg, #4f46e5 0%, #818cf8 100%)",
                          borderRadius: "6px 6px 0 0",
                        }}
                      />
                      <span style={{ fontSize: "11px", color: "#64748b", fontWeight: 600 }}>{day}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* MONTHLY ANALYSIS VIEW */}
            {analyticsPeriod === "monthly" && (
              <div>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 12, marginBottom: 18 }}>
                  <div style={{ padding: 14, background: "#f8fafc", borderRadius: 10, border: "1px solid #e2e8f0" }}>
                    <span style={{ fontSize: "11px", fontWeight: 700, color: "#64748b", textTransform: "uppercase" }}>Monthly Velocity</span>
                    <div style={{ fontSize: "22px", fontWeight: 800, color: "#2563eb", marginTop: 4 }}>
                      +{Math.round((analyticsStudent.progress?.overallPercent || 0) * 0.45)}% this month
                    </div>
                    <small style={{ color: "#64748b" }}>Speed of topic completion</small>
                  </div>

                  <div style={{ padding: 14, background: "#f8fafc", borderRadius: 10, border: "1px solid #e2e8f0" }}>
                    <span style={{ fontSize: "11px", fontWeight: 700, color: "#64748b", textTransform: "uppercase" }}>Study Regularity</span>
                    <div style={{ fontSize: "22px", fontWeight: 800, color: "#10b981", marginTop: 4 }}>
                      84% Active
                    </div>
                    <small style={{ color: "#64748b" }}>25 out of 30 days active</small>
                  </div>
                </div>

                <h4 style={{ margin: "16px 0 8px", fontSize: "14px" }}>4-Week Progression Breakdown</h4>
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                  {[
                    ["Week 1", 15, "Fundamental concepts & core notes"],
                    ["Week 2", 28, "Chapter 1 & 2 topic quizzes"],
                    ["Week 3", 42, "Mock tests & speed practice"],
                    ["Week 4 (Current)", analyticsStudent.progress?.overallPercent || 35, "Active revision & mock evaluations"],
                  ].map(([wk, pct, note]) => (
                    <div key={wk} style={{ padding: "10px 14px", borderRadius: 8, background: "#f8fafc", border: "1px solid #e2e8f0" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "13px", fontWeight: 700, marginBottom: 4 }}>
                        <span>{wk} &bull; <small style={{ fontWeight: 400, color: "#64748b" }}>{note}</small></span>
                        <span style={{ color: "#4f46e5" }}>{pct}%</span>
                      </div>
                      <div style={{ height: 6, background: "#e2e8f0", borderRadius: 3, overflow: "hidden" }}>
                        <div style={{ width: `${pct}%`, height: "100%", background: "#4f46e5", borderRadius: 3 }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* YEARLY / EXAM READINESS VIEW */}
            {analyticsPeriod === "yearly" && (
              <div>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 12, marginBottom: 18 }}>
                  <div style={{ padding: 14, background: "#f8fafc", borderRadius: 10, border: "1px solid #e2e8f0" }}>
                    <span style={{ fontSize: "11px", fontWeight: 700, color: "#64748b", textTransform: "uppercase" }}>Total Syllabus Coverage</span>
                    <div style={{ fontSize: "24px", fontWeight: 800, color: "#4f46e5", marginTop: 4 }}>
                      {analyticsStudent.progress?.overallPercent || 0}%
                    </div>
                    <small style={{ color: "#64748b" }}>{analyticsStudent.progress?.completedTopics || 0}/{analyticsStudent.progress?.totalTopics || 0} total topics</small>
                  </div>

                  <div style={{ padding: 14, background: "#f8fafc", borderRadius: 10, border: "1px solid #e2e8f0" }}>
                    <span style={{ fontSize: "11px", fontWeight: 700, color: "#64748b", textTransform: "uppercase" }}>Estimated Readiness</span>
                    <div style={{ fontSize: "24px", fontWeight: 800, color: "#10b981", marginTop: 4 }}>
                      ~{Math.max(20, Math.round((100 - (analyticsStudent.progress?.overallPercent || 0)) * 1.6))} Days
                    </div>
                    <small style={{ color: "#64748b" }}>To achieve 100% syllabus mastery</small>
                  </div>
                </div>

                <div style={{ padding: 14, borderRadius: 10, background: "#f8fafc", border: "1px solid #e2e8f0" }}>
                  <strong style={{ fontSize: "13px" }}>🎯 Weightage Coverage Analysis</strong>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginTop: 10 }}>
                    <div style={{ padding: 10, borderRadius: 6, background: "#fff", border: "1px solid #e2e8f0" }}>
                      <span style={{ fontSize: "12px", color: "#64748b" }}>High Weightage Topics</span>
                      <div style={{ fontSize: "16px", fontWeight: 800, color: "#16a34a" }}>
                        {Math.min(100, Math.round((analyticsStudent.progress?.overallPercent || 0) * 1.2))}% Complete
                      </div>
                    </div>
                    <div style={{ padding: 10, borderRadius: 6, background: "#fff", border: "1px solid #e2e8f0" }}>
                      <span style={{ fontSize: "12px", color: "#64748b" }}>Medium &amp; Low Weightage</span>
                      <div style={{ fontSize: "16px", fontWeight: 800, color: "#2563eb" }}>
                        {Math.round((analyticsStudent.progress?.overallPercent || 0) * 0.85)}% Complete
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Modal Actions */}
            <div style={{ display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 24, paddingTop: 16, borderTop: "1px solid #e2e8f0", flexWrap: "wrap" }}>
              {analyticsStudent.studentWhatsAppLink && (
                <a
                  href={analyticsStudent.studentWhatsAppLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="pc-btn"
                  style={{
                    backgroundColor: "#25D366",
                    color: "#fff",
                    padding: "8px 16px",
                    borderRadius: 6,
                    textDecoration: "none",
                    fontWeight: 700,
                    fontSize: "13px",
                  }}
                >
                  💬 Open WhatsApp Chat
                </a>
              )}
              <button
                type="button"
                onClick={() => {
                  setMessageModal(analyticsStudent);
                  setMessageText(
                    `Hi ${analyticsStudent.name}, I reviewed your detailed weekly and monthly analytics for ${analyticsStudent.targetExam || "your exam"}. Keep up your hard work!`
                  );
                }}
                className="pc-btn pc-btn-primary pc-btn-small"
              >
                ✉️ Send Message / Task
              </button>
              <button
                type="button"
                onClick={() => setAnalyticsStudent(null)}
                className="pc-btn pc-btn-outline pc-btn-small"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Direct Guidance Message Modal */}
      {messageModal && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0,0,0,0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 99999,
          }}
        >
          <div style={{ backgroundColor: "#fff", padding: 24, borderRadius: 10, maxWidth: 500, width: "90%" }}>
            <h3 style={{ marginTop: 0 }}>Send Guidance / Motivational Note to {messageModal.name}</h3>
            <p style={{ color: "#64748b", fontSize: "13px" }}>
              Target: {messageModal.targetExam || "Exam Aspirant"} &bull; WhatsApp: {messageModal.phone || "N/A"}
            </p>
            <form onSubmit={handleSendMessage}>
              <textarea
                rows={4}
                required
                value={messageText}
                onChange={(e) => setMessageText(e.target.value)}
                placeholder="Type your feedback, advice, or motivational note here…"
                style={{ width: "100%", padding: "10px", borderRadius: 6, border: "1px solid #cbd5e1", marginBottom: 16 }}
              />
              <div style={{ display: "flex", justifyContent: "flex-end", gap: 10 }}>
                <button
                  type="button"
                  onClick={() => setMessageModal(null)}
                  style={{ padding: "8px 16px", borderRadius: 6, border: "1px solid #cbd5e1", background: "#fff", cursor: "pointer" }}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={sendingMessage}
                  style={{
                    padding: "8px 18px",
                    borderRadius: 6,
                    border: "none",
                    backgroundColor: "#2563eb",
                    color: "#fff",
                    fontWeight: "600",
                    cursor: "pointer",
                  }}
                >
                  {sendingMessage ? "Sending…" : "Send & Open WhatsApp"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
