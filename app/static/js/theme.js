// Copia de design/assets/theme.js para uso en Django templates
(function(){
  const root = document.documentElement;
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
  const THEME_KEY = 'ui:theme';
  const SIDEBAR_KEY = 'ui:sidebar-collapsed';

  function applyTheme(theme){
    const isDark = theme === 'dark';
    root.classList.toggle('theme-dark', isDark);
  }
  function getInitialTheme(){
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === 'light' || saved === 'dark') return saved;
    return prefersDark.matches ? 'dark' : 'light';
  }
  function saveTheme(theme){ localStorage.setItem(THEME_KEY, theme); }
  function toggleTheme(){
    const next = root.classList.contains('theme-dark') ? 'light' : 'dark';
    applyTheme(next); saveTheme(next);
  }
  document.addEventListener('DOMContentLoaded', () => {
    applyTheme(getInitialTheme());
    prefersDark.addEventListener('change', (e) => {
      if (!localStorage.getItem(THEME_KEY)) applyTheme(e.matches ? 'dark' : 'light');
    });
    document.querySelectorAll('[data-action="theme-toggle"]').forEach(btn => btn.addEventListener('click', toggleTheme));
  });
})();
