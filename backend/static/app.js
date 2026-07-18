const teamList = document.getElementById("teamList");
const statusMessage = document.getElementById("statusMessage");
const teamCount = document.getElementById("teamCount");
const refreshBtn = document.getElementById("refreshBtn");

async function loadTeams() {
  statusMessage.textContent = "Memuat data tim...";
  teamList.innerHTML = "";

  try {
    const response = await fetch("/teams");
    const teams = await response.json();

    if (!response.ok) {
      throw new Error("Gagal mengambil data tim");
    }

    teamCount.textContent = `${teams.length} tim`;

    if (teams.length === 0) {
      statusMessage.textContent = "Belum ada tim di database.";
      teamList.innerHTML = `
        <div class="empty-state">
          Belum ada data tim. Tambahkan tim lewat endpoint POST /teams dulu.
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

refreshBtn.addEventListener("click", loadTeams);
loadTeams();