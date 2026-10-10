/* =====================================================
   Portal Mulher MT — script.js (versão corrigida v9)
   ===================================================== */

/* --- 1. CARROSSEL DE CARDS ----------------------------- */
document.addEventListener('DOMContentLoaded', () => {
    const track = document.querySelector('.carousel-track');
    const nextBtn = document.querySelector('.carousel-next');
    const prevBtn = document.querySelector('.carousel-prev');

    if (track && nextBtn && prevBtn) {
        const cards = Array.from(track.children);
        if (cards.length > 0) {
            let currentIndex = 1;

            const updateCarousel = () => {
                const trackWidth = track.parentElement.getBoundingClientRect().width;
                const cardWidth = cards[0].getBoundingClientRect().width;
                const gap = parseInt(window.getComputedStyle(track).gap) || 0;

                cards.forEach(card => card.classList.remove('active'));
                if (cards[currentIndex]) cards[currentIndex].classList.add('active');

                const amountToMove = (currentIndex * (cardWidth + gap)) - (trackWidth / 2) + (cardWidth / 2);
                track.style.transform = `translateX(${-amountToMove}px)`;
            };

            let autoPlayInterval = setInterval(() => {
                currentIndex = currentIndex < cards.length - 1 ? currentIndex + 1 : 0;
                updateCarousel();
            }, 5000);

            const resetAutoPlay = () => {
                clearInterval(autoPlayInterval);
                autoPlayInterval = setInterval(() => {
                    currentIndex = currentIndex < cards.length - 1 ? currentIndex + 1 : 0;
                    updateCarousel();
                }, 5000);
            };

            nextBtn.addEventListener('click', () => {
                currentIndex = currentIndex < cards.length - 1 ? currentIndex + 1 : 0;
                updateCarousel();
                resetAutoPlay();
            });

            prevBtn.addEventListener('click', () => {
                currentIndex = currentIndex > 0 ? currentIndex - 1 : cards.length - 1;
                updateCarousel();
                resetAutoPlay();
            });

            updateCarousel();
            window.addEventListener('resize', updateCarousel);
        }
    }
});


/* --- 2. DEMAIS FUNCIONALIDADES ------------------------- */
document.addEventListener('DOMContentLoaded', () => {

    /* 2a. Banner rotativo */
    const heroBgs = document.querySelectorAll('.hero-bg');
    if (heroBgs.length > 1) {
        let currentBg = 0;
        setInterval(() => {
            heroBgs[currentBg].classList.remove('active');
            currentBg = (currentBg + 1) % heroBgs.length;
            heroBgs[currentBg].classList.add('active');
        }, 6000);
    }

    /* 2b. Parallax na fita de fundo */
    const ribbon = document.querySelector('.background-ribbon');
    if (ribbon) {
        window.addEventListener('scroll', () => {
            ribbon.style.transform = `rotate(20deg) translateY(${window.scrollY * 0.15}px)`;
        });
    }

    /* 2b. Scroll-reveal nos cards de serviço */
    const serviceCards = document.querySelectorAll('.service-card');
    if (serviceCards.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        serviceCards.forEach((card, i) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = `all 0.5s cubic-bezier(0.16, 1, 0.3, 1) ${i * 0.1}s`;
            observer.observe(card);
        });
    }

    /* 2c. Barra de pesquisa hero */
    const searchForm = document.querySelector('.hero-search-bar');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input');
        const searchBtn = searchForm.querySelector('button');
        if (searchBtn && searchInput) {
            searchBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (searchInput.value.trim() !== '') {
                    console.log('Buscando por:', searchInput.value);
                    searchInput.value = '';
                    searchInput.placeholder = 'Buscando...';
                    setTimeout(() => {
                        searchInput.placeholder = 'Quais serviços você gostaria de explorar hoje?';
                    }, 1500);
                }
            });
        }
    }

    /* 2d. Chat / Assistente Virtual Ixpia */
    const assistantBtn = document.getElementById('assistantBtn');
    const chatWindow = document.getElementById('chatWindow');
    const closeChat = document.getElementById('closeChat');
    const maximizeChat = document.getElementById('maximizeChat');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const chatTyping = document.getElementById('chatTyping');

    function addMessage(text, side) {
        if (!chatMessages) return;
        const now = new Date();
        const timeString = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        let formattedText = text;
        // Parse markdown simplificado (negrito e quebras de linha)
        formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formattedText = formattedText.replace(/\n/g, '<br>');

        const wrapperDiv = document.createElement('div');
        wrapperDiv.classList.add('message-wrapper');
        wrapperDiv.style.cssText = side === 'bot' ? 'display: flex; gap: 10px; align-items: flex-end; margin-bottom: 10px;' : 'display: flex; justify-content: flex-end; margin-bottom: 10px;';
        
        const msgHTML = side === 'bot' 
            ? `<img src="/static/assets/assistant.png" alt="ExpiA" class="chat-msg-avatar" style="width:30px; height:30px; border-radius:50%; border:2px solid #e2d6ff;">
               <div class="message bot" style="max-width: 100%;">
                   ${formattedText}
                   <span class="msg-time" style="font-size:0.6rem; color:#999; display:block; text-align:right; margin-top:5px;">${timeString}</span>
               </div>`
            : `<div class="message user" style="background-color: #8c71d6; color: white; border-bottom-right-radius: 2px;">
                   ${formattedText}
                   <span class="msg-time" style="font-size:0.6rem; color:#e2d6ff; display:block; text-align:right; margin-top:5px;">${timeString}</span>
               </div>`;
               
        wrapperDiv.innerHTML = msgHTML;
        chatMessages.appendChild(wrapperDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    if (assistantBtn && chatWindow) {
        assistantBtn.addEventListener('click', () => {
            chatWindow.classList.toggle('active');
            if (chatWindow.classList.contains('active') && chatInput) {
                chatInput.focus();
            }
        });

        if (closeChat) {
            closeChat.addEventListener('click', () => {
                chatWindow.classList.remove('active');
                chatWindow.classList.remove('maximized');
                if (maximizeChat) maximizeChat.innerHTML = '<i class="fa-solid fa-expand"></i>';
            });
        }

        if (maximizeChat) {
            maximizeChat.addEventListener('click', () => {
                chatWindow.classList.toggle('maximized');
                if (chatWindow.classList.contains('maximized')) {
                    maximizeChat.innerHTML = '<i class="fa-solid fa-compress"></i>';
                } else {
                    maximizeChat.innerHTML = '<i class="fa-solid fa-expand"></i>';
                }
            });
        }

        if (chatForm) {
            const chatCharCounter = document.getElementById('chatCharCounter');
            
            if (chatInput && chatCharCounter) {
                chatInput.addEventListener('input', () => {
                    const remaining = 200 - chatInput.value.length;
                    chatCharCounter.textContent = `${remaining} letras restantes`;
                });
            }

            // Atualiza tempo inicial
            const initTime = document.getElementById('initTime');
            if (initTime) {
                initTime.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            }

            chatForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const message = chatInput ? chatInput.value.trim() : '';
                if (!message) return;

                const optionsContainer = document.getElementById('chatOptionsContainer');
                if (optionsContainer) optionsContainer.style.display = 'none';

                addMessage(message, 'user');
                if (chatInput) {
                    chatInput.value = '';
                    if (chatCharCounter) chatCharCounter.textContent = '200 letras restantes';
                }
                if (chatTyping) { chatTyping.style.display = 'flex'; }
                if (chatMessages) chatMessages.scrollTop = chatMessages.scrollHeight;

                try {
                    const response = await fetch('/chat?message=' + encodeURIComponent(message), {
                        method: 'GET',
                        headers: { 'Accept': 'application/json' }
                    });
                    const data = await response.json();
                    if (chatTyping) chatTyping.style.display = 'none';
                    addMessage(data.response, 'bot');
                } catch (error) {
                    console.error('Erro no chat:', error);
                    if (chatTyping) chatTyping.style.display = 'none';
                    addMessage('Desculpe, tive um problema de conexão. Tente novamente mais tarde.', 'bot');
                }
            });
        }
    }

    // Função global para enviar tópicos rápidos
    window.sendTopic = function(topicText) {
        const optionsContainer = document.getElementById('chatOptionsContainer');
        if (optionsContainer) optionsContainer.style.display = 'none';
        
        addMessage(topicText, 'user');
        if (chatTyping) { chatTyping.style.display = 'flex'; }
        if (chatMessages) chatMessages.scrollTop = chatMessages.scrollHeight;

        fetch('/chat?message=' + encodeURIComponent(topicText), {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            if (chatTyping) chatTyping.style.display = 'none';
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Erro no chat:', error);
            if (chatTyping) chatTyping.style.display = 'none';
            addMessage('Desculpe, tive um problema de conexão. Tente novamente mais tarde.', 'bot');
        });
    };

    /* 2e. Voltar ao topo */
    const backToTopBtn = document.getElementById('backToTopBtn');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    /* Lógica A+ / A- do Chat */
    const chatFontIncrease = document.getElementById('chatFontIncrease');
    const chatFontDecrease = document.getElementById('chatFontDecrease');
    let chatBaseSize = 100;
    
    if (chatFontIncrease && chatMessages) {
        chatFontIncrease.addEventListener('click', () => {
            if (chatBaseSize < 140) {
                chatBaseSize += 10;
                chatMessages.style.fontSize = `${chatBaseSize}%`;
            }
        });
    }
    if (chatFontDecrease && chatMessages) {
        chatFontDecrease.addEventListener('click', () => {
            if (chatBaseSize > 80) {
                chatBaseSize -= 10;
                chatMessages.style.fontSize = `${chatBaseSize}%`;
            }
        });
    }

    /* 2f. Alto Contraste */
    const darkToggle = document.getElementById('accessDarkToggle');
    if (darkToggle) {
        if (localStorage.getItem('contrastActive') === 'true') {
            document.body.classList.add('dark-contrast');
            darkToggle.setAttribute('aria-pressed', 'true');
        }
        darkToggle.addEventListener('click', (e) => {
            e.preventDefault();
            const active = document.body.classList.toggle('dark-contrast');
            localStorage.setItem('contrastActive', active);
            darkToggle.setAttribute('aria-pressed', active ? 'true' : 'false');
        });
    }

    /* 2g. Tamanho de fonte (ciclo: 100% → 120% → 140% → 100%) */
    const fontToggle = document.getElementById('accessFontToggle');
    let currentFontSizeFactor = parseInt(localStorage.getItem('fontSizeFactor')) || 100;
    if (currentFontSizeFactor !== 100) {
        document.body.style.fontSize = `${currentFontSizeFactor}%`;
    }
    if (fontToggle) {
        fontToggle.addEventListener('click', (e) => {
            e.preventDefault();
            if (currentFontSizeFactor === 100) currentFontSizeFactor = 120;
            else if (currentFontSizeFactor === 120) currentFontSizeFactor = 140;
            else currentFontSizeFactor = 100;
            document.body.style.fontSize = `${currentFontSizeFactor}%`;
            localStorage.setItem('fontSizeFactor', currentFontSizeFactor);
        });
    }

    /* 2h. Botão Libras — abre o widget VLibras ao clicar */
    const fabLibras = document.querySelector('.fab-libras');
    if (fabLibras) {

        fabLibras.addEventListener('click', () => {
            /* dispatchEvent funciona mesmo com pointer-events:none no elemento alvo */
            const dispararVLibras = (tentativa) => {
                const btn = document.querySelector('[vw-access-button]') ||
                    document.querySelector('.vw-access-button');
                if (btn) {
                    /* Remove pointer-events:none momentaneamente para garantir o clique */
                    btn.style.setProperty('pointer-events', 'auto', 'important');
                    btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
                    btn.style.setProperty('pointer-events', 'none', 'important');
                } else if (tentativa < 15) {
                    /* VLibras ainda carregando — tenta de novo */
                    setTimeout(() => dispararVLibras(tentativa + 1), 300);
                }
            };
            dispararVLibras(0);
        });

        fabLibras.addEventListener('mouseenter', () => { fabLibras.style.transform = 'scale(1.12)'; });
        fabLibras.addEventListener('mouseleave', () => { fabLibras.style.transform = 'scale(1)'; });
    }

    /* 2i. Topbar scroll color change */
    const topbar = document.querySelector('.topbar');
    if (topbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 150) {
                topbar.classList.add('topbar-scrolled');
            } else {
                topbar.classList.remove('topbar-scrolled');
            }
        });
    }
});
