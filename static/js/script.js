
// Get HTML elements
const searchInput = document.getElementById("searchInput");
const statusFilter = document.getElementById("statusFilter");
const documentsTable = document.getElementById("documentsTable");
const noResults = document.getElementById("noResults");


// Search and filter documents
function filterDocuments() {

    if (!searchInput || !statusFilter || !documentsTable) {
        return;
    }

    const searchText = searchInput.value.toLowerCase().trim();

    const selectedStatus = statusFilter.value.toLowerCase();

    const rows = documentsTable.querySelectorAll(".document-row");

    let visibleCount = 0;

    rows.forEach(function(row) {

        const documentName = row.cells[0].textContent.toLowerCase();

        const documentStatus = row.cells[4].textContent.trim().toLowerCase();

        const matchesName = documentName.includes(searchText);

        const matchesStatus =
            selectedStatus === "" || documentStatus === selectedStatus;

        if (matchesName && matchesStatus) {

            row.style.display = "";
            visibleCount++;

        } else {

            row.style.display = "none";

        }

    });

    // Show message if no documents match
    if (noResults) {
        noResults.hidden = visibleCount !== 0;
    }

}


// Listen for search input
if (searchInput) {
    searchInput.addEventListener("input", filterDocuments);
}


// Listen for status filter
if (statusFilter) {
    statusFilter.addEventListener("change", filterDocuments);
}

