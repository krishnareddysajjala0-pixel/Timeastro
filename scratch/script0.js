
        (function () {
            const savedTheme = localStorage.getItem('preferred-theme') || 'default';
            if (savedTheme !== 'default') {
                document.documentElement.setAttribute('data-theme', savedTheme);
            }
        })();
    