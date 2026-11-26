const themeToggle = document.querySelector("[data-theme-toggle]");

if (themeToggle) {
  const themeLabel = themeToggle.querySelector("[data-theme-label]");
  const themeColor = document.querySelector('meta[name="theme-color"]');

  const updateThemeControls = (theme) => {
    const isDark = theme === "dark";
    themeToggle.setAttribute("aria-pressed", String(isDark));
    themeToggle.setAttribute("aria-label", `Switch to ${isDark ? "light" : "dark"} mode`);
    themeLabel.textContent = isDark ? "Light mode" : "Dark mode";
    if (themeColor) {
      themeColor.content = isDark ? "#11131a" : "#f5f6fa";
    }
  };

  updateThemeControls(document.documentElement.dataset.theme);

  themeToggle.addEventListener("click", () => {
    const theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("taskboard-theme", theme);
    updateThemeControls(theme);
  });
}
