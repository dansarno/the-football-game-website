$(document).ready(function () {
  var chartDataEndpoint = $("#performance-chart_container").attr("data-entries-url-endpoint")
  var ctx = document.getElementById('performanceScoreChart').getContext('2d');
  var ctx2 = document.getElementById('performanceNumberChart').getContext('2d');

  $.ajax({
    method: "GET",
    url: chartDataEndpoint,
    success: function (data) {
      chartOptions = {
        scales: {
          r: {
            beginAtZero: true,
            min: 0,
            // max: 100,
            ticks: {
              precision: 0,
              stepSize: 20,
              callback: function (value, index, values) {
                return value + '%';
              }
            },
            gridLines: {
              circular: false
            }
          },
        },
        plugins: {
          legend: {
            position: 'bottom'
          },
        }
      }

      lineColourSet = ['rgba(236, 70, 90, 1)', 'rgba(73, 212, 198, 1)', 'rgba(255, 179, 71, 1)']
      areaColourSet = ['rgba(236, 70, 90, 0.2)', 'rgba(73, 212, 198, 0.2)', 'rgba(255, 179, 71, 0.2)']

      if (data.entries[0].performance.length < 3) {
        let txt = $("<h3></h3").text("COMING SOON");
        $("#middle-element").append(txt)
        $("#performanceScoreChart").addClass("grayout")
        $("#performanceNumberChart").addClass("grayout")

        chartData = {
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
        }
        chartOptions.animation = {
          duration: 0
        }
        chartOptions.plugins.tooltip = {
          enabled: false
        }

        scoreChartData = {
          labels: ['Group Winners', 'Top Teams', 'Tournament Totals', 'The Final', '50/50s', 'Group Matches', 'Most Goals'],
          datasets: [{
            label: 'Entry A',
            data: [40, 30, 66, 36, 18, 20, 59],
            borderWidth: 1
          }, {
            label: 'Entry B',
            data: [70, 40, 29, 50, 50, 30, 0],
            borderWidth: 1
          }]
        }

      } else {

        chartLabels = []
        for (let category of data.entries[0].performance) {
          chartLabels.push(category.game_category)
        }

        // Score Chart
        i = 0
        scoreChartDataset = []
        for (let entry of data.entries) {
          datasetLabel = ""
          datasetData = []
          if (!entry.label) {
            datasetLabel = "Your Entry";
          } else {
            datasetLabel = 'Entry ' + entry.label
          }
          for (let category of entry.performance) {
            datasetData.push(category.percentage_score)
          }
          scoreChartDataset.push({
            label: datasetLabel,
            data: datasetData,
            backgroundColor: areaColourSet[i],
            borderColor: lineColourSet[i],
            pointBackgroundColor: lineColourSet[i],
            pointHoverBackgroundColor: lineColourSet[i],
            borderWidth: 3,
            pointRadius: 2,
            pointHoverRadius: 8,
          })
          i++
        }
        scoreChartData = {
          labels: chartLabels,
          datasets: scoreChartDataset
        }
        chartOptions.plugins.tooltip = {
          mode: 'nearest',
          callbacks: {
            title: function (tooltipItem) {
              return tooltipItem[0].label
            },
            label: function (tooltipItem) {
              return tooltipItem.dataset.label + ': ' + Math.round(tooltipItem.parsed.r) + '%'
            }
          }
        }

        // Number Wins Chart
        i = 0
        chartDataset = []
        for (let entry of data.entries) {
          datasetLabel = ""
          datasetData = []
          if (!entry.label) {
            datasetLabel = "Your Entry";
          } else {
            datasetLabel = 'Entry ' + entry.label
          }
          for (let category of entry.performance) {
            datasetData.push(category.percentage_wins)
          }
          chartDataset.push({
            label: datasetLabel,
            data: datasetData,
            backgroundColor: areaColourSet[i],
            borderColor: lineColourSet[i],
            pointBackgroundColor: lineColourSet[i],
            pointHoverBackgroundColor: lineColourSet[i],
            borderWidth: 3,
            pointRadius: 2,
            pointHoverRadius: 8,
          })
          i++
        }
        chartData = {
          labels: chartLabels,
          datasets: chartDataset
        }
        chartOptions.plugins.tooltip = {
          mode: 'nearest',
          callbacks: {
            title: function (tooltipItem) {
              return tooltipItem[0].label
            },
            label: function (tooltipItem) {
              return tooltipItem.dataset.label + ': ' + Math.round(tooltipItem.parsed.r) + '%'
            }
          }
        }
      }

      chartOptions.plugins.title = {
        display: true,
        text: 'Score Performance'
      }

      new Chart(ctx, {
        type: 'radar',
        data: scoreChartData,
        options: chartOptions
      })

      chartOptions.plugins.title = {
        display: true,
        text: 'Bet Performance'
      }

      new Chart(ctx2, {
        type: 'radar',
        data: chartData,
        options: chartOptions
      })
    },
    error: function (error_data) {
      console.log(error_data)
    }
  })

})