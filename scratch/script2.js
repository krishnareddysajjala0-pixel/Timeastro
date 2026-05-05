
        // Theme Management
        function setTheme(themeName) {
            if (themeName === 'default') {
                document.documentElement.removeAttribute('data-theme');
            } else {
                document.documentElement.setAttribute('data-theme', themeName);
            }
            localStorage.setItem('preferred-theme', themeName);

            // Update UI buttons
            document.querySelectorAll('.theme-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.getAttribute('data-theme-btn') === themeName) {
                    btn.classList.add('active');
                }
            });
        }

        // Load saved theme state into buttons immediately
        const savedThemeGlobal = localStorage.getItem('preferred-theme') || 'default';
        document.querySelectorAll('.theme-btn').forEach(btn => {
            if (btn.getAttribute('data-theme-btn') === savedThemeGlobal) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Smooth scroll function
        function scrollToSection(sectionId) {
            const section = document.getElementById(sectionId);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
        }

        // Navigation functions
      window.onbeforeprint = function() {
        // Standard print adjustments
      };
      window.onafterprint = function() {
        // Standard cleanup
      };

      function goToBirthChart() {
            showLoader();
            window.location.href = '/go-to-birth-chart';
        }

        function goToDashaChart() {
            showLoader();
            window.location.href = '/go-to-dasha-chart';
        }

        // Add hover effects to table rows
        document.addEventListener('DOMContentLoaded', function () {
            const tableRows = document.querySelectorAll('.data-table tbody tr');

            tableRows.forEach(row => {
                row.addEventListener('mouseenter', function () {
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.2)';
                });

                row.addEventListener('mouseleave', function () {
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = 'none';
                });
            });

            // Highlight current year in footer
            const currentYear = new Date().getFullYear();
            const footerText = document.querySelector('.footer p');
            if (footerText) {
                footerText.innerHTML = `© ${currentYear} తెలుగు జ్యోతిష్య విశ్లేషణ - ద్వాదశ గ్రహముల ఫలితాలు`;
            }

            // Add floating button tooltips
            const floatBtns = document.querySelectorAll('.float-btn');
            floatBtns.forEach(btn => {
                btn.addEventListener('mouseenter', function () {
                    this.style.transform = 'translateY(-5px)';
                });
                btn.addEventListener('mouseleave', function () {
                    this.style.transform = 'translateY(0)';
                });
            });
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', function (e) {
            // Home key to go to top
            if (e.key === 'Home') {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }

            // End key to go to bottom
            if (e.key === 'End') {
                window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            }

            // Ctrl+P for print
            if (e.ctrlKey && e.key === 'p') {
                e.preventDefault();
                window.print();
            }

            // Escape to go home
            if (e.key === 'Escape') {
                window.location.href = '/';
            }

            // Ctrl+1 for birth chart
            if (e.ctrlKey && e.key === '1') {
                e.preventDefault();
                goToBirthChart();
            }

            // Ctrl+2 for dasha chart
            if (e.ctrlKey && e.key === '2') {
                e.preventDefault();
                goToDashaChart();
            }
        });

        // Add loading animation to page
        window.addEventListener('load', function () {
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.5s ease';

            setTimeout(() => {
                document.body.style.opacity = '1';
            }, 100);
        });

        function startTyping() {
            const element = document.getElementById("typing-text");
            if (!element) return;
            
            element.innerHTML = '<div class="rainbow-scroller">6-3=6</div>';
        }

        /* Rainbow Scroller Styles */
        const style = document.createElement('style');
        style.textContent = `
            .rainbow-scroller {
                font-size: 42px;
                font-weight: 900;
                white-space: nowrap;
                display: inline-block;
                animation: rainbow-scroll-left-right 4s linear infinite;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
                position: absolute;
                left: 0;
            }
            @keyframes rainbow-scroll-left-right {
                0% { color: #ff0000; left: -100px; }
                15% { color: #ff7f00; }
                30% { color: #ffff00; }
                45% { color: #00ff00; }
                60% { color: #0000ff; }
                75% { color: #4b0082; }
                90% { color: #8b00ff; }
                100% { color: #ff0000; left: 100%; }
            }
            #loading-overlay {
                overflow: hidden;
                position: relative;
            }
        `;
        document.head.appendChild(style);

        function playLoadingSound() {
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                let time = audioCtx.currentTime;
                for(let i = 0; i < 6; i++) {
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.type = i % 2 === 0 ? 'sine' : 'triangle';
                    osc.frequency.setValueAtTime(440 + (i * 80), time);
                    gain.gain.setValueAtTime(0, time);
                    gain.gain.linearRampToValueAtTime(0.04, time + 0.05);
                    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.3);
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start(time);
                    osc.stop(time + 0.4);
                    time += 0.25;
                }
            } catch (e) {}
        }

        function showLoader() {
            playLoadingSound();
            const overlay = document.getElementById('loading-overlay');
            if (overlay) overlay.style.display = 'flex';
            startTyping();
        }

        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', function(e) {
                if(this.href && !this.href.includes('#')) {
                    showLoader();
                }
            });
        });
    