
//filter
   function applyFilters() {
    var nameFilter = document.getElementById('nameFilter').value;
    var dateFilter = document.getElementById('dateFilter').value;

    // Make AJAX request to your API with the filter values
    $.ajax({
        url: 'your_api_endpoint_here',
        type: 'POST',
        data: {
            name: nameFilter,
            date: dateFilter
        },
        success: function(response) {
            // Handle the response and update the data grid
            displayFilteredData(response);
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

function displayFilteredData(data) {
    var dataBody = document.getElementById('dataBody');
    dataBody.innerHTML = ''; // Clear existing data

    // Parse the response and add rows to the data grid
    data.forEach(function(item) {
        var row = '<tr><td>' + item.name + '</td><td>' + item.date + '</td></tr>';
        // Add more cells as needed
        dataBody.innerHTML += row;
    });

    // Show the data grid
    document.getElementById('dataGrid').style.display = 'block';
}
