$(document).ready(function() {
  var chartDataEndpoint = $("#chart_container").attr("data-url-endpoint")
  var defaultScoreData = []
  var defaultPositionData = []
  var defaultLabels = []

  $.ajax({
    method: "GET",
    url: chartDataEndpoint,
    success: function(data) {
      let scores = []
      let positions = []
      let labels = []
      let verboseLabels = []
      let dateLabels = []
      let entryLabels = []

      i = 1
      for (let score_log of data.entries[0].score_logs) {
        labels.push(i)
        verboseLabels.push(score_log.called_bet.outcome)
        dateLabels.push(score_log.called_bet.date)
        i++
      }

      for (let entry of data.entries) {
        entryLabels.push(entry.label)

        entryScores = []
        for (let score_log of entry.score_logs) {
          entryScores.push(score_log.score)
        }
        scores.push(entryScores)

        entryPostions = []
        for (let position_log of entry.position_logs) {
          entryPostions.push(position_log.position)
        }
        positions.push(entryPostions)
      }

      defaultLabels = labels
      defaultVerboseLabels = verboseLabels
      defaultDateLabels = dateLabels
      defaultScoreData = scores
      defaultPositionData = positions
      setChart(entryLabels)
    },
    error: function(error_data) {
      console.log(error_data)
    }
  })

  function setChart(entryLabels) {
    var ctx = document.getElementById('scoreChart').getContext('2d');
    var ctx2 = document.getElementById('positionChart').getContext('2d');

    scoreChartData = {}
    scoreChartData.labels = defaultLabels
    scoreChartData.verboseLabels = defaultVerboseLabels
    scoreChartData.dateLabels = defaultDateLabels
    scoreChartData.datasets = []

    lineColourSet = ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)']
    areaColourSet = ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)']
    i = 0
    for (let scores of defaultScoreData) {
      label = ""
      if (!entryLabels[i]) {
        label = "Entry";
      } else {
        label = 'Entry ' + entryLabels[i]
      }
      scoreChartData.datasets.push({
        label: label,
        data: scores,
        backgroundColor: areaColourSet[i],
        borderColor: lineColourSet[i],
        pointBackgroundColor: lineColourSet[i],
        pointHoverBackgroundColor: lineColourSet[i],
        borderWidth: 3,
        pointRadius: 2,
        pointHoverRadius: 8,
        fill: false, //'origin',
        lineTension: 0
      })
      i++
    }

    positionChartData = {}
    positionChartData.labels = defaultLabels
    positionChartData.verboseLabels = defaultVerboseLabels
    positionChartData.dateLabels = defaultDateLabels
    positionChartData.datasets = []

    i = 0
    for (let positions of defaultPositionData) {
      label = ""
      if (!entryLabels[i]) {
        label = "Entry";
      } else {
        label = 'Entry ' + entryLabels[i]
      }
      positionChartData.datasets.push({
        label: label,
        data: positions,
        backgroundColor: areaColourSet[i],
        borderColor: lineColourSet[i],
        pointBackgroundColor: lineColourSet[i],
        pointHoverBackgroundColor: lineColourSet[i],
        borderWidth: 3,
        pointRadius: 2,
        pointHoverRadius: 8,
        fill: false,
        lineTension: 0
      })
      i++
    }

    // Score Chart
    var scoreChart = new Chart(ctx, {
      type: 'line',
      data: scoreChartData,
      options: {
        responsive: true,
        layout: {
          padding: {
            left: 0,
            right: 20,
            top: 20,
            bottom: 0
          }
        },
        tooltips: {
          mode: 'nearest',
          callbacks: {
            title: function(tooltipItem, data) {
              return data['verboseLabels'][tooltipItem[0]['index']];
            },
            label: function(tooltipItem, data) {
              return data.datasets[tooltipItem.datasetIndex].label + ': ' +
                tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            },
          },
        },
        legend: {
          position: 'bottom'
        },
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true,
              callback: function(value, index, values) {
                if (Math.max(...values) > 1500) {
                  return value / 1000 + 'k';
                } else {
                  return value;
                }
              }
            },
            scaleLabel: {
              display: true,
              labelString: 'Score'
            },
          }]
        }
      }
    });

    // Position Chart
    var positionChart = new Chart(ctx2, {
      type: 'line',
      data: positionChartData,
      options: {
        responsive: true,
        layout: {
          padding: {
            left: 0,
            right: 20,
            top: 20,
            bottom: 0
          }
        },
        tooltips: {
          mode: 'nearest',
          callbacks: {
            title: function(tooltipItem, data) {
              return data['verboseLabels'][tooltipItem[0]['index']];
            },
            label: function(tooltipItem, data) {
              return data.datasets[tooltipItem.datasetIndex].label + ': ' +
                tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            },
          },
        },
        legend: {
          position: 'bottom',
          padding: 25
        },
        scales: {
          yAxes: [{
            ticks: {
              suggestedMin: 1,
              beginAtZero: false,
              precision: 0,
              reverse: true,
            },
            scaleLabel: {
              display: true,
              labelString: 'Position'
            }
          }]
        }
      }
    });
  }
})