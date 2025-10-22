// Premium UI behavior: theme + sidebar
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

  function applySidebar(collapsed){
    document.body.closest('.app')?.setAttribute('data-sidebar-collapsed', collapsed ? 'true' : 'false');
  }

  function saveSidebar(collapsed){ localStorage.setItem(SIDEBAR_KEY, collapsed ? '1' : '0'); }

  function getInitialSidebar(){ return localStorage.getItem(SIDEBAR_KEY) === '1'; }

  document.addEventListener('DOMContentLoaded', () => {
    // Theme init
    applyTheme(getInitialTheme());
    prefersDark.addEventListener('change', (e) => {
      if (!localStorage.getItem(THEME_KEY)) applyTheme(e.matches ? 'dark' : 'light');
    });

    // Theme toggle
    document.querySelectorAll('[data-action="theme-toggle"]').forEach(btn => {
      btn.addEventListener('click', toggleTheme);
    });

    // Sidebar init
    applySidebar(getInitialSidebar());

    // Sidebar toggle
    document.querySelectorAll('[data-action="sidebar-toggle"]').forEach(btn => {
      btn.addEventListener('click', () => {
        const app = document.querySelector('.app');
        const collapsed = app?.getAttribute('data-sidebar-collapsed') === 'true';
        applySidebar(!collapsed); saveSidebar(!collapsed);
      });
    });
  });
})();
