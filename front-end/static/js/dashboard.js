// Create new chart. First remove to prevent data mutations as all charts are plotted
// to the same canvas.
function plot_graph(data){
    // canvas
    $("canvas#chart").remove();
    $("#chart_canvas").append('<canvas id="chart" width="400" height="150"></canvas>');

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
function active_buttons() {
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
    id = '#' + Cookies.get('analytics')
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
        Cookies.set('period', '1Y', { expires: 7, path: '' });
    };

    // table period
    if (Cookies.get('table_period') === undefined) {
        Cookies.set('table_period', 'month', { expires: 7, path: '' });
    };

    // analysis type
    if (Cookies.get('analytics') === undefined) {
        Cookies.set('analytics', 'author', { expires: 7, path: '' });
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
            const block_num = data.block_num[0].block_num
            const delta = data.delta
            const delta_30d = data.delta_30d
            const delta_365d = data.delta_365d
            const timestamp = data.block_num[0].timestamp
            $("#block_num").text(block_num);
            $("#delta").text(delta + '%')
            $("#delta_30d").text(delta_30d + '%');
            $("#delta_365d").text(delta_365d + '%');
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
        active_buttons()
    });
    $("#hour").click(function(){
        Cookies.set('chart', 'hour', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });
    $("#day").click(function(){
        Cookies.set('chart', 'day', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });

    // chart periods
    $("#ALL").click(function(){
        Cookies.set('period', 'ALL', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });
    $("#30D").click(function(){
        Cookies.set('period', '30D', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });
    $("#7D").click(function(){
        Cookies.set('period', '7D', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });
    $("#90D").click(function(){
        Cookies.set('period', '90D', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });
    $("#1Y").click(function(){
        Cookies.set('period', '1Y', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });
    $("#1H").click(function(){
        Cookies.set('period', '1H', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart') + '/' + Cookies.get('period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });

    // tables
    $("#table_month").click(function(){
        Cookies.set('table_period', 'month', { expires: 7, path: '' });
        get_table('api/table/votes/' + Cookies.get('analytics') + '/' + Cookies.get('table_period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });
    $("#table_week").click(function(){
        Cookies.set('table_period', 'week', { expires: 7, path: '' });
        get_table('api/table/votes/' + Cookies.get('analytics') + '/' + Cookies.get('table_period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });
    $("#table_day").click(function(){
        Cookies.set('table_period', 'day', { expires: 7, path: '' });
        get_table('api/table/votes/' + Cookies.get('analytics') + '/' + Cookies.get('table_period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });
    $("#author").click(function(){
        Cookies.set('analytics', 'author', { expires: 7, path: '' });
        get_table('api/table/votes/' + Cookies.get('analytics') + '/' + Cookies.get('table_period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });
    $("#voter").click(function(){
        Cookies.set('analytics', 'voter', { expires: 7, path: '' });
        get_table('api/table/votes/' + Cookies.get('analytics') + '/' + Cookies.get('table_period'));
        $('.btn-sm').removeClass("active")
        active_buttons()
    });
});
