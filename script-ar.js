function renderBooks() {
  const loadingIndicator = document.getElementById("loading-indicator");
              const e = document.getElementById("book-list");
              // Clear previous books
  e.innerHTML = "";
    fetch("books-ar.json").then((t => t.json())).then((t => {
        if (t && t.length > 0) {
    loadingIndicator.style.display = "none";

        function n(t) {
            e.innerHTML = "", t.sort(((t, e) => t.year.match(/\d+/)[0] > e.year.match(/\d+/)[0] ? 1 : e.year.match(/\d+/)[0] > t.year.match(/\d+/)[0] ? -1 : 0)).forEach((t => {
                const n = document.createElement("li");
                n.className = "box", n.innerHTML = `\n\t\t\t\t\t\t<strong>\n\t\t\t\t\t\t\t<a href="https://cdn.solaranamnesis.com/library-test/examples/book_shelf-ar.html#${t.id}">${t.title}</a>\n\t\t\t\t\t\t</strong> — ${t.author} (${t.year}) \t\t\n\t\t\t\t\t\t<br>\n\t\t\t\t\t\t\t<small>\n\t\t\t\t\t\t\t\t<b>اللغات:</b> ${t.languages}\n\t\t\t\t\t\t\t</small>\n\t\t\t\t\t\t\t<br>\n\t\t\t\t\t\t\t\t<small>\n\t\t\t\t\t\t\t\t\t<b>الموضوعات:</b> ${t.subjects}\n\t\t\t\t\t\t\t\t</small>\n            `, e.appendChild(n)
            }))
        }

        function a(t, e, n) {
            return n.indexOf(t) === e
        }

        function l() {
            const e = document.getElementById("language-select").value,
                a = document.getElementById("year-select").value,
                l = document.getElementById("subject-select").value,
                c = document.getElementById("author-select").value;
            n(t.filter((t => {
                const n = "اختر اللغة" === e || t.languages.includes(e),
                    s = "اختر السنة" === a || t.year.includes(a),
                    o = "اختر الموضوع" === l || t.subjects.includes(l),
                    r = "اختر المؤلف" === c || t.author.includes(c);
                return n && s && o && r
            })))
        }

        function c(t, e) {
            const n = document.getElementById(t);
            e.forEach((t => {
                const e = document.createElement("option");
                e.value = t, e.textContent = t, n.appendChild(e)
            }))
        }
        const s = t.flatMap((t => t.languages.split(",").map((t => t.trim())))).filter(a).sort(),
            o = t.map((t => t.year.match(/\d+/)[0])).filter(a).sort(),
            r = t.flatMap((t => t.subjects.split(",").map((t => t.trim())))).filter(a).sort(),
            d = t.flatMap((t => t.author.split(",").map((t => t.trim())))).filter(a).sort();
        c("language-select", s), c("year-select", o), c("subject-select", r), c("author-select", d), n(t), document.getElementById("language-select").addEventListener("change", l), document.getElementById("year-select").addEventListener("change", l), document.getElementById("subject-select").addEventListener("change", l), document.getElementById("author-select").addEventListener("change", l)
        
        } else {
          // Retry after delay if data is invalid or empty
          console.log('books not found, retrying the request to fetch books json in 1 second...');
          setTimeout(renderBooks, 1000);
        }
    })).catch((t => console.error("Error:", t)))
}
document.addEventListener("DOMContentLoaded", renderBooks);
