// ===============================
// GLOBAL VARIABLES
// ===============================
let pieChart = null;

const categoryColors = {
    "Groceries": "#22c55e",
    "Food & Dining": "#f97316",
    "Transport": "#3b82f6",
    "Fuel": "#facc15",
    "Shopping": "#ec4899",
    "Entertainment": "#8b5cf6",
    "Health & Medical": "#ef4444",
    "Education": "#14b8a6",
    "Rent": "#6366f1",
    "Subscriptions": "#a855f7",
    "Other": "#64748b"
};

// ===============================
// DOM READY
// ===============================
document.addEventListener("DOMContentLoaded", () => {

    initializeSetupModal();
    initializeDateField();
    initializeProfileDropdown();
    initializeMenuHighlight();
    initializeEditExpenseToggle();

    renderPieChart();
    toggleSetupEditLimit();
});

// ===============================
// INITIALIZERS
// ===============================

function initializeSetupModal() {
    if (typeof setupMode !== "undefined" && setupMode === true) {
        const modal = document.getElementById("profileSetupModal");
        if (modal) modal.style.display = "flex";
    }
}

function initializeDateField() {
    const expenseDate = document.getElementById("expenseDate");
    if (!expenseDate) return;

    const today = new Date().toISOString().split("T")[0];
    expenseDate.value = today;
    expenseDate.setAttribute("min", today);
}

function initializeProfileDropdown() {
    const profileBtn = document.getElementById("profileBtn");
    const dropdown = document.getElementById("profileDropdown");
    const wrapper = document.querySelector(".profile-wrapper");

    if (!profileBtn || !dropdown) return;

    profileBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        dropdown.classList.toggle("show");
    });

    document.addEventListener("click", (e) => {
        if (!wrapper?.contains(e.target)) {
            dropdown.classList.remove("show");
        }
    });
}

function initializeMenuHighlight() {
    const menuLinks = document.querySelectorAll(".menu a");

    menuLinks.forEach(link => {
        link.addEventListener("click", function () {
            menuLinks.forEach(l => l.parentElement.classList.remove("active"));
            this.parentElement.classList.add("active");
        });
    });
}

function initializeEditExpenseToggle() {
    document.addEventListener("click", (e) => {

        const editBtn = e.target.closest(".btn-edit");
        const cancelBtn = e.target.closest(".btn-cancel");

        if (editBtn) {
            toggleExpenseView(editBtn.dataset.id, false);
        }

        if (cancelBtn) {
            toggleExpenseView(cancelBtn.dataset.id, true);
        }
    });
}

// ===============================
// EXPENSE TOGGLE
// ===============================

function toggleExpenseView(id, showViewMode) {
    const view = document.getElementById(`view-${id}`);
    const edit = document.getElementById(`edit-${id}`);

    if (!view || !edit) return;

    view.style.display = showViewMode ? "block" : "none";
    edit.style.display = showViewMode ? "none" : "block";
}

// ===============================
// CALCULATOR
// ===============================

function toggleCalculator() {
    const box = document.getElementById("calculatorBox");
    if (!box) return;

    box.style.display = box.style.display === "block" ? "none" : "block";
}

function addValue(value) {
    const input = document.getElementById("calcInput");
    if (input) input.value += value;
}

function calculate() {
    const input = document.getElementById("calcInput");
    if (!input) return;

    try {
        input.value = eval(input.value); // ⚠ OK for college project
    } catch {
        input.value = "Error";
    }
}

function clearCalc() {
    const input = document.getElementById("calcInput");
    if (input) input.value = "";
}

// ===============================
// PIE CHART
// ===============================
function renderPieChart() {

    const holder = document.getElementById("dataHolder");
    if(!holder) return;

    const categoryData = JSON.parse(holder.dataset.category);

    const labels = Object.keys(categoryData);
    const data = Object.values(categoryData);

    if(labels.length === 0) return;

    const ctx = document.getElementById("categoryChart").getContext("2d");

    const colors = labels.map(label => categoryColors[label] || "#94a3b8");

    if(pieChart) pieChart.destroy();

    pieChart = new Chart(ctx,{
        type:"pie",
        data:{
            labels:labels,
            datasets:[{
                data:data,
                backgroundColor:colors,
                borderWidth:1,
                borderColor:"#ffffff"
            }]
        },
        options:{
    responsive:true,
    maintainAspectRatio:false,
    layout:{
        padding:0
    },
    plugins:{
        legend:{
            position:"right"
        }
    }
}
    });
}

// ===============================
// MODAL SYSTEM
// ===============================

function openModal(contentHTML) {
    const modal = document.getElementById("globalModal");
    const content = document.getElementById("modalContent");

    if (!modal || !content) return;

    content.innerHTML = contentHTML;
    modal.style.display = "flex";
}

function closeModal() {
    const modal = document.getElementById("globalModal");
    if (modal) modal.style.display = "none";
}

// ===============================
// PROFILE FUNCTIONS
// ===============================

function openEditProfile() {

    if (typeof currentUser === "undefined") return;

    openModal(`
        <h2 style="margin-bottom:20px;">My Profile</h2>

        <div class="profile-grid">
            <div><strong>Name:</strong> ${currentUser.name}</div>
            <div><strong>Email:</strong> ${currentUser.email}</div>
            <div><strong>Age:</strong> ${currentUser.age || '-'}</div>
            <div><strong>Gender:</strong> ${currentUser.gender || '-'}</div>
            <div><strong>Profession:</strong> ${currentUser.profession || '-'}</div>
            <div><strong>Monthly Income:</strong> ₹${currentUser.monthly_income || 0}</div>
            <div><strong>Budget Fixed:</strong> ${currentUser.budget_fixed ? "Yes" : "No"}</div>
            <div><strong>Edit Limit:</strong> ${currentUser.budget_edit_limit || 0}</div>
        </div>

        <div style="margin-top:20px;text-align:right;">
            <button class="btn-blue" onclick="closeModal()">Close</button>
        </div>
    `);
}

function closeProfileSetup() {
    const modal = document.getElementById("profileSetupModal");
    if (modal) modal.style.display = "none";
}

function toggleSetupEditLimit() {
    const select = document.getElementById("budgetFixedSetup");
    const field = document.getElementById("setupEditLimitField");

    if (!select || !field) return;

    field.style.display = select.value === "yes" ? "none" : "block";
}

function logout() {
    if (confirm("Logout?")) {
        window.location.href = "/logout";
    }
}
const incomeData = JSON.parse(holder.dataset.income);

new Chart(document.getElementById("incomeChart"), {
    type: "bar",
    data: {
        labels: ["Income","Expense"],
        datasets: [{
            data: [incomeData.income, incomeData.expense],
            backgroundColor: ["#22c55e","#ef4444"]
        }]
    }
});
// ===============================
// DATA HOLDER (ONLY ONCE)
// ===============================
document.addEventListener("DOMContentLoaded", function(){

const holder = document.getElementById("dataHolder");

if(!holder) return;

const categoryData = JSON.parse(holder.dataset.category || "{}");

const labels = Object.keys(categoryData);
const values = Object.values(categoryData);

if(labels.length === 0) return;

const ctx = document.getElementById("monthlyChart");

if(!ctx) return;

new Chart(ctx,{
type:"pie",

data:{
labels:labels,

datasets:[{
data:values,

backgroundColor:[
"#f97316",
"#3b82f6",
"#22c55e",
"#a855f7",
"#ef4444",
"#facc15",
"#14b8a6"
]
}]
},

options:{
responsive:true,
maintainAspectRatio:false,

plugins:{
legend:{
position:"right"
}
}

}

});

});