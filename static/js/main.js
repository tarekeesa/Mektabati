// Main JavaScript functionality for Mektabati

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            if (alert.classList.contains('show')) {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);
    
    // Search form enhancements
    var searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            var query = this.querySelector('input[name="query"]').value.trim();
            if (!query) {
                e.preventDefault();
                alert('Please enter a search term');
                return false;
            }
        });
    }
    
    // Form validation enhancements
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                
                // Re-enable after 3 seconds to prevent permanent disable
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = submitBtn.innerHTML.replace('<span class="loading"></span> Processing...', 'Submit');
                }, 3000);
            }
        });
    });
    
    // Quick search functionality
    var quickSearchInput = document.querySelector('input[placeholder*="Search books"]');
    if (quickSearchInput) {
        quickSearchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                var query = this.value.trim();
                if (query) {
                    window.location.href = '/search?query=' + encodeURIComponent(query);
                }
            }
        });
    }
    
    // Data table enhancements for DataFrame view
    var dataTable = document.getElementById('dataframe-table');
    if (dataTable) {
        // Add search functionality to table
        addTableSearch(dataTable);
        
        // Make table responsive
        dataTable.classList.add('table-responsive');
    }
});

// Add search functionality to tables
function addTableSearch(table) {
    var searchContainer = document.createElement('div');
    searchContainer.className = 'mb-3';
    searchContainer.innerHTML = `
        <input type="text" class="form-control" placeholder="Search in table..." id="table-search">
    `;
    
    table.parentNode.insertBefore(searchContainer, table);
    
    var searchInput = document.getElementById('table-search');
    searchInput.addEventListener('keyup', function() {
        var filter = this.value.toLowerCase();
        var rows = table.getElementsByTagName('tr');
        
        for (var i = 1; i < rows.length; i++) { // Skip header row
            var row = rows[i];
            var cells = row.getElementsByTagName('td');
            var found = false;
            
            for (var j = 0; j < cells.length; j++) {
                if (cells[j].textContent.toLowerCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
            
            row.style.display = found ? '' : 'none';
        }
    });
}

// API helper functions
function searchBooks(query, field = 'all') {
    return fetch(`/api/search?q=${encodeURIComponent(query)}&field=${field}`)
        .then(response => response.json())
        .catch(error => {
            console.error('Search error:', error);
            return [];
        });
}

function getAllBooks() {
    return fetch('/api/books')
        .then(response => response.json())
        .catch(error => {
            console.error('API error:', error);
            return [];
        });
}

// Export functions
function exportToCSV() {
    window.location.href = '/export/csv';
}

// Utility functions
function showLoading(element) {
    element.innerHTML = '<span class="loading"></span> Loading...';
    element.disabled = true;
}

function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}