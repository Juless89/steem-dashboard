function plot_graph(data){
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

function active_graph() {
    id = '#' + Cookies.get('chart')
    $(id).addClass("active");

    id = '#' + Cookies.get('period')
    $(id).addClass("active");

    var pathname = window.location.pathname;
    id = '#' + pathname.substr(1)
    $(id).addClass("nav-link active");

};

function get_graph_data(endpoint) {
    $.ajax({
        method: "GET",
        url: endpoint,
        success: function(data){
            console.log(data);
            plot_graph(data);
        },
        error: function(error_data){
            console.log(error_data)
        }
    });  
};

function get_table(endpoint) {
    $.ajax({
        method: "GET",
        url: endpoint,
        success: function(data){
            console.log(data);
        },
        error: function(error_data){
            console.log(error_data)
        }
    });  
};

function set_cookies(){
    if (Cookies.get('chart') === undefined) {
        Cookies.set('chart', 'day', { expires: 7, path: '' });
    };
    if (Cookies.get('period') === undefined) {
        Cookies.set('period', '30D', { expires: 7, path: '' });
    };
};

$(document).ready(function() {
    var pathname = window.location.pathname;
    api = 'api/' + pathname.substr(1) + '/'

    // Resolutions
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

    // Periods
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

    
});