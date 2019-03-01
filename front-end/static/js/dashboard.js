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


$(document).ready(function() {
    var pathname = window.location.pathname;
    api = 'api/' + pathname.substr(1)

    $("#minute").click(function(){
        get_graph_data(api + '/minute');
        $('.btn-sm').removeClass("active")
        $("#minute").addClass("active");
    }); 
    $("#hour").click(function(){
        get_graph_data(api + '/hour');
        $('.btn-sm').removeClass("active")
        $("#hour").addClass("active");
    }); 
    $("#day").click(function(){
        get_graph_data(api + '/day');
        $('.btn-sm').removeClass("active")
        $("#day").addClass("active");
    }); 

    
});