console.log("✅ admin.js loaded");

function showNotification(message, type = "info") {
  const existing = document.querySelector(".notification");
  if (existing) existing.remove();

  const notification = document.createElement("div");
  notification.className = `notification ${type}`;
  notification.textContent = message;

  document.querySelector(".container").prepend(notification);

  setTimeout(() => {
    notification.remove();
  }, 4000);
}

function addSubjectRow(subject = {}) {
  const tbody = document.querySelector("#subjectTable tbody");
  const row = document.createElement("tr");

  row.innerHTML = `
    <td><input type="text" class="sub-name" value="${
      subject.name || ""
    }" /></td>
    <td><input type="number" class="sub-hours" value="${
      subject.hours_per_week || 3
    }" min="1" /></td>
    <td><input type="text" class="sub-prof-name" value="${
      subject.professor_name || ""
    }" /></td>
    <td><button class="delete-btn">🗑️</button></td>
  `;

  tbody.appendChild(row);

  row.querySelector(".delete-btn").addEventListener("click", () => {
    if (confirm("Are you sure you want to delete this subject?")) {
      row.remove();
    }
  });
}

function validateForm() {
  const branch = document.getElementById("branch").value.trim();
  const semester = document.getElementById("semester").value.trim();
  if (!branch) {
    showNotification("Branch is required.", "error");
    return false;
  }
  if (!semester || isNaN(semester) || semester <= 0) {
    showNotification("Valid semester is required.", "error");
    return false;
  }
  return true;
}

function setLoading(button, isLoading) {
  if (isLoading) {
    button.disabled = true;
    button.dataset.originalText = button.textContent;
    button.textContent = "⏳ Please wait...";
  } else {
    button.disabled = false;
    button.textContent = button.dataset.originalText;
  }
}

function saveSubjects() {
  if (!validateForm()) return;

  const branch = document.getElementById("branch").value.trim();
  const semester = document.getElementById("semester").value.trim();
  const rows = document.querySelectorAll("#subjectTable tbody tr");

  const subjects = Array.from(rows).map((row) => ({
    name: row.querySelector(".sub-name").value,
    hours: parseInt(row.querySelector(".sub-hours").value),
    professor_name: row.querySelector(".sub-prof-name").value,
  }));

  const saveBtn = document.querySelector("button[onclick='saveSubjects()']");
  setLoading(saveBtn, true);

  fetch("/save_subjects", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ branch, semester, subjects }),
  })
    .then((res) => res.json())
    .then(() => {
      showNotification("✅ Subjects saved successfully!", "success");
    })
    .catch((err) => {
      console.error(err);
      showNotification("❌ Failed to save subjects.", "error");
    })
    .finally(() => {
      setLoading(saveBtn, false);
    });
}

function loadSubjects() {
  if (!validateForm()) return;

  const branch = document.getElementById("branch").value.trim();
  const semester = document.getElementById("semester").value.trim();

  const loadBtn = document.querySelector("button[onclick='loadSubjects()']");
  setLoading(loadBtn, true);

  fetch(`/get_subjects?branch=${branch}&semester=${semester}`)
    .then((res) => res.json())
    .then((data) => {
      const tbody = document.querySelector("#subjectTable tbody");
      tbody.innerHTML = "";
      data.subjects.forEach(addSubjectRow);
      showNotification("📂 Subjects loaded successfully!", "success");
    })
    .catch((err) => {
      console.error(err);
      showNotification("❌ Failed to load subjects.", "error");
    })
    .finally(() => {
      setLoading(loadBtn, false);
    });
}

function generateTimetable() {
  if (!validateForm()) return;

  const branch = document.getElementById("branch").value.trim();
  const semester = document.getElementById("semester").value.trim();

  const rows = document.querySelectorAll("#subjectTable tbody tr");
  if (rows.length === 0) {
    showNotification(
      "Please add at least one subject before generating timetable.",
      "error"
    );
    return;
  }

  const genBtn = document.querySelector(
    "button[onclick='generateTimetable()']"
  );
  setLoading(genBtn, true);

  fetch("/generate_timetable", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ branch, semester }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "already_exists") {
        showNotification(
          "📌 Timetable already exists! Redirecting to view...",
          "info"
        );
      } else {
        showNotification("✅ Timetable generated successfully!", "success");
      }
      window.location.href = `/view_timetable?branch=${branch}&semester=${semester}`;
    })
    .catch((err) => {
      console.error("❌ Error generating timetable:", err);
      showNotification("Failed to generate timetable.", "error");
    })
    .finally(() => {
      setLoading(genBtn, false);
    });
}

function resetTimetable() {
  if (!validateForm()) return;

  const branch = document.getElementById("branch").value.trim();
  const semester = document.getElementById("semester").value.trim();

  if (
    !confirm(
      `Are you sure you want to reset timetable for ${branch} Semester ${semester}?`
    )
  ) {
    return;
  }

  const resetBtn = document.querySelector("button.reset-btn");
  setLoading(resetBtn, true);

  fetch("/reset_timetable", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ branch, semester }),
  })
    .then((res) => res.json())
    .then(() => {
      showNotification(
        "🧹 Timetable reset successfully! You can generate a new one now.",
        "success"
      );
    })
    .catch((err) => {
      console.error("❌ Error resetting timetable:", err);
      showNotification("Failed to reset timetable.", "error");
    })
    .finally(() => {
      setLoading(resetBtn, false);
    });
}
