
      function setTheme(theme) {
          if (theme === 'default') {
              document.documentElement.removeAttribute('data-theme');
          } else {
              document.documentElement.setAttribute('data-theme', theme);
          }
          localStorage.setItem('preferred-theme', theme);

          // Update UI buttons
          document.querySelectorAll('.theme-btn').forEach(btn => {
              btn.classList.remove('active');
              if (btn.getAttribute('data-theme-btn') === theme) {
                  btn.classList.add('active');
              }
          });
      }

        // Load saved theme immediately to prevent flashing
        const savedTheme = localStorage.getItem('preferred-theme') || 'light';
        setTheme(savedTheme);
    