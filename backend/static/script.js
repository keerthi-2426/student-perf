// Search functionality
function filterTable() {
    const input = document.getElementById("searchInput");
    const filter = input.value.toLowerCase();
    const table = document.getElementById("studentTable");
    const tr = table.getElementsByTagName("tr");

    // Start from i = 1 to skip header row
    for (let i = 1; i < tr.length; i++) {
        const td = tr[i].getElementsByTagName("td")[1]; // Name column
        if (td) {
            const txtValue = td.textContent || td.innerText;
            tr[i].style.display = txtValue.toLowerCase().includes(filter) ? "" : "none";
        }
    }
}

// Copy row to clipboard
function copyRow(button) {
    const row = button.closest("tr");
    let text = "";
    row.querySelectorAll("td").forEach(td => {
        text += td.innerText + "\t"; // Tab-separated
    });

    // Copy to clipboard
    navigator.clipboard.writeText(text.trim())
        .then(() => { 
            alert("Row copied to clipboard!"); 
        })
        .catch(err => { 
            alert("Failed to copy: " + err); 
        });
}
