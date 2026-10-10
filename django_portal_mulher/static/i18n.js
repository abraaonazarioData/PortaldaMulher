document.addEventListener("DOMContentLoaded", () => {
    const customLangSelector = document.getElementById("customLangSelector");
    const langBtn = document.getElementById("langBtn");
    const currentLangText = document.getElementById("currentLangText");
    const langDropdownItems = document.querySelectorAll("#langDropdown li");
    
    // Identificar idioma atual lendo o cookie do Google Translate
    const getCookie = (name) => {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        if (match) return match[2];
        return null;
    };

    let currentLang = 'pt';
    const googtrans = getCookie('googtrans');
    
    if (googtrans) {
        const parts = decodeURIComponent(googtrans).split('/');
        if (parts.length === 3) {
            currentLang = parts[2];
        }
    }
    
    // Atualiza a UI inicial
    if (currentLangText) {
        currentLangText.textContent = currentLang.toUpperCase();
        
        // Esconde a linguagem atual das opções
        langDropdownItems.forEach(item => {
            if (item.getAttribute("data-lang") === currentLang) {
                item.style.display = 'none';
            } else {
                item.style.display = 'block';
            }
            
            // Verifica se a opção "PT" precisa ser exibida
            // Se o atual não for PT, adicionamos/mostramos PT dinamicamente ou podemos apenas alternar a visibilidade.
            // Para ser robusto, reconstruiremos o dropdown com base na linguagem atual.
        });
        
        // Reconstrói as opções de dropdown excluindo a atual
        const dropdownList = document.getElementById("langDropdown");
        if (dropdownList) {
            dropdownList.innerHTML = '';
            ['pt', 'en', 'es'].forEach(lang => {
                if (lang !== currentLang) {
                    const li = document.createElement("li");
                    li.setAttribute("data-lang", lang);
                    li.textContent = lang.toUpperCase();
                    dropdownList.appendChild(li);
                }
            });
            
            // Re-anexa eventos aos novos li
            document.querySelectorAll("#langDropdown li").forEach(item => {
                item.addEventListener("click", () => handleLangSelect(item.getAttribute("data-lang")));
            });
        }
    }
    
    // Toggle dropdown
    if (langBtn && customLangSelector) {
        langBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            customLangSelector.classList.toggle("active");
        });
        
        // Fecha ao clicar fora
        document.addEventListener("click", (e) => {
            if (!customLangSelector.contains(e.target)) {
                customLangSelector.classList.remove("active");
            }
        });
    }
    
    // Lógica ao selecionar um idioma
    function handleLangSelect(selectedLang) {
        if (selectedLang === 'pt') {
            document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=." + document.domain + "; path=/;";
            document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=" + document.domain + "; path=/;";
        } else {
            document.cookie = `googtrans=/pt/${selectedLang}; path=/;`;
            document.cookie = `googtrans=/pt/${selectedLang}; domain=.${document.domain}; path=/;`;
            document.cookie = `googtrans=/pt/${selectedLang}; domain=${document.domain}; path=/;`;
        }
        
        // Recarrega a página para o Google Translate agir
        window.location.reload();
    }
});
