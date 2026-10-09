import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { AuthProvider } from "./context/AuthContext";
import { LanguageProvider } from "./context/LanguageContext";
import "./styles.css";

// Restore stored appearance settings across the entire application immediately
try {
  document.documentElement.dataset.theme = localStorage.getItem("prepcycle_theme") || "light";
  document.documentElement.dataset.color = localStorage.getItem("prepcycle_color") || "default";
  document.documentElement.dataset.font = localStorage.getItem("prepcycle_font") || "medium";
  const custom = JSON.parse(localStorage.getItem("prepcycle_custom_palette") || "null");
  if (custom) {
    if (custom.buttonColor) {
      document.documentElement.style.setProperty("--pc-primary", custom.buttonColor);
      document.documentElement.style.setProperty("--pc-primary-dark", custom.buttonColor);
    }
    if (custom.textColor) document.documentElement.style.setProperty("--pc-text", custom.textColor);
    if (custom.bgColor) document.documentElement.style.setProperty("--pc-bg", custom.bgColor);
    if (custom.surfaceColor) document.documentElement.style.setProperty("--pc-surface", custom.surfaceColor);
  }
} catch {
  // Graceful fallback
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <LanguageProvider>
          <App />
        </LanguageProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
