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
          entryPostions.push({
            y: position_log.position,
            x: position_log.called_bet.date
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
    setChart(entryLabels)
    $('#xaxis-toggle').show()
  })

  function setChart(entryLabels) {
    var ctx = document.getElementById('allHistoryChart').getContext('2d');

    lineColour = 'rgba(199, 199, 199, 0.4)' // ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)']
    areaColourSet = [] // ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)']
    prizeColours = {
      T: 'rgba(218, 165, 32, 0.5)',
      M: 'rgba(192, 192, 192, 0.5)',
      B: 'rgba(205, 127, 50, 0.5)'
    }

    positionChartData = {}
    // positionChartData.labels = defaultLabels
    positionChartData.dateLabels = defaultDateLabels
    positionChartData.datasets = []

    i = 0
    for (let positions of defaultPositionData) {
      positionChartData.datasets.push({
        label: entryLabels[i],
        verboseLabel: defaultVerboseLabels[i],
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
        plugins: {
          tooltip: {
            mode: 'nearest',
            intersect: true,
            callbacks: {
              title: function(tooltipItem) {
                return tooltipItem[0].dataset.verboseLabel
              },
              label: function(tooltipItem) {
                return tooltipItem.dataset.label + ': ' + ordinal_suffix_of(tooltipItem.parsed.y)
              },
            },
          },
          legend: {
            display: false
          }
        },
        hover: {
          mode: 'dataset',
          intersect: false,
        },
        scales: {
          y: {
            scaleID: "y-axis-0",
            beginAtZero: false,
            reverse: true,
            ticks: {
              stepSize: 1,
              precision: 0,
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
              },
            },
            grid: {
              drawBorder: false,
              color: function (context) {
                for (let prize of prizeData) {
                  if (context.tick.value === prize.position) {
                    return prizeColours[prize.band]
                  }
                }
                return 'rgba(0, 0, 0, 0.1)' // default grey
              },
            },
            title: {
              display: true,
              text: 'Position'
            },
          },
          x: {
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
            title: {
              display: true,
              labelString: 'Time (linear)'
            }
          }
        },
      }
    })

    return positionChart
  }

  function toggleDistribution(chart) {
    attr = chart.options.scales.x.type
    attr = (attr == 'time') ? 'timeseries' : 'time'
    chart.options.scales.x.type = attr
  }

  function toggleTickSource(chart) {
    attr = chart.options.scales.x.ticks.source
    attr = (attr == 'auto') ? 'data' : 'auto'
    chart.options.scales.x.ticks.source = attr
  }

  function toggleXLabel(chart) {
    attr = chart.options.scales.x.title.text
    attr = (attr == 'Time (linear)') ? 'Time (series)' : 'Time (linear)'
    chart.options.scales.x.title.text = attr
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
    toggleTickSource(positionChart)
    toggleXLabel(positionChart)
    positionChart.update()
  })

})