// Create new chart. First remove to prevent data mutations as all charts are plotted 
// to the same canvas.
function plot_graph(data){
    // canvas
    $("canvas#chart").remove();
    $("#chart_canvas").append('<canvas id="chart" width="400" height="200"></canvas>');

    // new chart
    var ctx = document.getElementById("chart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: data.label,
                data: data.data,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255,99,132,1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
};

// Get the current settings from the user to highlight
// the corrent buttons.
function active_graph() {
    // chart resolution
    id = '#' + Cookies.get('chart')
    $(id).addClass("active");

    // chart period
    id = '#' + Cookies.get('period')
    $(id).addClass("active");

    // table period
    id = '#table_' + Cookies.get('table_period')
    $(id).addClass("active");

    // analysis type
    id = '#' + Cookies.get('analyses')
    $(id).addClass("active");

    // current operation type
    var pathname = window.location.pathname;
    id = '#' + pathname.substr(1)
    $(id).addClass("nav-link active");

};

// retrieve chart data from api
function get_graph_data(endpoint) {
    $.ajax({
        method: "GET",
        url: endpoint,

        // plot chart on success
        success: function(data){
            plot_graph(data);
        },
        error: function(error_data){
            console.log(error_data)
        }
    });  
};

// fill table
function fill_table(data) {
    const rankingsBody = document.querySelector("#table1 > tbody");

    // clear table
    while (rankingsBody.firstChild){
        rankingsBody.removeChild(rankingsBody.firstChild);
    }

    // parse data to json
    let array = JSON.parse(data.data);

    // create each row
    array.forEach(row => {
        const tr = document.createElement("tr");

        let x = 0
        row.forEach((cell) => {
            const td = document.createElement("td");
            // Add a link and @ for steem user accounts
            if (x == 1) {
                const a = document.createElement("a");
                a.textContent = '@' + cell;
                a.target = "_blank"
                a.href = 'https://www.steemit.com/@' + cell
                td.appendChild(a);
            }
            else {
                td.textContent = cell;
            }
            tr.appendChild(td);
            x += 1
        });

        rankingsBody.appendChild(tr);
    });
}

// get table data from api
function get_table(endpoint) {
    $.ajax({
        method: "GET",
        url: endpoint,

        // on success fill table
        success: function(data){
            fill_table(data[0]);
        },
        error: function(error_data){
            console.log(error_data)
        }
    });  
};

// Check for cookies if none set preset cookies.
function set_cookies(){
    // chart resolution
    if (Cookies.get('chart') === undefined) {
        Cookies.set('chart', 'day', { expires: 7, path: '' });
    };

    // chart period
    if (Cookies.get('period') === undefined) {
        Cookies.set('period', 'ALL', { expires: 7, path: '' });
    };

    // table period
    if (Cookies.get('table_period') === undefined) {
        Cookies.set('table_period', 'month', { expires: 7, path: '' });
    };

    // analysis type
    if (Cookies.get('analyses') === undefined) {
        Cookies.set('analyses', 'author', { expires: 7, path: '' });
    };
};

// Periodically update main stats 
function update_stats() {
    var endpoint = '/api/stats' + window.location.pathname;

    $.ajax({
        method: "GET",
        url: endpoint,
        success: function(data){
            // extract data and set to selected fields
            $("#operations").text(data.operations);
            block_num = data.block_num[0].block_num
            timestamp = data.block_num[0].timestamp
            $("#block_num").text(block_num);
        },
        error: function(error_data){
            console.log(error_data)
        }
    });  
};

// Update stats every 2.5s
$(document).ready(function() {
    update_stats();
    setInterval("update_stats();",2500);
});

// All button interactions for dynamic charts and tables:
// Set new cookie
// plot new chart/table
// remove current active buttons
// apply new active button
$(document).ready(function() {
    var pathname = window.location.pathname;
    api = 'api/' + pathname.substr(1) + '/'

    // chart resolutions
    $("#minute").click(function(){
        Cookies.set('chart', 'minute', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    }); 
    $("#hour").click(function(){
        Cookies.set('chart', 'hour', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    }); 
    $("#day").click(function(){
        Cookies.set('chart', 'day', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    });

    // chart periods
    $("#ALL").click(function(){
        Cookies.set('period', 'ALL', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    }); 
    $("#30D").click(function(){
        Cookies.set('period', '30D', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    }); 
    $("#7D").click(function(){
        Cookies.set('period', '7D', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    }); 
    $("#24H").click(function(){
        Cookies.set('period', '24H', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    });
    $("#12H").click(function(){
        Cookies.set('period', '12H', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    });
    $("#1H").click(function(){
        Cookies.set('period', '1H', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    }); 

    // tables
    $("#table_month").click(function(){
        Cookies.set('table_period', 'month', { expires: 7, path: '' });
        get_table('api/table/votes/' + Cookies.get('analyses') + '/' + Cookies.get('table_period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    });
    $("#table_week").click(function(){
        Cookies.set('table_period', 'week', { expires: 7, path: '' });
        get_table('api/table/votes/' + Cookies.get('analyses') + '/' + Cookies.get('table_period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    });
    $("#table_day").click(function(){
        Cookies.set('table_period', 'day', { expires: 7, path: '' });
        get_table('api/table/votes/' + Cookies.get('analyses') + '/' + Cookies.get('table_period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    });
    $("#author").click(function(){
        Cookies.set('analyses', 'author', { expires: 7, path: '' });
        get_table('api/table/votes/' + Cookies.get('analyses') + '/' + Cookies.get('table_period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    });
    $("#voter").click(function(){
        Cookies.set('analyses', 'voter', { expires: 7, path: '' });
        get_table('api/table/votes/' + Cookies.get('analyses') + '/' + Cookies.get('table_period'));
        $('.btn-sm').removeClass("active")
        active_graph()
    });
});