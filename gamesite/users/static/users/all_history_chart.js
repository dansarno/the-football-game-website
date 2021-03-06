$(document).ready(function() {
  var chartDataEndpoint = $("#all-history-chart-container").attr("data-all-history-url-endpoint")
  var prizeDataEndpoint = $("#all-history-chart-container").attr("data-prize-url-endpoint")
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
    for (let position_log of data[0].entries[0].position_logs) {
      labels.push(position_log.called_bet.date)
      verboseLabels.push(position_log.called_bet.outcome)
      dateLabels.push(position_log.called_bet.date)
      i++
    }

    for (let profile of data) {
      for (let entry of profile.entries) {
        if (entry.label) {
          entryLabels.push(`${profile.user} (${entry.label})`)
        } else {
          entryLabels.push(`${profile.user}`)
        }
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
    }

    defaultLabels = labels
    defaultVerboseLabels = verboseLabels
    defaultDateLabels = dateLabels
    defaultPositionData = positions

    $("#loading").hide()
    // $('#chart-card').append('<button type="button" class="btn btn-outline-dark btn-sm" id="xaxis-toggle">Toggle X Axis</button>')
    setChart(entryLabels)
    $('#xaxis-toggle').show()
  })

  function setChart(entryLabels) {
    var ctx = document.getElementById('allHistoryChart').getContext('2d');

    lineColour = 'rgba(199, 199, 199, 0.4)' // ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)']
    areaColourSet = [] // ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)']
    prizeColourSet = ['rgba(218, 165, 32, 0.2)', 'rgba(192, 192, 192, 0.2)', 'rgba(205, 127, 50, 0.2)']

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
      positionChartData.datasets.push({
        label: entryLabels[i],
        data: positions,
        backgroundColor: areaColourSet[i],
        borderColor: lineColour,
        pointBackgroundColor: lineColour,
        pointHoverBackgroundColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 3,
        pointRadius: 0,
        pointHoverRadius: 2,
        hoverBorderColor: 'rgba(255, 99, 132, 1)',
        hoverBorderWidth: 4,
        fill: false,
        lineTension: 0
      })
      i++
    }

    // Position Chart
    positionChart = new Chart(ctx, {
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
        animation: {
          onComplete: function(animation) {}
        },
        tooltips: {
          mode: 'nearest',
          intersect: true,
          callbacks: {
            title: function(tooltipItem, data) {
              return data['verboseLabels'][tooltipItem[0]['index']]
            },
            label: function(tooltipItem, data) {
              positionNumber = tooltipItem.yLabel
              return data.datasets[tooltipItem.datasetIndex].label + ': ' + ordinal_suffix_of(positionNumber)
            },
          },
        },
        hover: {
          mode: 'dataset',
          intersect: false,
        },
        legend: {
          display: false
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
              // minUnit: 'minute',
              displayFormats: {
                hour: 'ddd HH'
              }
            },
            ticks: {
              source: 'auto',
            },
            scaleLabel: {
              display: true,
              labelString: 'Time (linear)'
            }
          }]
        },
        annotation: {
          annotations: prizeHLines
        }
      }
    })

    return positionChart
  }

  function toggleDistribution(chart) {
    attr = chart.options.scales.xAxes[0].distribution
    attr = (attr == 'linear') ? 'series' : 'linear'
    chart.options.scales.xAxes[0].distribution = attr
  }

  function toggleXLabel(chart) {
    attr = chart.options.scales.xAxes[0].scaleLabel.labelString
    attr = (attr == 'Time (linear)') ? 'Time (series)' : 'Time (linear)'
    chart.options.scales.xAxes[0].scaleLabel.labelString = attr
  }

  function toggleXTickSource(chart) {
    attr = chart.options.scales.xAxes[0].ticks.source
    attr = (attr == 'label') ? 'auto' : 'label'
    chart.options.scales.xAxes[0].ticks.source = attr
  }

  function ordinal_suffix_of(i) {
    var j = i % 10
    var k = i % 100

    if (j == 1 && k != 11) {
      return i + "st"
    }
    if (j == 2 && k != 12) {
      return i + "nd"
    }
    if (j == 3 && k != 13) {
      return i + "rd"
    }
    return i + "th"
  }

  $("#xaxis-toggle").click(function() {
    toggleDistribution(positionChart)
    toggleXLabel(positionChart)
    positionChart.update()
  })

})