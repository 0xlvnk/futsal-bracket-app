const teamList = document.getElementById("teamList");
const statusMessage = document.getElementById("statusMessage");
const teamCount = document.getElementById("teamCount");
const refreshBtn = document.getElementById("refreshBtn");
const teamForm = document.getElementById("teamForm");
const formMessage = document.getElementById("formMessage");
const teamNameInput = document.getElementById("teamName");
const teamCategoryInput = document.getElementById("teamCategory");

const matchForm = document.getElementById("matchForm");
const matchMessage = document.getElementById("matchMessage");
const matchList = document.getElementById("matchList");
const matchCount = document.getElementById("matchCount");
const matchStatusMessage = document.getElementById("matchStatusMessage");
const roundNameInput = document.getElementById("roundName");
const matchCodeInput = document.getElementById("matchCode");
const team1Select = document.getElementById("team1Select");
const team2Select = document.getElementById("team2Select");

let cachedTeams = [];

function showMessage(element, message, type) {
  element.textContent = message;
  element.className = `status ${type}`;
}

function fillTeamSelects(teams) {
  const options = ['<option value="">Pilih tim</option>']
    .concat(
      teams.map(team => `<option value="${team.id}">${team.name} (${team.category})</option>`)
    )
    .join("");

  team1Select.innerHTML = options;
  team2Select.innerHTML = options;
}

async function loadTeams() {
  statusMessage.textContent = "Memuat data tim...";
  teamList.innerHTML = "";

  try {
    const response = await fetch("/teams");
    const teams = await response.json();

    if (!response.ok) {
      throw new Error("Gagal mengambil data tim");
    }

    cachedTeams = teams;
    fillTeamSelects(teams);

    teamCount.textContent = `${teams.length} tim`;

    if (teams.length === 0) {
      statusMessage.textContent = "Belum ada tim di database.";
      teamList.innerHTML = `
        <div class="empty-state">
          Belum ada data tim. Tambahkan tim melalui form di atas.
        </div>
      `;
      return;
    }

    statusMessage.textContent = "Data tim berhasil dimuat.";

    teamList.innerHTML = teams.map(team => `
      <div class="team-item">
        <h4>${team.name}</h4>
        <p>Kategori: ${team.category}</p>
        <p>ID: ${team.id}</p>
      </div>
    `).join("");
  } catch (error) {
    teamCount.textContent = "0 tim";
    statusMessage.textContent = "Terjadi error saat mengambil data tim.";
    teamList.innerHTML = `
      <div class="empty-state">
        ${error.message}
      </div>
    `;
  }
}

async function loadMatches() {
  matchStatusMessage.textContent = "Memuat data match...";
  matchList.innerHTML = "";

  try {
    const response = await fetch("/matches");
    const matches = await response.json();

    if (!response.ok) {
      throw new Error("Gagal mengambil data match");
    }

    matchCount.textContent = `${matches.length} match`;

    if (matches.length === 0) {
      matchStatusMessage.textContent = "Belum ada match di database.";
      matchList.innerHTML = `
        <div class="empty-state">
          Belum ada data match. Tambahkan match melalui form di atas.
        </div>
      `;
      return;
    }

    matchStatusMessage.textContent = "Data match berhasil dimuat.";

    matchList.innerHTML = matches.map(match => `
      <div class="team-item">
        <h4>${match.match_code} - ${match.round_name}</h4>
        <p>${match.team1_name || "-"} vs ${match.team2_name || "-"}</p>
        <p>Skor: ${match.home_score ?? "-"} - ${match.away_score ?? "-"}</p>
        <p>Pemenang: ${match.winner_name || "-"}</p>
      </div>
    `).join("");
  } catch (error) {
    matchCount.textContent = "0 match";
    matchStatusMessage.textContent = "Terjadi error saat mengambil data match.";
    matchList.innerHTML = `
      <div class="empty-state">
        ${error.message}
      </div>
    `;
  }
}

teamForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const name = teamNameInput.value.trim();
  const category = teamCategoryInput.value.trim();

  if (!name || !category) {
    showMessage(formMessage, "Nama tim dan kategori wajib diisi.", "error");
    return;
  }

  try {
    const response = await fetch("/teams", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name, category })
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Gagal menambahkan tim");
    }

    showMessage(formMessage, "Tim berhasil ditambahkan.", "success");
    teamForm.reset();
    await loadTeams();
  } catch (error) {
    showMessage(formMessage, error.message, "error");
  }
});

matchForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const round_name = roundNameInput.value.trim();
  const match_code = matchCodeInput.value.trim();
  const team1_id = Number(team1Select.value);
  const team2_id = Number(team2Select.value);

  if (!round_name || !match_code || !team1_id || !team2_id) {
    showMessage(matchMessage, "Semua field match wajib diisi.", "error");
    return;
  }

  if (team1_id === team2_id) {
    showMessage(matchMessage, "Team 1 dan Team 2 tidak boleh sama.", "error");
    return;
  }

  try {
    const response = await fetch("/matches", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        round_name,
        match_code,
        team1_id,
        team2_id
      })
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Gagal menambahkan match");
    }

    showMessage(matchMessage, "Match berhasil ditambahkan.", "success");
    matchForm.reset();
    await loadMatches();
  } catch (error) {
    showMessage(matchMessage, error.message, "error");
  }
});

refreshBtn.addEventListener("click", async () => {
  await loadTeams();
  await loadMatches();
});

async function initPage() {
  await loadTeams();
  await loadMatches();
}

initPage();