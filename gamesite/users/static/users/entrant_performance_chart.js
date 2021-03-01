$(document).ready(function() {
  var chartDataEndpoint = $("#performance-chart_container").attr("data-entries-url-endpoint")
  var ctx = document.getElementById('performanceChart').getContext('2d');

  $.ajax({
    method: "GET",
    url: chartDataEndpoint,
    success: function(data) {
      chartOptions = {
        scale: {
          ticks: {
            suggestedMin: 0,
            beginAtZero: true,
            min: 0,
            max: 100,
            stepSize: 25,
            callback: function(value, index, values) {
              return value + '%';
            },
          },
          gridLines: {
            circular: false
          }
        }
      }

      lineColourSet = ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)']
      areaColourSet = ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)']

      if (data.entries[0].performance.length < 3) {
        let txt = $("<h3></h3").text("COMING SOON");
        $("#middle-element").append(txt)
        $("#performanceChart").addClass("grayout")

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
        chartOptions.tooltips = {
          enabled: false
        }
      } else {

        chartLabels = []
        for (let category of data.entries[0].performance) {
          chartLabels.push(category.game_category)
        }

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
      }

      console.log(chartData)

      var performanceRadar = new Chart(ctx, {
        type: 'radar',
        data: chartData,
        options: chartOptions
      })
    },
    error: function(error_data) {
      console.log(error_data)
    }
  })

})