const SYMPTOMS = [
    "Demam", "Mual", "Muntah", "Lemas", "Mencret", "Kejang", "Tenggorokan sakit",
    "Bintik merah", "Mimisan", "Nyeri sendi", "Pusing", "Leukosit", "Hematokrit", "Trombosit"
];

const GRADES = ["DHF-I", "DHF-II", "DHF-III", "DHF-IV"];

const GRADE_NAMES = {
    "DHF-I": "Demam Berdarah Grade I",
    "DHF-II": "Demam Berdarah Grade II",
    "DHF-III": "Demam Berdarah Grade III",
    "DHF-IV": "Demam Berdarah Grade IV"
};

const DATASET = {
    "DHF-I": [1, 8, 12, 13, 14],
    "DHF-II": [1, 8, 9, 12, 13, 14],
    "DHF-III": [1, 8, 9, 10, 12, 13, 14],
    "DHF-IV": [1, 6, 10, 12, 13, 14]
};

const EXAMPLE = [1, 2, 4, 8, 9, 10];

const EXCEL = {
    same: [2, 3, 4, 2],
    cosine: [0.3651483716701107, 0.5, 0.6172133998483676, 0.3333333333333333],
    distance: [2.6457513110645907, 2.449489742783178, 2.23606797749979, 2.8284271247461903],
    jaccard: [0.2222222222222222, 0.3333333333333333, 0.4444444444444444, 0.2]
};

const STORAGE_KEY = "dbd_extra";

const $ = id => document.getElementById(id);
const toVector = numbers => SYMPTOMS.map((_, index) => numbers.includes(index + 1) ? 1 : 0);
const format = value => value.toFixed(4);
const escapeHtml = text => String(text).replace(/[&<>"']/g, char => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
}[char]));
const symptomNames = vector => vector.map((on, index) => on ? SYMPTOMS[index] : "").filter(Boolean).join(", ");

const baseCases = GRADES.map(grade => ({
    grade,
    source: "Dataset (Excel)",
    vector: toVector(DATASET[grade])
}));

let savedCases = loadSavedCases();

function loadSavedCases() {
    try {
        const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
        if (!Array.isArray(data)) return [];

        return data
            .filter(item => Array.isArray(item.vector || item.v) && (item.vector || item.v).length === SYMPTOMS.length)
            .map(item => ({
                vector: item.vector || item.v,
                grade: item.grade || item.g,
                source: item.source || item.src || "Kasus tersimpan"
            }));
    } catch {
        return [];
    }
}

function allCases() {
    return [...baseCases, ...savedCases];
}

function persistCases() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(savedCases));
    } catch (error) {
        console.error("Gagal menyimpan kasus", error);
    }
    renderCaseList();
}

function compare(a, b) {
    let same = 0;
    let countA = 0;
    let countB = 0;
    let squared = 0;

    for (let i = 0; i < a.length; i++) {
        same += a[i] * b[i];
        countA += a[i];
        countB += b[i];
        squared += (a[i] - b[i]) ** 2;
    }

    const denominator = Math.sqrt(countA * countB);
    const union = countA + countB - same;

    return {
        same,
        cosine: denominator ? same / denominator : 0,
        jaccard: union ? same / union : 0,
        distance: Math.sqrt(squared)
    };
}

function diagnose(selected) {
    const vector = toVector(selected);
    const rows = allCases().map((item, index) => ({
        no: index + 1,
        grade: item.grade,
        source: item.source,
        ...compare(vector, item.vector)
    }));

    const best = Math.max(...rows.map(row => row.cosine));

    rows.forEach(row => {
        row.rank = 1 + rows.filter(other => other.cosine > row.cosine + 1e-9).length;
        row.winner = best > 0 && Math.abs(row.cosine - best) < 1e-9;
    });

    const winners = rows.filter(row => row.winner);
    const grades = [...new Set(winners.map(row => row.grade))];

    return {
        selected,
        vector,
        rows,
        best,
        winners,
        grades,
        final: grades.length === 1 ? grades[0] : grades.length > 1 ? "SERI" : null
    };
}

function showStep(step) {
    ["p1", "p2", "p3"].forEach(id => $(id).classList.toggle("hide", id !== step));
}

function renderSymptoms() {
    $("gej").innerHTML = SYMPTOMS.map((name, index) => `
        <label class="sym">
            <input type="checkbox" value="${index + 1}">
            <span>${name}</span>
        </label>
    `).join("");
}

function checkboxes() {
    return [...$("gej").querySelectorAll("input")];
}

function selectedSymptoms() {
    return checkboxes().filter(box => box.checked).map(box => Number(box.value));
}

function renderCaseList() {
    const rows = allCases().map((item, index) => `
        <tr>
            <td>${index + 1}</td>
            <td class="l w">${symptomNames(item.vector)}</td>
            <td>${item.grade}</td>
            <td>${item.source}</td>
            <td>${index >= baseCases.length ? `<button data-remove="${index - baseCases.length}">Hapus</button>` : ""}</td>
        </tr>
    `).join("");

    $("kl").innerHTML = `
        <div class="tw">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th class="l">Gejala</th>
                        <th>Grade</th>
                        <th>Sumber</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
        </div>`;
    $("clr").disabled = savedCases.length === 0;
}

function renderTable(headers, rows, highlight = []) {
    return `
        <div class="tw">
            <table>
                <thead>
                    <tr>${headers.map((head, index) => `<th${index ? "" : ' class="l"'}>${head}</th>`).join("")}</tr>
                </thead>
                <tbody>
                    ${rows.map((cells, index) => `
                        <tr${highlight[index] ? ' class="top"' : ""}>
                            ${cells.map((cell, cellIndex) => `<td${cellIndex ? "" : ' class="l"'}>${cell}</td>`).join("")}
                        </tr>
                    `).join("")}
                </tbody>
            </table>
        </div>`;
}

function renderResult(result) {
    const patient = {
        name: escapeHtml($("nama").value.trim()),
        gender: $("jk").value,
        age: $("umur").value
    };
    const selectedNames = result.selected.map(number => SYMPTOMS[number - 1]).join(", ");

    let html = `
        <div class="card">
            <h2>Hasil diagnosis</h2>
            <p>Pasien: <b>${patient.name}</b> · ${patient.gender} · ${patient.age} tahun</p>
            <p>Gejala dipilih: ${selectedNames}</p>
            <p class="mut">Representasi biner: ${result.vector.join(" ")}</p>
            <p class="note">Hasil ini hanya implementasi metode untuk pembelajaran dan harus dikonfirmasi tenaga medis.</p>
        </div>
        <div class="card">
            <h2>Klasifikasi akhir</h2>`;

    if (result.final && result.final !== "SERI") {
        const winnerList = result.winners.map(row => `#${row.no}`).join(", ");
        html += `
            <p class="big">${result.final} — ${GRADE_NAMES[result.final]}</p>
            <p>Kasus ${winnerList} memiliki cosine tertinggi, yaitu <b>${format(result.best)}</b>. Grade diambil dari kasus tersebut.</p>`;
    } else if (result.final === "SERI") {
        html += `<p class="bad">Seri antara ${result.grades.join(" dan ")} dengan cosine ${format(result.best)}. Perlu keputusan pakar.</p>`;
    } else {
        html += `<p class="bad">Tidak ada kasus yang memiliki gejala sama dengan input, sehingga grade tidak dapat ditentukan.</p>`;
    }

    html += `</div>`;

    const similarityRows = result.rows.map(row => [
        `#${row.no}`,
        row.grade,
        row.source,
        row.same,
        format(row.cosine),
        format(row.jaccard),
        format(row.distance),
        row.rank
    ]);

    html += `
        <div class="card">
            <h2>Similarity terhadap setiap kasus</h2>
            <p class="mut">sama = jumlah (input × kasus); cosine = sama / (√gejala input × √gejala kasus); SV = sama / (input + kasus − sama); d = √jumlah (input − kasus)². Peringkat memakai cosine terbesar.</p>
            ${renderTable(
                ["Kasus", "Grade", "Sumber", "Sama", "Cosine", "SV", "Jarak d", "Peringkat"],
                similarityRows,
                result.rows.map(row => row.winner)
            )}
        </div>`;

    const isExample = result.selected.length === EXAMPLE.length && EXAMPLE.every(number => result.selected.includes(number));
    if (isExample) {
        const matches = GRADES.every((_, index) => {
            const row = result.rows[index];
            return row.same === EXCEL.same[index]
                && Math.abs(row.cosine - EXCEL.cosine[index]) < 1e-9
                && Math.abs(row.distance - EXCEL.distance[index]) < 1e-9
                && Math.abs(row.jaccard - EXCEL.jaccard[index]) < 1e-9;
        });

        html += `
            <div class="card">
                <h2>Validasi terhadap Excel (K1)</h2>
                <p>Nilai sama, cosine, SV, dan jarak untuk keempat grade: <span class="${matches ? "ok" : "bad"}">${matches ? "identik dengan Excel" : "berbeda dari Excel"}</span>.</p>
                <p class="note">Sel "Diagnosis diharapkan" di Excel berisi DHF-II, tetapi rumus Excel menghasilkan DHF-III. Nilai harapan tersebut perlu dikonfirmasi pemilik file.</p>
            </div>`;
    }

    const canRetain = result.final && result.final !== "SERI";

    html += `
        <div class="card">
            <h2>Retain</h2>
            <p class="mut">Simpan kasus ini ke basis kasus hanya setelah hasilnya dikonfirmasi tenaga medis.</p>
            <div class="row">
                <button id="ret"${canRetain ? "" : " disabled"}>Simpan sebagai kasus baru</button>
            </div>
            <p id="rm" class="mut"></p>
            <div class="row">
                <button id="b2">← Kembali ke gejala</button>
                <button id="rs">Reset gejala</button>
                <button class="p" id="re">Diagnosis ulang</button>
            </div>
        </div>`;

    $("p3").innerHTML = html;

    $("ret").onclick = () => {
        savedCases.push({
            vector: result.vector,
            grade: result.final,
            source: "Kasus tersimpan"
        });
        persistCases();
        $("ret").disabled = true;
        $("rm").textContent = `Kasus disimpan sebagai ${result.final}.`;
    };

    $("b2").onclick = () => showStep("p2");

    $("rs").onclick = () => {
        checkboxes().forEach(box => { box.checked = false; });
        showStep("p2");
    };

    $("re").onclick = () => {
        checkboxes().forEach(box => { box.checked = false; });
        $("nama").value = "";
        $("jk").value = "";
        $("umur").value = "";
        $("e1").textContent = "";
        $("e2").textContent = "";
        showStep("p1");
        window.scrollTo(0, 0);
    };
}

$("lanjut").onclick = () => {
    const missing = [];

    if (!$("nama").value.trim()) missing.push("nama");
    if (!$("jk").value) missing.push("jenis kelamin");
    if ($("umur").value === "") missing.push("umur");

    $("e1").textContent = missing.length ? `Input belum lengkap: ${missing.join(", ")}.` : "";

    if (!missing.length) {
        $("e2").textContent = "";
        showStep("p2");
        window.scrollTo(0, 0);
    }
};

$("back1").onclick = () => showStep("p1");

$("all").onclick = () => {
    checkboxes().forEach(box => { box.checked = true; });
    $("e2").textContent = "";
};

$("none").onclick = () => {
    checkboxes().forEach(box => { box.checked = false; });
    $("e2").textContent = "";
};

$("ex").onclick = () => {
    checkboxes().forEach(box => { box.checked = EXAMPLE.includes(Number(box.value)); });
    $("e2").textContent = "";
};

$("go").onclick = () => {
    const selected = selectedSymptoms();

    if (!selected.length) {
        $("e2").textContent = "Pilih minimal satu gejala terlebih dahulu.";
        return;
    }

    $("e2").textContent = "";
    renderResult(diagnose(selected));
    showStep("p3");
    window.scrollTo(0, 0);
};

$("kl").addEventListener("click", event => {
    const index = event.target.dataset.remove;
    if (index === undefined) return;

    savedCases.splice(Number(index), 1);
    persistCases();
});

$("clr").onclick = () => {
    if (!savedCases.length || !confirm("Hapus semua kasus tersimpan?")) return;

    savedCases = [];
    persistCases();
};

renderSymptoms();
renderCaseList();
