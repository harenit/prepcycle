import { NavLink, Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useLanguage } from "../context/LanguageContext";

const STUDENT_LINKS = [
  { to: "/exam-explorer", key: "exams", label: "Exams", icon: "🧭" },
  { to: "/my-progress", key: "myProgress", label: "My Progress", icon: "📈" },
  { to: "/marketplace", key: "marketplace", label: "Marketplace", icon: "📚" },
  { to: "/orders", key: "ordersTracking", label: "Orders & Tracking", icon: "🚚" },
  { to: "/resources", key: "resources", label: "Resources", icon: "🗂️" },
  { to: "/community", key: "community", label: "Community", icon: "💬" },
  { to: "/study-planner", key: "studyPlanner", label: "Study Planner", icon: "📅" },
  { to: "/settings", key: "settings", label: "Settings", icon: "⚙️" },
];

const ADMIN_LINKS = [
  { to: "/admin?tab=overview", tabValue: "overview", key: "dashboard", label: "Dashboard", icon: "📊" },
  { to: "/admin?tab=exams", tabValue: "exams", key: "manageExams", label: "Manage Exams", icon: "🧭" },
  { to: "/admin?tab=resources", tabValue: "resources", key: "manageResources", label: "Manage Resources", icon: "🗂️" },
  { to: "/admin?tab=products", tabValue: "products", key: "manageProducts", label: "Marketplace", icon: "📚" },
  { to: "/admin?tab=users", tabValue: "users", key: "users", label: "Users", icon: "👥" },
  { to: "/admin?tab=mentors", tabValue: "mentors", key: "mentors", label: "Mentors & Assignment", icon: "👨‍🏫" },
  { to: "/admin?tab=orders", tabValue: "orders", key: "orders", label: "Orders", icon: "🚚" },
  { to: "/admin?tab=returns", tabValue: "returns", key: "returns", label: "Returns / Resale", icon: "♻️" },
  { to: "/admin?tab=communications", tabValue: "communications", key: "communications", label: "Communication Logs", icon: "📨" },
  { to: "/settings", key: "settings", label: "Settings & Appearance", icon: "⚙️" },
];

const MENTOR_LINKS = [
  { to: "/mentor", key: "mentorDashboard", label: "Assigned Students & Alerts", icon: "👨‍🏫" },
  { to: "/settings", key: "settings", label: "Settings & Appearance", icon: "⚙️" },
];

export default function Sidebar() {
  const { user, logout } = useAuth();
  const { lang, setLang, t, supportedLanguages } = useLanguage();
  const location = useLocation();

  const isAdmin = user?.role === "admin";
  const isDelivery = user?.role === "delivery";
  const isMentor = user?.role === "mentor";
  const activeAdminTab = new URLSearchParams(location.search).get("tab") || "overview";

  // Dedicated layout for Delivery Partner
  if (isDelivery) {
    return (
      <aside className="pc-sidebar">
        <div className="pc-sidebar-brand">
          <span className="pc-logo-dot" />
          PrepCycle
        </div>
        <nav className="pc-sidebar-nav">
          <NavLink to="/delivery" className="pc-sidebar-link">
            <span className="pc-sidebar-icon">🚚</span>
            {t("deliveryDashboard", "Delivery Console")}
          </NavLink>
          <NavLink to="/settings" className="pc-sidebar-link">
            <span className="pc-sidebar-icon">⚙️</span>
            {t("settings", "Settings & Appearance")}
          </NavLink>
        </nav>
        <div className="pc-sidebar-language">
          <label htmlFor="pc-language">{t("language", "Language")}</label>
          <select id="pc-language" value={lang} onChange={(e) => setLang(e.target.value)}>
            {supportedLanguages.map((l) => (
              <option key={l.code} value={l.code}>
                {l.label}
              </option>
            ))}
          </select>
        </div>
        <div className="pc-sidebar-footer">
          <div className="pc-sidebar-user">
            <div
              className="pc-avatar"
              style={{ background: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)", color: "#fff" }}
            >
              {user?.name?.[0]?.toUpperCase() || "D"}
            </div>
            <div>
              <div className="pc-sidebar-user-name">{user?.name}</div>
              <div className="pc-sidebar-user-role" style={{ color: "#fbbf24", fontWeight: 700 }}>
                🚚 Delivery Partner
              </div>
            </div>
          </div>
          <button className="pc-btn pc-btn-ghost pc-btn-small" onClick={logout}>
            {t("logOut", "Log out")}
          </button>
        </div>
      </aside>
    );
  }

  // Dedicated layout for Academic Mentor
  if (isMentor) {
    return (
      <aside className="pc-sidebar">
        <div className="pc-sidebar-brand">
          <span className="pc-logo-dot" />
          PrepCycle
        </div>
        <nav className="pc-sidebar-nav">
          {MENTOR_LINKS.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => `pc-sidebar-link${isActive ? " active" : ""}`}
            >
              <span className="pc-sidebar-icon">{link.icon}</span>
              {t(link.key, link.label)}
            </NavLink>
          ))}
        </nav>
        <div className="pc-sidebar-language">
          <label htmlFor="pc-language">{t("language", "Language")}</label>
          <select id="pc-language" value={lang} onChange={(e) => setLang(e.target.value)}>
            {supportedLanguages.map((l) => (
              <option key={l.code} value={l.code}>
                {l.label}
              </option>
            ))}
          </select>
        </div>
        <div className="pc-sidebar-footer">
          <div className="pc-sidebar-user">
            <div
              className="pc-avatar"
              style={{ background: "linear-gradient(135deg, #10b981 0%, #059669 100%)", color: "#fff" }}
            >
              {user?.name?.[0]?.toUpperCase() || "M"}
            </div>
            <div>
              <div className="pc-sidebar-user-name">{user?.name}</div>
              <div className="pc-sidebar-user-role" style={{ color: "#34d399", fontWeight: 700 }}>
                👨‍🏫 Academic Mentor
              </div>
            </div>
          </div>
          <button className="pc-btn pc-btn-ghost pc-btn-small" onClick={logout}>
            {t("logOut", "Log out")}
          </button>
        </div>
      </aside>
    );
  }

  return (
    <aside className="pc-sidebar">
      <div className="pc-sidebar-brand">
        <span className="pc-logo-dot" />
        PrepCycle
      </div>

      <nav className="pc-sidebar-nav">
        {isAdmin
          ? ADMIN_LINKS.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                data-tour={`nav-${link.key}`}
                className={`pc-sidebar-link${activeAdminTab === link.tabValue ? " active" : ""}`}
              >
                <span className="pc-sidebar-icon">{link.icon}</span>
                {t(link.key, link.label)}
              </Link>
            ))
          : STUDENT_LINKS.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                data-tour={`nav-${link.key}`}
                className={({ isActive }) => `pc-sidebar-link${isActive ? " active" : ""}`}
              >
                <span className="pc-sidebar-icon">{link.icon}</span>
                {t(link.key, link.label)}
              </NavLink>
            ))}
      </nav>

      <div className="pc-sidebar-language">
        <label htmlFor="pc-language">{t("language", "Language")}</label>
        <select id="pc-language" value={lang} onChange={(e) => setLang(e.target.value)}>
          {supportedLanguages.map((l) => (
            <option key={l.code} value={l.code}>
              {l.label}
            </option>
          ))}
        </select>
      </div>

      <div className="pc-sidebar-footer">
        <div className="pc-sidebar-user">
          <div
            className="pc-avatar"
            style={{
              background: isAdmin
                ? "linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)"
                : "linear-gradient(135deg, #4f46e5 0%, #3730a3 100%)",
              color: "#fff",
            }}
          >
            {user?.name?.[0]?.toUpperCase() || "?"}
          </div>
          <div>
            <div className="pc-sidebar-user-name">{user?.name}</div>
            <div
              className="pc-sidebar-user-role"
              style={{
                color: isAdmin ? "#c084fc" : "#818cf8",
                fontWeight: 700,
              }}
            >
              {isAdmin ? "⚡ Platform Admin" : (user?.studentId ? `🎓 Student (${user.studentId})` : "🎓 Student")}
            </div>
          </div>
        </div>
        <button className="pc-btn pc-btn-ghost pc-btn-small" onClick={logout}>
          {t("logOut", "Log out")}
        </button>
      </div>
    </aside>
  );
}
