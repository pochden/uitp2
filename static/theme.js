document.addEventListener('DOMContentLoaded', () => {
    // Theme toggle
    const setThemeCookie = (theme) => {
        document.cookie = `theme=${theme};path=/;max-age=31536000;SameSite=Lax`;
    };

    const getThemeCookie = () => {
        return document.cookie
            .split('; ')
            .find(row => row.startsWith('theme='))
            ?.split('=')[1] || 'light';
    };

    const toggleButton = document.createElement('button');
    toggleButton.id = 'theme-toggle';
    Object.assign(toggleButton.style, {
        position: 'absolute',
        right: '20px',
        top: '20px',
        cursor: 'pointer',
        zIndex: '1000'
    });

    document.querySelector('header')?.prepend(toggleButton);

    const applyTheme = () => {
        const theme = getThemeCookie();
        document.body.classList.toggle('dark-theme', theme === 'dark');
        toggleButton.textContent = theme === 'dark' ? '☀️ Светлая тема' : '🌙 Тёмная тема';
        toggleButton.setAttribute('aria-label', `Текущая тема: ${theme === 'dark' ? 'тёмная' : 'светлая'}`);
    };

    applyTheme();

    toggleButton.addEventListener('click', () => {
        const newTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
        setThemeCookie(newTheme);
        applyTheme();
    });

    // Menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const navUl = document.querySelector('nav ul');

    if (menuToggle && navUl) {
        menuToggle.addEventListener('click', () => {
            navUl.classList.toggle('show');
            menuToggle.textContent = navUl.classList.contains('show') ? '✖' : '☰';
            menuToggle.setAttribute('aria-label', navUl.classList.contains('show') ? 'Закрыть меню' : 'Открыть меню');
        });
    } else {
        console.error('Menu toggle or nav ul not found');
    }
});