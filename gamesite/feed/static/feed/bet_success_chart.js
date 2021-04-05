$(document).ready(function () {
  var chartDataEndpoint = $("#bet-success-chart_container").attr("data-bet-success-url-endpoint")
  var ctx = document.getElementById('betSuccessChart').getContext('2d');

  $.ajax({
    method: "GET",
    url: chartDataEndpoint,
    success: function (data) {
      let totalEntries = data.num_correct + data.num_incorrect
      new Chart(document.getElementById("betSuccessChart"), {
        type: 'pie',
        data: {
          labels: ["Number Successful", "Number Unsuccessful"],
          datasets: [{
            label: "Entries",
            backgroundColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
            data: [data.num_correct, data.num_incorrect]
          }]
        },
        options: {
          plugins: {
            tooltip: {
              callbacks: {
                label: function(tooltipItem) {
                  return tooltipItem.label + ': ' + tooltipItem.parsed + ' of ' + totalEntries;
                },
              },
            },
        }
      }
    });
    },
    error: function (error_data) {
      console.log(error_data)
    }
  })

})