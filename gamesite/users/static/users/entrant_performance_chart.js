$(document).ready(function() {
  var ctx = document.getElementById('myChart').getContext('2d');
  var performanceRadar = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Group Winners', 'Top Teams', 'Tournament Totals', 'The Final', '50/50s', 'Group Matches', 'Most Goals'],
      datasets: [{
        label: 'Entry A',
        data: [45, 19, 60, 33, 12, 20, 50],
        borderWidth: 1
      }, {
        label: 'Entry B',
        data: [53, 49, 20, 53, 32, 40, 0],
        borderWidth: 1
      }]
    },
    options: {
      scale: {
        ticks: {
          suggestedMin: 0,
          beginAtZero: true,
          min: 0,
          max: 100,
          stepSize: 25
        }
      },
      animation: {
        duration: 0
      },
      tooltips: {
        enabled: false
      }
    }
  });
})