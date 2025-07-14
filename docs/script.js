document.addEventListener("DOMContentLoaded", () => {
      const textarea = document.querySelector(".code");
      const preview  = document.querySelector(".preview");

      const keywords  = ["data", "trace", "out", "in", "loop", "end", "block", "as", "CLS", "default?", "condition"];
      const constants = ["LINE", "TAB", "ESP", "PI", "E"];
      const ops       = ["->", "\\+", "-", "\\*", "/", "%", "\\^", "=", ">=", "<=", ">", "<", ":", "\\?", "not", "and", "or"];

      function escapeHtml(s) {
        return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
      }

      function highlight(code) {
  // Escapamos primero
  let out = code
    .replace(/&/g,"&amp;")
    .replace(/</g,"&lt;")
    .replace(/>/g,"&gt;");

  // Aplicamos resaltado sobre texto plano y escapado
// Comentarios: buscar '@' ya escapado como '&#64;'
    out = out.replace(/&#64;[^\n\r]*/g, m => `<span class="comment">${m}</span>`);
  out = out.replace(/"([^"\\]|\\.)*"/g, m => `<span class="string">${m}</span>`);
  out = out.replace(/\b\d+(\.\d+)?\b/g, m => `<span class="number">${m}</span>`);

  [...keywords, ...constants].forEach(word => {
    out = out.replace(new RegExp(`\\b${word}\\b`, "g"), m => `<span class="keyword">${m}</span>`);
  });

  // Procesamos operadores con cuidado
  ops.sort((a,b) => b.length - a.length).forEach(op => {
    const pattern = new RegExp(`\\b${op}\\b`, "g"); // No coincide con <> porque ya están escapados
    out = out.replace(pattern, m => `<span class="operator">${m}</span>`);
  });

  return out;
}


      function update() {
        preview.innerHTML = highlight(textarea.value);
      }

      textarea.addEventListener("input", update);
      update();
    });