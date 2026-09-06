const form = document.querySelector("#employee-form");
const list = document.querySelector("#employee-list");
const search = document.querySelector("#search");
const message = document.querySelector("#form-message");
const themeToggle = document.querySelector("#theme-toggle");
const themeIcon = themeToggle.querySelector(".theme-icon");
const themeLabel = themeToggle.querySelector(".theme-label");
let employees = [];

const fields = ["name", "email", "department", "role", "salary"];

function applyTheme(theme) {
	document.documentElement.dataset.theme = theme;
	const isDark = theme === "dark";
	themeIcon.textContent = isDark ? "☀" : "☾";
	themeLabel.textContent = isDark ? "Light mode" : "Dark mode";
	themeToggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
	themeToggle.title = isDark ? "Switch to light mode" : "Switch to dark mode";
}

const savedTheme = localStorage.getItem("employee-management-theme") || "light";
applyTheme(savedTheme === "dark" ? "dark" : "light");

themeToggle.addEventListener("click", () => {
	const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
	localStorage.setItem("employee-management-theme", nextTheme);
	applyTheme(nextTheme);
});

function render() {
	const query = search.value.toLowerCase().trim();
	const visible = employees.filter((employee) =>
		[employee.name, employee.email, employee.department, employee.role]
			.some((value) => value.toLowerCase().includes(query))
	);
	document.querySelector("#employee-count").textContent = employees.length;
	list.innerHTML = visible.length ? visible.map((employee) => `
		<article class="employee-card">
			<div class="avatar">${employee.name.charAt(0).toUpperCase()}</div>
			<div class="employee-info"><h3>${employee.name}</h3><p>${employee.role} · ${employee.department}</p><a href="mailto:${employee.email}">${employee.email}</a></div>
			<div class="employee-actions"><span class="salary">INR ${Number(employee.salary).toLocaleString("en-IN")}</span><button data-action="edit" data-id="${employee.id}" aria-label="Edit ${employee.name}">Edit</button><button data-action="delete" data-id="${employee.id}" aria-label="Delete ${employee.name}">Delete</button></div>
		</article>`).join("") : '<p class="empty-state">No employees match that search.</p>';
}

async function loadEmployees() {
	const response = await fetch("/api/employees");
	employees = await response.json();
	render();
}

function resetForm() {
	form.reset();
	document.querySelector("#employee-id").value = "";
	document.querySelector("#form-title").textContent = "Add employee";
	document.querySelector("#submit-label").textContent = "Add employee";
	document.querySelector("#cancel-edit").classList.add("hidden");
}

form.addEventListener("submit", async (event) => {
	event.preventDefault();
	const id = document.querySelector("#employee-id").value;
	const payload = Object.fromEntries(fields.map((field) => [field, document.querySelector(`#${field}`).value]));
	const response = await fetch(id ? `/api/employees/${id}` : "/api/employees", {
		method: id ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
	});
	const result = await response.json();
	if (!response.ok) { message.textContent = result.error; return; }
	message.textContent = id ? "Employee updated." : "Employee added.";
	resetForm();
	await loadEmployees();
});

list.addEventListener("click", async (event) => {
	const button = event.target.closest("button");
	if (!button) return;
	const employee = employees.find((item) => item.id === Number(button.dataset.id));
	if (button.dataset.action === "edit") {
		fields.forEach((field) => { document.querySelector(`#${field}`).value = employee[field]; });
		document.querySelector("#employee-id").value = employee.id;
		document.querySelector("#form-title").textContent = "Edit employee";
		document.querySelector("#submit-label").textContent = "Save changes";
		document.querySelector("#cancel-edit").classList.remove("hidden");
		document.querySelector("#name").focus();
	} else if (confirm(`Delete ${employee.name}?`)) {
		await fetch(`/api/employees/${employee.id}`, { method: "DELETE" });
		await loadEmployees();
	}
});

document.querySelector("#cancel-edit").addEventListener("click", resetForm);
search.addEventListener("input", render);
loadEmployees();
