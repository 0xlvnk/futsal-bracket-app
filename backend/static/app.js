const teamList = document.getElementById("teamList");
const statusMessage = document.getElementById("statusMessage");
const teamCount = document.getElementById("teamCount");
const refreshBtn = document.getElementById("refreshBtn");
const teamForm = document.getElementById("teamForm");
const formMessage = document.getElementById("formMessage");
const teamNameInput = document.getElementById("teamName");
const teamCategoryInput = document.getElementById("teamCategory");

function showFormMessage(message, type) {
  formMessage.textContent = message;
  formMessage.className = `status ${type}`;
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

teamForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const name = teamNameInput.value.trim();
  const category = teamCategoryInput.value.trim();

  if (!name || !category) {
    showFormMessage("Nama tim dan kategori wajib diisi.", "error");
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

    showFormMessage("Tim berhasil ditambahkan.", "success");
    teamForm.reset();
    await loadTeams();
  } catch (error) {
    showFormMessage(error.message, "error");
  }
});

refreshBtn.addEventListener("click", loadTeams);
loadTeams();