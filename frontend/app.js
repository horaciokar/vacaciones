async function load() {
    const res = await fetch("/api/fotos");
    const data = await res.json();

    const g = document.getElementById("galeria");
    g.innerHTML = "";

    data.forEach(f => {
        const url = encodeURI(f.url);

        const div = document.createElement("div");

        const img = document.createElement("img");
        img.src = url;
        img.width = 300;

        const p = document.createElement("p");
        p.textContent = f.nombre;

        div.appendChild(img);
        div.appendChild(p);

        g.appendChild(div);
    });
}

load();