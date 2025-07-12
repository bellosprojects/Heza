document.addEventListener('DOMContentLoaded', function() {
    const codeDivs = document.querySelectorAll('div.code');
    const keywords = ['data', 'out', 'in', 'trace', 'block', 'loop','as', 'insert', 'default','end'];
    
    // Orden de importancia: strings primero, luego otros patrones
    const syntaxRules = [
        {
            name: 'string',
            regex: /"(?:\\.|[^"\\])*"/g,
        },
        {
            name: 'operator',
            // Operadores mejorados para capturar aquellos después de números
            regex: /(->|\?|[:+\-*/%=!<>^&|~]+)/g,
            color: 'red'
        },
        {
            name: 'number',
            // Números con posibles operadores inmediatamente después
            regex: /\b\d+(?:\.\d+)?(?![\w])/g,
            color: 'green'
        },
        {
            name: 'keyword',
            regex: new RegExp(`\\b(${keywords.join('|')})\\b`, 'g'),
        }
    ];

    function highlightSyntax(text) {
        // Array para guardar las partes del texto
        const fragments = [{ text, type: null }];
        
        syntaxRules.forEach(rule => {
            fragments.forEach((fragment, index) => {
                if (fragment.type !== null) return;
                
                const parts = [];
                let lastIndex = 0;
                let match;
                
                const regex = new RegExp(rule.regex.source, rule.regex.flags + (rule.regex.global ? '' : 'g'));
                
                while ((match = regex.exec(fragment.text)) !== null) {
                    // Texto antes del match
                    if (match.index > lastIndex) {
                        parts.push({
                            text: fragment.text.substring(lastIndex, match.index),
                            type: null
                        });
                    }
                    
                    // El match
                    parts.push({
                        text: match[0],
                        type: rule.name
                    });
                    
                    lastIndex = match.index + match[0].length;
                    
                    // Si la regex no es global, salir después del primer match
                    if (!rule.regex.global) break;
                }
                
                // Texto restante
                if (lastIndex < fragment.text.length) {
                    parts.push({
                        text: fragment.text.substring(lastIndex),
                        type: null
                    });
                }
                
                // Reemplazar el fragmento actual con las partes divididas
                if (parts.length > 1) {
                    fragments.splice(index, 1, ...parts);
                }
            });
        });
        
        // Construir el HTML con los spans
        let html = '';
        fragments.forEach(fragment => {
            if (fragment.type) {
                const rule = syntaxRules.find(r => r.name === fragment.type);
                html += `<span class="${rule.name}">${fragment.text}</span>`;
            } else {
                html += fragment.text;
            }
        });
        
        return html;
    }

    codeDivs.forEach(div => {
        // Guardar el texto original para evitar problemas con entidades HTML
        const originalText = div.textContent;
        div.innerHTML = highlightSyntax(originalText);
    });
});