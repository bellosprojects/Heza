/**
 * Procesa un texto y resalta elementos (palabras clave, números, etc.) 
 * con elementos <span> que tienen una clase CSS específica.
 *
 * @param {string} texto - El código o texto a resaltar.
 * @returns {string} El texto con los elementos <span> insertados.
 */
function resaltarCodigo(texto) {
    // 1. Definición de la expresión regular maestra
    // El orden de las partes es CRÍTICO, las más específicas primero.
    const regex = new RegExp(
        // 1. Cadenas de texto (entre comillas dobles o simples)
        // Coincide con cualquier carácter excepto la comilla de cierre.
        '(".*?")|' +         // Cadenas con comillas dobles
        "('.*?')|" +         // Cadenas con comillas simples
        // 2. Comentarios (@comentario)
        '(@.*?(?=\\n|$))|' +
        // 3. Palabras clave específicas (data, trace, ...)
        '\\b(data|trace|end|play|stop)\\b|' +
        // 4. Números (enteros y flotantes)
        '\\b(\\d+(?:\\.\\d+)?)\\b|' +
        // 5. Signos y operadores (+/*&^%$:<>?=) - Escapar caracteres especiales
        '([\\+=/*-\\?<>&%\\$\\^|≔←→∈↩∧∨¬√∅∀∃⊂≠∑∏∞∄∂∫∪!∩Δ])|' +
        // 5. Funciones (nombre pre-establecidos)
        '\\b(true|false|Sin|Cos|OUTPUT|INPUT|LINE|TAB|Bool|Text|Number|Expresion|Inf|Nah|Null|Set|Reference|lim|eval)\\b|' + 
        // 6. Espacios en blanco (para preservar formato)
        '(\\s+)|' +
        // 6. Otras palabras (Identificadores) - Coincide con el resto de "palabras"
        '(\\b[a-zA-Z_]\\w*\\b)|', 
        'g' // Bandera global para encontrar todas las coincidencias
    );

    let resultadoHTML = '';
    let ultimoIndice = 0;
    
    // matchAll devuelve un iterador con todas las coincidencias
    for (const match of texto.matchAll(regex)) {
        const [token, strDoble, strSimple, comentario, palabraClave, numero, signo, functions, ignorar, otraPalabra] = match;
        const inicio = match.index;
        
        // 1. Agregar el texto sin resaltar que estaba antes del token
        // Esto maneja espacios, saltos de línea y texto que no coincide.
        resultadoHTML += texto.substring(ultimoIndice, inicio);

        let claseCSS = '';

        // 2. Determinar la clase CSS del token
        if (strDoble) {
            claseCSS = 'string';
        } else if (strSimple) {
            claseCSS = 'expresion';
        } else if (comentario) {
            claseCSS = 'comment';
        } else if (palabraClave) {
            claseCSS = 'keyword';
        } else if (numero) {
            claseCSS = 'number';
        } else if (signo) {
            claseCSS = 'operator';
        } else if (otraPalabra) {
            claseCSS = 'identifier';
        } else if (functions){
            claseCSS = 'function';
        } else {
            claseCSS = 'plain';
        }
        
        // 3. Envolver el token en un span con la clase determinada
        resultadoHTML += `<span class="${claseCSS}">${token}</span>`;

        // 4. Actualizar el índice para la próxima iteración
        ultimoIndice = inicio + token.length;
    }

    // 5. Agregar el texto restante después del último token
    resultadoHTML += texto.substring(ultimoIndice);

    return resultadoHTML;
}

document.addEventListener('DOMContentLoaded', () => {
    const elementosCodigo = document.querySelectorAll('.heza-code');
    elementosCodigo.forEach(elemento => {
        const textoOriginal = elemento.textContent;
        const textoResaltado = resaltarCodigo(textoOriginal);
        elemento.innerHTML = textoResaltado;
    });
});
