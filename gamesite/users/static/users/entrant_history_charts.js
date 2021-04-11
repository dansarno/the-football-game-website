$(document).ready(function () {
  var chartDataEndpoint = $("#history-charts_container").attr("data-entries-url-endpoint")
  var prizeDataEndpoint = $("#history-charts_container").attr("data-prize-url-endpoint")
  var defaultScoreData = []
  var defaultPositionData = []
  var defaultLabels = []

  let ajaxChartData = $.ajax({
    method: "GET",
    url: chartDataEndpoint,
    success: function (data) {},
    error: function (error_data) {
      console.log(error_data)
    }
  })

  let ajaxPrizeData = $.ajax({
    method: "GET",
    url: prizeDataEndpoint,
    success: function (data) {},
    error: function (error_data) {
      console.log(error_data)
    }
  })

  $.when(ajaxChartData, ajaxPrizeData).done(function (a1, a2) {
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
          x: score_log.called_bet.date
        })
      }
      scores.push(entryScores)

      entryPostions = []
      for (let position_log of entry.position_logs) {
        entryPostions.push({
          y: position_log.position,
          x: position_log.called_bet.date
        })
      }
      positions.push(entryPostions)
    }

    defaultLabels = labels
    defaultVerboseLabels = verboseLabels
    defaultDateLabels = dateLabels
    defaultScoreData = scores
    defaultPositionData = positions

    setChart(entryLabels, data.username)
  })

  function setChart(entryLabels, username) {
    var ctx = document.getElementById('scoreChartCanvas').getContext('2d');
    var ctx2 = document.getElementById('positionChartCanvas').getContext('2d');

    scoreChartData = {}
    // scoreChartData.labels = defaultLabels
    scoreChartData.dateLabels = defaultDateLabels
    scoreChartData.datasets = []

    lineColourSet = ['rgba(236, 70, 90, 1)', 'rgba(73, 212, 198, 1)', 'rgba(255, 179, 71, 1)']
    areaColourSet = ['rgba(236, 70, 90, 0.2)', 'rgba(73, 212, 198, 0.2)', 'rgba(255, 179, 71, 0.2)']
    prizeColours = {
      T: 'rgba(218, 165, 32, 0.5)',
      M: 'rgba(192, 192, 192, 0.5)',
      B: 'rgba(205, 127, 50, 0.5)'
    }
    i = 0
    for (let scores of defaultScoreData) {
      datasetLabel = ""
      if (!entryLabels[i]) {
        datasetLabel = `${username}'s Entry`;
      } else {
        datasetLabel = 'Entry ' + entryLabels[i]
      }
      scoreChartData.datasets.push({
        label: datasetLabel,
        verboseLabel: defaultVerboseLabels,
        data: scores,
        stepped: true,
        backgroundColor: areaColourSet[i],
        borderColor: lineColourSet[i],
        pointBackgroundColor: lineColourSet[i],
        pointHoverBackgroundColor: lineColourSet[i],
        borderWidth: 3,
        pointRadius: 2,
        pointHoverRadius: 8,
        fill: false, //'origin',
      })
      i++
    }

    positionChartData = {}
    // positionChartData.labels = defaultLabels
    positionChartData.dateLabels = defaultDateLabels
    positionChartData.datasets = []

    i = 0
    for (let positions of defaultPositionData) {
      label = ""
      if (!entryLabels[i]) {
        label = `${username}'s Entry`;
      } else {
        label = 'Entry ' + entryLabels[i]
      }
      positionChartData.datasets.push({
        label: label,
        verboseLabel: defaultVerboseLabels,
        data: positions,
        // stepped: true,
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
        plugins: {
          tooltip: {
            mode: 'nearest',
            callbacks: {
              title: function (tooltipItem) {
                return tooltipItem[0].dataset.verboseLabel[tooltipItem[0].dataIndex]
              },
              label: function (tooltipItem) {
                return tooltipItem.dataset.label + ': ' +
                  tooltipItem.parsed.y.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
              },
            },
          },
          legend: {
            position: 'bottom'
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (value, index, values) {
                if (Math.max(...getValues(values)) > 1500) {
                  return value / 1000 + 'k';
                } else {
                  return value;
                }
              }
            },
            title: {
              display: true,
              text: 'Score'
            },
          },
          x: {
            type: 'time',
            distribution: 'linear', // 'series',
            bounds: 'ticks',
            time: {
              minUnit: 'minute',
              displayFormats: {
                hour: 'ddd HH'
              }
            },
            ticks: {
              source: 'auto',
            },
            title: {
              display: true,
              text: 'Time (linear)'
            }
          }
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
        plugins: {
          tooltip: {
            mode: 'nearest',
            callbacks: {
              title: function (tooltipItem) {
                return tooltipItem[0].dataset.verboseLabel[tooltipItem[0].dataIndex]
              },
              label: function (tooltipItem) {
                return tooltipItem.dataset.label + ': ' + ordinal_suffix_of(tooltipItem.parsed.y)
              },
            },
          },
          legend: {
            position: 'bottom',
            padding: 25
          },
        },
        scales: {
          y: {
            scaleID: "y-axis-0",
            beginAtZero: false,
            reverse: true,
            ticks: {
              stepSize: 1,
              precision: 0,
              callback: function (value, index, values) {
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
            title: {
              display: true,
              text: 'Position'
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
          },
          x: {
            type: 'time',
            distribution: 'linear', // 'series',
            bounds: 'ticks',
            time: {
              minUnit: 'minute',
              displayFormats: {
                hour: 'ddd HH'
              }
            },
            ticks: {
              source: 'auto',
            },
            title: {
              display: true,
              text: 'Time (linear)'
            }
          }
        },
      }
    })

    return positionChart, scoreChart
  }

  function getValues(data) {
    return data.map(d => d.value);
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

  $("#xaxis-toggle").click(function () {
    toggleDistribution(scoreChart)
    toggleTickSource(scoreChart)
    toggleXLabel(scoreChart)
    scoreChart.update()

    toggleDistribution(positionChart)
    toggleTickSource(positionChart)
    toggleXLabel(positionChart)
    positionChart.update()
  })

})