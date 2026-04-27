// Frontend-delen dekker oppgavekravet om å vise API-data i nettleser.

function getApiBaseUrl() {
    // Leser API-base fra config slik at samme frontend kan peke mot lokal eller live backend.
    if (window.APP_CONFIG && window.APP_CONFIG.API_BASE_URL) {
        return window.APP_CONFIG.API_BASE_URL.replace(/\/$/, "");
    }
    return "";
}

const API_BASE_URL = getApiBaseUrl();
document.getElementById("api-base").textContent =
    API_BASE_URL ? `API: ${API_BASE_URL}` : "API: samme origin som frontend";

function apiUrl(path) {
    return `${API_BASE_URL}${path}`;
}

async function fetchJson(url) {
    // Felles funksjon for henting fra API som også stopper videre rendering ved feil.
    const response = await fetch(url);
    const payload = await response.json();
    if (!response.ok || !payload.ok) {
        throw new Error(payload.message || "Ukjent feil fra server.");
    }
    return payload;
}

function setText(id, text, isError = false) {
    const el = document.getElementById(id);
    el.textContent = text;
    el.classList.toggle("status-error", isError);
}

function renderVarelager(items) {
    const body = document.querySelector("#vare-tabell tbody");
    body.innerHTML = "";
    // Løkken bygger opp tabellen rad for rad fra JSON-responsen fra backend.
    for (const item of items) {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.VNr}</td>
            <td>${item.Betegnelse}</td>
            <td>${item.Antall}</td>
            <td>${Number(item.Pris).toFixed(2)} kr</td>
        `;
        body.appendChild(row);
    }
}

function renderOrdrer(items) {
    const body = document.querySelector("#ordre-tabell tbody");
    body.innerHTML = "";
    // Samme prinsipp brukes for ordreliste, slik at bruker kan teste flere API-ruter i browser.
    for (const item of items) {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.OrdreNr}</td>
            <td>${item.OrdreDato ?? "-"}</td>
            <td>${item.SendtDato ?? "-"}</td>
            <td>${item.BetaltDato ?? "-"}</td>
            <td>${item.KNr}</td>
        `;
        body.appendChild(row);
    }
}

async function loadVarelager() {
    setText("vare-status", "Laster varelager...");
    try {
        // Oppgavekrav: varelager skal også kunne vises i browser via API.
        const result = await fetchJson(apiUrl("/api/varelager"));
        renderVarelager(result.items);
        setText("vare-status", `Viser ${result.count} varer.`);
    } catch (error) {
        setText("vare-status", `Feil: ${error.message}`, true);
    }
}

async function loadOrdrer() {
    setText("ordre-status", "Laster ordre...");
    try {
        // Dette er ekstra funksjonalitet i nettleseren utover minimumskravet om varelager.
        const result = await fetchJson(apiUrl("/api/ordrer"));
        renderOrdrer(result.items);
        setText("ordre-status", `Viser ${result.count} ordre.`);
    } catch (error) {
        setText("ordre-status", `Feil: ${error.message}`, true);
    }
}

document.getElementById("load-varelager").addEventListener("click", loadVarelager);
document.getElementById("load-ordrer").addEventListener("click", loadOrdrer);

loadVarelager();
