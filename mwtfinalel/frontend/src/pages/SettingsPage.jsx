import { useEffect, useState } from "react";
import AppLayout from "../components/AppLayout";
import { useAuth } from "../context/AuthContext";
import { useLanguage } from "../context/LanguageContext";
import api from "../api";

const DEFAULT_PALETTE = {
  buttonColor: "#4f46e5",
  textColor: "#0f172a",
  bgColor: "#f8fafc",
  surfaceColor: "#ffffff",
};

const PRESET_PALETTES = [
  { name: "⚡ Electric Indigo (Default)", buttonColor: "#4f46e5", textColor: "#0f172a", bgColor: "#f8fafc", surfaceColor: "#ffffff" },
  { name: "🌊 Ocean Blue", buttonColor: "#0284c7", textColor: "#0f172a", bgColor: "#f0f9ff", surfaceColor: "#ffffff" },
  { name: "🌲 Emerald Growth", buttonColor: "#059669", textColor: "#064e3b", bgColor: "#f0fdf4", surfaceColor: "#ffffff" },
  { name: "🔮 Royal Violet", buttonColor: "#7c3aed", textColor: "#1e1b4b", bgColor: "#faf5ff", surfaceColor: "#ffffff" },
  { name: "🌅 Sunset Amber", buttonColor: "#ea580c", textColor: "#431407", bgColor: "#fff7ed", surfaceColor: "#ffffff" },
  { name: "🌑 Midnight Dark", buttonColor: "#6366f1", textColor: "#f8fafc", bgColor: "#090d16", surfaceColor: "#111827" },
];

export default function SettingsPage() {
  const { user, token } = useAuth();
  const { lang, setLang, t } = useLanguage();

  const [theme, setTheme] = useState(() => localStorage.getItem("prepcycle_theme") || "light");
  const [font, setFont] = useState(() => localStorage.getItem("prepcycle_font") || "medium");

  // Custom live color palette state
  const [customPalette, setCustomPalette] = useState(() => {
    try {
      const saved = JSON.parse(localStorage.getItem("prepcycle_custom_palette") || "null");
      return saved ? { ...DEFAULT_PALETTE, ...saved } : DEFAULT_PALETTE;
    } catch {
      return DEFAULT_PALETTE;
    }
  });

  const [paletteSavedMsg, setPaletteSavedMsg] = useState("");

  // Profile form state (role-aware)
  const [profile, setProfile] = useState({
    name: user?.name || "",
    phone: user?.phone || user?.whatsappNumber || "",
    whatsappNumber: user?.whatsappNumber || user?.phone || "",
    targetExam: user?.targetExam || "GATE CSE",
    college: user?.college || "",
    state: user?.state || "",
    dailyGoalHours: user?.dailyGoalHours || 4,
    bio: user?.bio || "",
  });
  const [profileSaving, setProfileSaving] = useState(false);
  const [profileMsg, setProfileMsg] = useState({ text: "", error: false });

  // Change password state
  const [passwords, setPasswords] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });
  const [passSaving, setPassSaving] = useState(false);
  const [passMsg, setPassMsg] = useState({ text: "", error: false });

  useEffect(() => {
    if (user) {
      setProfile({
        name: user.name || "",
        phone: user.phone || user.whatsappNumber || "",
        whatsappNumber: user.whatsappNumber || user.phone || "",
        targetExam: user.targetExam || "GATE CSE",
        college: user.college || "",
        state: user.state || "",
        dailyGoalHours: user.dailyGoalHours || 4,
        bio: user.bio || "",
      });
    }
  }, [user]);

  // Apply custom palette to document in real time
  const applyPalette = (palette) => {
    document.documentElement.style.setProperty("--pc-primary", palette.buttonColor);
    document.documentElement.style.setProperty("--pc-primary-dark", palette.buttonColor);
    document.documentElement.style.setProperty("--pc-text", palette.textColor);
    document.documentElement.style.setProperty("--pc-bg", palette.bgColor);
    document.documentElement.style.setProperty("--pc-surface", palette.surfaceColor);
    localStorage.setItem("prepcycle_custom_palette", JSON.stringify(palette));
  };

  const handlePaletteColorChange = (key, val) => {
    const updated = { ...customPalette, [key]: val };
    setCustomPalette(updated);
    applyPalette(updated);
    setPaletteSavedMsg("✓ Live palette applied to entire application!");
    setTimeout(() => setPaletteSavedMsg(""), 3500);
  };

  const handleApplyPreset = (preset) => {
    const updated = {
      buttonColor: preset.buttonColor,
      textColor: preset.textColor,
      bgColor: preset.bgColor,
      surfaceColor: preset.surfaceColor,
    };
    setCustomPalette(updated);
    applyPalette(updated);
    setPaletteSavedMsg(`✓ Applied preset "${preset.name}"!`);
    setTimeout(() => setPaletteSavedMsg(""), 3500);
  };

  const handleResetPalette = () => {
    setCustomPalette(DEFAULT_PALETTE);
    applyPalette(DEFAULT_PALETTE);
    setPaletteSavedMsg("✓ Restored default PrepCycle color palette.");
    setTimeout(() => setPaletteSavedMsg(""), 3500);
  };

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("prepcycle_theme", theme);
  }, [theme]);

  useEffect(() => {
    document.documentElement.dataset.font = font;
    localStorage.setItem("prepcycle_font", font);
  }, [font]);

  async function handleProfileSubmit(e) {
    e.preventDefault();
    setProfileSaving(true);
    setProfileMsg({ text: "", error: false });
    try {
      await api.updateProfile(token, profile);
      setProfileMsg({ text: "Profile details saved successfully!", error: false });
      setTimeout(() => setProfileMsg({ text: "", error: false }), 4000);
    } catch (err) {
      setProfileMsg({ text: err.message || "Failed to update profile.", error: true });
    } finally {
      setProfileSaving(false);
    }
  }

  async function handlePasswordSubmit(e) {
    e.preventDefault();
    if (passwords.newPassword !== passwords.confirmPassword) {
      return setPassMsg({ text: "New password and confirmation do not match.", error: true });
    }
    if (passwords.newPassword.length < 6) {
      return setPassMsg({ text: "Password must be at least 6 characters long.", error: true });
    }
    setPassSaving(true);
    setPassMsg({ text: "", error: false });
    try {
      await api.changePassword(token, {
        currentPassword: passwords.currentPassword,
        newPassword: passwords.newPassword,
      });
      setPassMsg({ text: "Password updated successfully!", error: false });
      setPasswords({ currentPassword: "", newPassword: "", confirmPassword: "" });
      setTimeout(() => setPassMsg({ text: "", error: false }), 4000);
    } catch (err) {
      setPassMsg({ text: err.message || "Failed to change password.", error: true });
    } finally {
      setPassSaving(false);
    }
  }

  const roleLabel =
    user?.role === "mentor"
      ? "Academic Mentor"
      : user?.role === "admin"
      ? "Platform Administrator"
      : user?.role === "delivery"
      ? "Delivery Partner"
      : "Student Aspirant";

  return (
    <AppLayout>
      <div className="pc-page">
        <header className="pc-page-header">
          <div>
            <h1>⚙️ {t("settings", "Settings & Personalization")}</h1>
            <p className="pc-page-subtitle">
              Configure personal profile, custom website color palette, typography, and account security. Available for all roles.
            </p>
          </div>
          <div>
            <span
              className={
                user?.role === "mentor"
                  ? "pc-badge pc-badge-mentor"
                  : user?.role === "admin"
                  ? "pc-badge pc-badge-admin"
                  : user?.role === "delivery"
                  ? "pc-badge pc-badge-delivery"
                  : "pc-badge pc-badge-student"
              }
              style={{ fontSize: "13px", padding: "6px 14px" }}
            >
              Logged in as: {roleLabel}
            </span>
          </div>
        </header>

        <div style={{ display: "grid", gap: 24, maxWidth: 840 }}>
          {/* CUSTOM LIVE COLOR PALETTE STYLER (HIGH PRIORITY USER REQUEST) */}
          <div className="pc-card">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 10 }}>
              <div>
                <h3 style={{ margin: 0 }}>🎨 Custom Color Palette &amp; Website Styler</h3>
                <p className="pc-card-note" style={{ marginTop: 4 }}>
                  Customize the button color, text color, background color, and card surface of the entire website to your choice.
                </p>
              </div>
              <button
                type="button"
                className="pc-btn pc-btn-outline pc-btn-small"
                onClick={handleResetPalette}
              >
                ↺ Reset to Default
              </button>
            </div>

            {paletteSavedMsg && (
              <div style={{ background: "#d1fae5", color: "#065f46", padding: "8px 12px", borderRadius: 8, fontSize: "13px", fontWeight: 700, margin: "14px 0" }}>
                {paletteSavedMsg}
              </div>
            )}

            {/* Preset Palettes */}
            <div style={{ marginTop: 16 }}>
              <span style={{ fontSize: "12px", fontWeight: 700, color: "var(--pc-text-muted)", textTransform: "uppercase", letterSpacing: "0.04em" }}>
                Quick Preset Themes:
              </span>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 8 }}>
                {PRESET_PALETTES.map((preset) => (
                  <button
                    key={preset.name}
                    type="button"
                    onClick={() => handleApplyPreset(preset)}
                    className="pc-btn pc-btn-small pc-btn-outline"
                    style={{
                      borderLeft: `5px solid ${preset.buttonColor}`,
                      fontSize: "12px",
                      padding: "6px 12px",
                    }}
                  >
                    {preset.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Interactive Color Pickers */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 14, marginTop: 18 }}>
              {/* Button Color */}
              <div style={{ padding: 12, border: "1px solid var(--pc-border)", borderRadius: 10, background: "var(--pc-surface-subtle, #f8fafc)" }}>
                <label style={{ fontSize: "12.5px", fontWeight: 700, display: "block", marginBottom: 6 }}>
                  🔘 Button &amp; Accent Color
                </label>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <input
                    type="color"
                    value={customPalette.buttonColor}
                    onChange={(e) => handlePaletteColorChange("buttonColor", e.target.value)}
                    style={{ width: 44, height: 36, border: "none", borderRadius: 6, cursor: "pointer", padding: 0 }}
                  />
                  <input
                    type="text"
                    value={customPalette.buttonColor}
                    onChange={(e) => handlePaletteColorChange("buttonColor", e.target.value)}
                    style={{ flex: 1, padding: "6px 8px", fontSize: "12px", borderRadius: 6, border: "1px solid var(--pc-border)" }}
                  />
                </div>
              </div>

              {/* Text Color */}
              <div style={{ padding: 12, border: "1px solid var(--pc-border)", borderRadius: 10, background: "var(--pc-surface-subtle, #f8fafc)" }}>
                <label style={{ fontSize: "12.5px", fontWeight: 700, display: "block", marginBottom: 6 }}>
                  ✏️ Text &amp; Heading Color
                </label>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <input
                    type="color"
                    value={customPalette.textColor}
                    onChange={(e) => handlePaletteColorChange("textColor", e.target.value)}
                    style={{ width: 44, height: 36, border: "none", borderRadius: 6, cursor: "pointer", padding: 0 }}
                  />
                  <input
                    type="text"
                    value={customPalette.textColor}
                    onChange={(e) => handlePaletteColorChange("textColor", e.target.value)}
                    style={{ flex: 1, padding: "6px 8px", fontSize: "12px", borderRadius: 6, border: "1px solid var(--pc-border)" }}
                  />
                </div>
              </div>

              {/* Background Color */}
              <div style={{ padding: 12, border: "1px solid var(--pc-border)", borderRadius: 10, background: "var(--pc-surface-subtle, #f8fafc)" }}>
                <label style={{ fontSize: "12.5px", fontWeight: 700, display: "block", marginBottom: 6 }}>
                  🖼️ Website Background Color
                </label>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <input
                    type="color"
                    value={customPalette.bgColor}
                    onChange={(e) => handlePaletteColorChange("bgColor", e.target.value)}
                    style={{ width: 44, height: 36, border: "none", borderRadius: 6, cursor: "pointer", padding: 0 }}
                  />
                  <input
                    type="text"
                    value={customPalette.bgColor}
                    onChange={(e) => handlePaletteColorChange("bgColor", e.target.value)}
                    style={{ flex: 1, padding: "6px 8px", fontSize: "12px", borderRadius: 6, border: "1px solid var(--pc-border)" }}
                  />
                </div>
              </div>

              {/* Card Surface Color */}
              <div style={{ padding: 12, border: "1px solid var(--pc-border)", borderRadius: 10, background: "var(--pc-surface-subtle, #f8fafc)" }}>
                <label style={{ fontSize: "12.5px", fontWeight: 700, display: "block", marginBottom: 6 }}>
                  🃏 Card / Container Surface
                </label>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <input
                    type="color"
                    value={customPalette.surfaceColor}
                    onChange={(e) => handlePaletteColorChange("surfaceColor", e.target.value)}
                    style={{ width: 44, height: 36, border: "none", borderRadius: 6, cursor: "pointer", padding: 0 }}
                  />
                  <input
                    type="text"
                    value={customPalette.surfaceColor}
                    onChange={(e) => handlePaletteColorChange("surfaceColor", e.target.value)}
                    style={{ flex: 1, padding: "6px 8px", fontSize: "12px", borderRadius: 6, border: "1px solid var(--pc-border)" }}
                  />
                </div>
              </div>
            </div>

            {/* Live Interactive Preview */}
            <div
              style={{
                marginTop: 20,
                padding: 16,
                borderRadius: 12,
                border: "1px dashed var(--pc-border)",
                background: customPalette.bgColor,
              }}
            >
              <div style={{ fontSize: "12px", fontWeight: 800, color: customPalette.textColor, marginBottom: 8 }}>
                Live Palette Preview:
              </div>
              <div
                style={{
                  background: customPalette.surfaceColor,
                  color: customPalette.textColor,
                  padding: 14,
                  borderRadius: 10,
                  boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  flexWrap: "wrap",
                  gap: 10,
                }}
              >
                <div>
                  <h4 style={{ margin: "0 0 4px", color: customPalette.textColor }}>PrepCycle Card Component</h4>
                  <p style={{ margin: 0, fontSize: "13px", opacity: 0.8, color: customPalette.textColor }}>
                    This demonstrates how your buttons, text, cards, and backgrounds dynamically adapt.
                  </p>
                </div>
                <button
                  type="button"
                  style={{
                    background: customPalette.buttonColor,
                    color: "#ffffff",
                    border: "none",
                    padding: "8px 16px",
                    borderRadius: 8,
                    fontWeight: 700,
                    cursor: "pointer",
                  }}
                >
                  Sample Button
                </button>
              </div>
            </div>
          </div>

          {/* THEME & ACCESSIBILITY SECTION */}
          <div className="pc-card pc-form">
            <h3>🌓 {t("appearance", "Theme Mode & Typography")}</h3>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
              <label>
                {t("theme", "Theme Mode")}
                <select value={theme} onChange={(e) => setTheme(e.target.value)}>
                  <option value="light">{t("light", "Light Mode")}</option>
                  <option value="dark">{t("dark", "Dark Mode")}</option>
                </select>
              </label>

              <label>
                {t("fontSize", "Application Font Size")}
                <select value={font} onChange={(e) => setFont(e.target.value)}>
                  <option value="small">{t("small", "Small (92%)")}</option>
                  <option value="medium">{t("medium", "Normal / Default (100%)")}</option>
                  <option value="large">{t("large", "Large — High Comfort (118%)")}</option>
                  <option value="xlarge">Extra Large — Maximum Visibility (135%)</option>
                </select>
              </label>
            </div>
          </div>

          {/* LANGUAGE SECTION */}
          <div className="pc-card pc-form">
            <h3>🌐 {t("language", "Language Selection")}</h3>
            <label>
              Application Interface Language (Available for all roles)
              <select value={lang} onChange={(e) => setLang(e.target.value)}>
                <option value="en">English (English)</option>
                <option value="ta">தமிழ் (Tamil)</option>
                <option value="hi">हिन्दी (Hindi)</option>
                <option value="te">తెలుగు (Telugu)</option>
                <option value="ml">മലയാളം (Malayalam)</option>
                <option value="kn">ಕನ್ನಡ (Kannada)</option>
                <option value="bn">বাংলা (Bengali)</option>
                <option value="mr">मराठी (Marathi)</option>
              </select>
            </label>
          </div>

          {/* USER PROFILE DETAILS SECTION */}
          <div className="pc-card">
            <h3>👤 {t("account", "Account")} &amp; {t("profileInfo", "Profile Details")}</h3>
            <p className="pc-card-note">
              {user?.role === "mentor"
                ? "Manage your academic mentor credentials and WhatsApp contact number for student alerts."
                : user?.role === "admin"
                ? "Platform administrator profile details."
                : user?.role === "delivery"
                ? "Delivery partner contact phone and service dispatch details."
                : "Manage your student identity, target examination, and daily study schedule."}
            </p>

            <form onSubmit={handleProfileSubmit} className="pc-form" style={{ marginTop: 14 }}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                <label>
                  Full Name
                  <input
                    type="text"
                    required
                    value={profile.name}
                    onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                    placeholder="Your Full Name"
                  />
                </label>

                <label>
                  Email Address
                  <input
                    type="email"
                    disabled
                    value={user?.email || ""}
                    style={{ background: "rgba(0,0,0,0.03)", cursor: "not-allowed" }}
                  />
                </label>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                <label>
                  Contact Phone Number
                  <input
                    type="tel"
                    value={profile.phone}
                    onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                    placeholder="+91 98765 43210"
                  />
                </label>

                {user?.role === "mentor" ? (
                  <label>
                    WhatsApp Number for Automated Student Alerts *
                    <input
                      type="tel"
                      value={profile.whatsappNumber}
                      onChange={(e) => setProfile({ ...profile, whatsappNumber: e.target.value })}
                      placeholder="+91 98765 43210"
                    />
                  </label>
                ) : user?.role === "student" ? (
                  <label>
                    Student ID
                    <input
                      type="text"
                      disabled
                      value={user?.studentId || "PC-STU-100001"}
                      style={{ fontWeight: 700, color: "var(--pc-primary)", background: "rgba(0,0,0,0.03)", cursor: "not-allowed" }}
                    />
                  </label>
                ) : (
                  <label>
                    Role Assigned
                    <input
                      type="text"
                      disabled
                      value={roleLabel}
                      style={{ fontWeight: 700, background: "rgba(0,0,0,0.03)", cursor: "not-allowed" }}
                    />
                  </label>
                )}
              </div>

              {user?.role === "student" && (
                <>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                    <label>
                      Target Examination
                      <select
                        value={profile.targetExam}
                        onChange={(e) => setProfile({ ...profile, targetExam: e.target.value })}
                      >
                        <option value="GATE CSE">GATE CSE (Computer Science &amp; IT)</option>
                        <option value="JEE Advanced">JEE Advanced</option>
                        <option value="JEE Main">JEE Main</option>
                        <option value="NEET UG">NEET UG</option>
                        <option value="UPSC Civil Services">UPSC Civil Services (CSE)</option>
                        <option value="CAT">CAT (Common Admission Test)</option>
                        <option value="SSC CGL">SSC CGL</option>
                        <option value="IBPS PO">IBPS PO</option>
                        <option value="TNPSC Group I">TNPSC Group I</option>
                      </select>
                    </label>

                    <label>
                      Daily Study Target (Hours)
                      <input
                        type="number"
                        min="1"
                        max="18"
                        value={profile.dailyGoalHours}
                        onChange={(e) => setProfile({ ...profile, dailyGoalHours: e.target.value })}
                      />
                    </label>
                  </div>

                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                    <label>
                      College / Institution
                      <input
                        type="text"
                        value={profile.college}
                        onChange={(e) => setProfile({ ...profile, college: e.target.value })}
                        placeholder="e.g. Anna University / IIT Madras"
                      />
                    </label>

                    <label>
                      State / Location
                      <input
                        type="text"
                        value={profile.state}
                        onChange={(e) => setProfile({ ...profile, state: e.target.value })}
                        placeholder="e.g. Tamil Nadu, India"
                      />
                    </label>
                  </div>
                </>
              )}

              <label>
                {user?.role === "mentor" ? "Mentor Bio & Subject Specialization" : "Bio / Personal Study Motto"}
                <textarea
                  rows="2"
                  value={profile.bio}
                  onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
                  placeholder={user?.role === "mentor" ? "e.g. Senior Faculty in GATE CSE / Data Structures" : "e.g. Aiming for AIR under 100."}
                />
              </label>

              {profileMsg.text && (
                <div className={profileMsg.error ? "pc-form-error" : "pc-badge pc-badge-success"} style={{ padding: "8px 12px" }}>
                  {profileMsg.text}
                </div>
              )}

              <button type="submit" className="pc-btn pc-btn-primary" disabled={profileSaving} style={{ width: "fit-content", marginTop: 4 }}>
                {profileSaving ? "Saving Profile…" : "Save Profile Details"}
              </button>
            </form>
          </div>

          {/* CHANGE PASSWORD SECTION (ALL ROLES) */}
          <div className="pc-card">
            <h3>🔒 Change Password</h3>
            <p className="pc-card-note">Update your account credentials to keep your PrepCycle account secure.</p>

            <form onSubmit={handlePasswordSubmit} className="pc-form" style={{ marginTop: 14 }}>
              <label>
                Current Password
                <input
                  type="password"
                  required
                  value={passwords.currentPassword}
                  onChange={(e) => setPasswords({ ...passwords, currentPassword: e.target.value })}
                  placeholder="Enter current password"
                />
              </label>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                <label>
                  New Password
                  <input
                    type="password"
                    required
                    minLength={6}
                    value={passwords.newPassword}
                    onChange={(e) => setPasswords({ ...passwords, newPassword: e.target.value })}
                    placeholder="At least 6 characters"
                  />
                </label>

                <label>
                  Confirm New Password
                  <input
                    type="password"
                    required
                    minLength={6}
                    value={passwords.confirmPassword}
                    onChange={(e) => setPasswords({ ...passwords, confirmPassword: e.target.value })}
                    placeholder="Re-enter new password"
                  />
                </label>
              </div>

              {passMsg.text && (
                <div className={passMsg.error ? "pc-form-error" : "pc-badge pc-badge-success"} style={{ padding: "8px 12px" }}>
                  {passMsg.text}
                </div>
              )}

              <button type="submit" className="pc-btn pc-btn-outline" disabled={passSaving} style={{ width: "fit-content", marginTop: 4 }}>
                {passSaving ? "Updating Password…" : "Update Password"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
