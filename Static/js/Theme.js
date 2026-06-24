// ========================================================================
// THEME SWITCHER - Dark/Light Mode Toggle
// ========================================================================

const themeToggle = document.getElementById('themeToggle');
const htmlElement = document.documentElement;

// Check for saved theme preference or default to light mode
const savedTheme = localStorage.getItem('theme') || 'light';
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

function setTheme(theme) {
    if (theme === 'dark') {
        htmlElement.querySelector('body').classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
        if (themeToggle) themeToggle.innerHTML = '<span>☀️</span>';
    } else {
        htmlElement.querySelector('body').classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
        if (themeToggle) themeToggle.innerHTML = '<span>🌙</span>';
    }
}

// Initialize theme on page load
if (savedTheme === 'dark' || (savedTheme === 'auto' && prefersDark)) {
    setTheme('dark');
} else {
    setTheme('light');
}

// Toggle theme on button click
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = localStorage.getItem('theme');
        setTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });
}

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    const newTheme = e.matches ? 'dark' : 'light';
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'auto') {
        setTheme(newTheme);
    }
});
