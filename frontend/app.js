async function load() {
    const res = await fetch("/api/fotos");
    const data = await res.json();

    const g = document.getElementById("galeria");

    data.forEach(f => {
        g.innerHTML += `<img src="${encodeURI(f.url)}" width="300">`;
    });
}

load();