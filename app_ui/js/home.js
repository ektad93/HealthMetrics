$(document).ready(function() {
//line graph
var options = {
    chart: {
        type: 'line'
    },
    series: [{
        name: 'sales',
        data: [30, 40, 35, 50, 49, 60, 70, 91, 125]
    }],
    xaxis: {
        categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]
    }
}

var chart = new ApexCharts(document.querySelector("#chart"), options);

chart.render();

//column bar chart
var options = {
    chart: {
        type: 'bar',
       
        toolbar: {
            show: true
        }
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '55%',
            endingShape: 'rounded'
        },
    },
    dataLabels: {
        enabled: true,
        formatter: function (val) {
            return val;
        },
        offsetY: -20,
        style: {
            fontSize: '12px',
            colors: ["#304758"]
        }
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    series: [{
        name: 'Sales',
        data: [30, 40, 45, 50, 49, 60, 70, 91, 125]
    }],
    xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
    },
    yaxis: {
        title: {
            text: 'Number of Sales'
        }
    },
    fill: {
        opacity: 1
    },
    tooltip: {
        y: {
            formatter: function (val) {
                return val + " sales"
            }
        }
    }
}

var chart = new ApexCharts(document.querySelector("#chart1"), options);

chart.render();

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
});