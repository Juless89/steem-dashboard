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
    $(id).addClass("nav-link active");

    id = '#' + Cookies.get('period')
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


$(document).ready(function() {
    var pathname = window.location.pathname;
    api = 'api/' + pathname.substr(1) + '/'

    $("#minute").click(function(){
        Cookies.set('chart', 'minute', { expires: 7, path: '' });
        console.log(Cookies.get('chart'));
        get_graph_data(api + Cookies.get('chart'));
        $('.btn-sm').removeClass("active")
        active_graph();
    }); 
    $("#hour").click(function(){
        Cookies.set('chart', 'hour', { expires: 7, path: '' });
        console.log(Cookies.get('chart'));
        get_graph_data(api + Cookies.get('chart'));
        $('.btn-sm').removeClass("active")
        active_graph();
    }); 
    $("#day").click(function(){
        Cookies.set('chart', 'day', { expires: 7, path: '' });
        get_graph_data(api + Cookies.get('chart'));
        $('.btn-sm').removeClass("active")
        active_graph();
    }); 

    
});