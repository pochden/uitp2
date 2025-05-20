document.addEventListener('DOMContentLoaded', () => {
    // Улучшенные функции работы с Cookies
    const setThemeCookie = (theme) => {
        document.cookie = `theme=${theme};path=/;max-age=31536000;SameSite=Lax`;
    };

    const getThemeCookie = () => {
        return document.cookie
            .split('; ')
            .find(row => row.startsWith('theme='))
            ?.split('=')[1] || 'light';
    };

    // Создание кнопки темы
    const toggleButton = document.createElement('button');
    toggleButton.id = 'theme-toggle';
    Object.assign(toggleButton.style, {
        position: 'absolute',
        right: '20px',
        top: '20px',
        cursor: 'pointer',
        zIndex: '1000'
    });

    // Вставка кнопки в DOM
    document.querySelector('header')?.prepend(toggleButton);

    // Применение темы
    const applyTheme = () => {
        const theme = getThemeCookie();
        document.body.classList.toggle('dark-theme', theme === 'dark');
        toggleButton.textContent = theme === 'dark' ? '☀️ Светлая тема' : '🌙 Тёмная тема';
        toggleButton.setAttribute('aria-label', `Текущая тема: ${theme === 'dark' ? 'тёмная' : 'светлая'}`);
    };

    // Инициализация
    applyTheme();

    // Обработчик клика
    toggleButton.addEventListener('click', () => {
        const newTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
        setThemeCookie(newTheme);
        applyTheme();
    });
});