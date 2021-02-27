$(document).ready(function() {
  var chartDataEndpoint = $("#chart_container").attr("data-positions-url-endpoint")
  var prizeDataEndpoint = $("#chart_container").attr("data-prize-url-endpoint")
  var defaultScoreData = []
  var defaultPositionData = []
  var defaultLabels = []

  let ajaxChartData = $.ajax({
    method: "GET",
    url: chartDataEndpoint,
    success: function(data) {},
    error: function(error_data) {
      console.log(error_data)
    }
  })

  let ajaxPrizeData = $.ajax({
    method: "GET",
    url: prizeDataEndpoint,
    success: function(data) {},
    error: function(error_data) {
      console.log(error_data)
    }
  })

  $.when(ajaxChartData, ajaxPrizeData).done(function(a1, a2) {
    let data = a1[0]
    prizeData = a2[0]

    let scores = []
    let positions = []
    let labels = []
    let verboseLabels = []
    let dateLabels = []
    let entryLabels = []

    prizePositions = []
    for (let prize of prizeData) {
      prizePositions.push(prize.position)
    }

    minPosition = 1000
    maxPosition = 1

    i = 1
    for (let score_log of data.entries[0].score_logs) {
      labels.push(score_log.called_bet.date)
      verboseLabels.push(score_log.called_bet.outcome)
      dateLabels.push(score_log.called_bet.date)
      i++
    }

    for (let entry of data.entries) {
      entryLabels.push(entry.label)

      entryScores = []
      for (let score_log of entry.score_logs) {
        entryScores.push({
          y: score_log.score,
          t: score_log.called_bet.date
        })
      }
      scores.push(entryScores)

      entryPostions = []
      for (let position_log of entry.position_logs) {
        if (position_log.position > maxPosition) {
          maxPosition = position_log.position
        }
        if (position_log.position < minPosition) {
          minPosition = position_log.position
        }

        entryPostions.push({
          y: position_log.position,
          t: position_log.called_bet.date
        })
      }
      positions.push(entryPostions)
    }

    defaultLabels = labels
    defaultVerboseLabels = verboseLabels
    defaultDateLabels = dateLabels
    defaultScoreData = scores
    defaultPositionData = positions

    setChart(entryLabels)
  })

  function setChart(entryLabels) {
    var ctx = document.getElementById('scoreChartCanvas').getContext('2d');
    var ctx2 = document.getElementById('positionChartCanvas').getContext('2d');

    scoreChartData = {}
    // scoreChartData.labels = defaultLabels
    scoreChartData.verboseLabels = defaultVerboseLabels
    scoreChartData.dateLabels = defaultDateLabels
    scoreChartData.datasets = []

    lineColourSet = ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)']
    areaColourSet = ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)']
    prizeColourSet = ['rgb(218, 165, 32, 0.2)', 'rgb(192, 192, 192, 0.2)', 'rgb(205, 127, 50, 0.2)']
    i = 0
    for (let scores of defaultScoreData) {
      datasetLabel = ""
      if (!entryLabels[i]) {
        datasetLabel = "Entry";
      } else {
        datasetLabel = 'Entry ' + entryLabels[i]
      }
      scoreChartData.datasets.push({
        label: datasetLabel,
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

    let prizeHLines = []
    for (let prize of prizeData) {
      let lineColor = ''
      if (prize.band === 'T') {
        lineColor = prizeColourSet[0]
      } else if (prize.band === 'M') {
        lineColor = prizeColourSet[1]
      } else if (prize.band === 'B') {
        lineColor = prizeColourSet[2]
      }

      if (prize.position >= minPosition && prize.position <= maxPosition) {
        prizeHLines.push({
          drawTime: "beforeDatasetsDraw",
          type: "line",
          mode: "horizontal",
          scaleID: "y-axis-0",
          value: prize.position,
          borderColor: lineColor,
          borderWidth: 5
        })
      }
    }

    positionChartData = {}
    // positionChartData.labels = defaultLabels
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
    scoreChart = new Chart(ctx, {
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
          }],
          xAxes: [{
            type: 'time',
            distribution: 'linear', // 'series',
            bounds: 'ticks',
            time: {
              minUnit: 'hour',
              stepSize: 1,
              displayFormats: {
                hour: 'ddd HH'
              }
            },
            ticks: {
              source: 'auto',
            },
            scaleLabel: {
              display: true,
              labelString: 'Time'
            }
          }]
        }
      }
    });

    // Position Chart
    positionChart = new Chart(ctx2, {
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
            scaleID: "y-axis-0",
            ticks: {
              stepSize: 1,
              beginAtZero: false,
              precision: 0,
              reverse: true,
              callback: function(value, index, values) {
                if (value === 1) {
                  return '🥇 ' + value;
                } else if (value === 2) {
                  return '🥈 ' + value;
                } else if (value === 3) {
                  return '🥉 ' + value;
                } else if (prizePositions.includes(value)) {
                  return '💰 ' + value;
                } else {
                  return value;
                }
              }
            },
            scaleLabel: {
              display: true,
              labelString: 'Position'
            },
          }],
          xAxes: [{
            type: 'time',
            distribution: 'linear', // 'series',
            bounds: 'ticks',
            time: {
              minUnit: 'hour',
              stepSize: 1,
              displayFormats: {
                hour: 'ddd HH'
              }
            },
            ticks: {
              source: 'auto',
            },
            scaleLabel: {
              display: true,
              labelString: 'Time'
            }
          }]
        },
        annotation: {
          annotations: prizeHLines
        }
      }
    })

    return positionChart, scoreChart
  }

  function toggleDistribution(chart) {
    attr = chart.options.scales.xAxes[0].distribution
    attr = (attr == 'linear') ? 'series' : 'linear'
    chart.options.scales.xAxes[0].distribution = attr
  }

  function toggleXLabel(chart) {
    attr = chart.options.scales.xAxes[0].scaleLabel.labelString
    attr = (attr == 'Time') ? 'Bet' : 'Time'
    chart.options.scales.xAxes[0].scaleLabel.labelString = attr
  }

  $("#xaxis-toggle").click(function() {
    toggleDistribution(scoreChart)
    toggleXLabel(scoreChart)
    scoreChart.update()

    toggleDistribution(positionChart)
    toggleXLabel(positionChart)
    positionChart.update()
  })

})