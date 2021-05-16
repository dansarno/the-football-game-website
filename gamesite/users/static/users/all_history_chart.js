$(document).ready(function () {
  var chartDataEndpoint = $("#all-history-chart-container").attr("data-all-history-url-endpoint")
  var prizeDataEndpoint = $("#all-history-chart-container").attr("data-prize-url-endpoint")
  var calledBetsDataEndpoint = $("#all-history-chart-container").attr("data-called-bets-url-endpoint")

  var ctx = document.getElementById('winnersChart').getContext('2d');
  var ctx2 = document.getElementById('top20Chart').getContext('2d');

  var username = $("#all-history-chart-container").attr("data-username")

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

  let calledBetsData = $.ajax({
    method: "GET",
    url: calledBetsDataEndpoint,
    success: function (data) {},
    error: function (error_data) {
      console.log(error_data)
    }
  })

  $.when(ajaxChartData, ajaxPrizeData, calledBetsData).done(function (a1, a2, a3) {
    let data = a1[0]
    prizeData = a2[0]
    let calledBetsData = a3[0]

    let positions = []
    let verboseLabels = []
    let dateLabels = []
    let entryLabels = []
    let usernames = []

    prizePositions = []
    for (let prize of prizeData) {
      prizePositions.push(prize.position)
    }

    for (let calledBet of calledBetsData) {
      verboseLabels.push(calledBet.outcome)
      dateLabels.push(calledBet.date)
    }

    for (let entry of data) {
      if (prizePositions.includes(entry.current_position)) {
        usernames.push(entry.username)
        if (entry.label) {
          entryLabels.push(`${entry.username} (${entry.label})`)
        } else {
          entryLabels.push(`${entry.username}`)
        }
        entryPostions = []
        let i = 0
        for (let position_log of entry.position_logs) {
          entryPostions.push({
            y: position_log.position,
            x: calledBetsData[i].date
          })
          i++
        }
        positions.push(entryPostions)
      }
    }

    let buttonElement = '#xaxis-toggle'
    $(".loading").hide()
    setChart(ctx, verboseLabels, dateLabels, positions, entryLabels, usernames, buttonElement)
    $(buttonElement).show()

    positions = []
    entryLabels = []
    usernames = []

    for (let entry of data) {
      if (entry.current_position <= 20) {
        usernames.push(entry.username)
        if (entry.label) {
          entryLabels.push(`${entry.username} (${entry.label})`)
        } else {
          entryLabels.push(`${entry.username}`)
        }
        entryPostions = []
        let i = 0
        for (let position_log of entry.position_logs) {
          entryPostions.push({
            y: position_log.position,
            x: calledBetsData[i].date
          })
          i++
        }
        positions.push(entryPostions)
      }
    }

    buttonElement = '#xaxis-toggle2'
    $(".loading").hide()
    setChart(ctx2, verboseLabels, dateLabels, positions, entryLabels, usernames, buttonElement)
    $(buttonElement).show()
  })

  function setChart(ctx, verboseLabels, dateLabels, positions, entryLabels, usernames, buttonElement) {

    areaColourSet = []
    prizeColours = {
      T: 'rgba(218, 165, 32, 0.5)',
      M: 'rgba(192, 192, 192, 0.5)',
      B: 'rgba(205, 127, 50, 0.5)'
    }

    positionChartData = {}
    positionChartData.dateLabels = dateLabels
    positionChartData.datasets = []

    i = 0
    for (let positionsSet of positions) {
      lineColor = "hsla(" + (360 * i / positions.length) + ",90%,70%,0.5)"
      lineColorFull = "hsla(" + (360 * i / positions.length) + ",90%,70%,1)"
      positionChartData.datasets.push({
        label: entryLabels[i],
        verboseLabel: verboseLabels,
        data: positionsSet,
        backgroundColor: (usernames[i] === username) ? lineColorFull : lineColor,
        borderColor: (usernames[i] === username) ? lineColorFull : lineColor,
        hoverBorderColor: "rgb(50,50,50)",
        pointBackgroundColor: (usernames[i] === username) ? lineColorFull : lineColor,
        pointHoverBackgroundColor: lineColorFull,
        borderWidth: (usernames[i] === username) ? 6 : 3,
        pointRadius: (usernames[i] === username) ? 3 : 0,
        pointHitRadius: 5,
        pointHoverRadius: 3,
        hoverBorderWidth: 6,
        fill: false,
        lineTension: 0.1
      })
      i++
    }

    // Position Chart
    let positionChart = new Chart(ctx, {
      type: 'line',
      data: positionChartData,
      options: {
        responsive: true,
        aspectRatio: 1.4,
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
              title: function (tooltipItem) {
                return tooltipItem[0].dataset.verboseLabel[tooltipItem[0].dataIndex]
              },
              label: function (tooltipItem) {
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
            min: 1,
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
              minUnit: 'hour',
              displayFormats: {
                hour: 'ddd ha',
                day: 'MMMM Do'
              }
            },
            ticks: {
              source: 'auto',
              minRotation: 50,
            },
            title: {
              display: true,
              labelString: 'Time (linear)'
            }
          }
        },
      }
    })

    $(buttonElement).click(function () {
      toggleDistribution(positionChart)
      toggleTickSource(positionChart)
      toggleXLabel(positionChart)
      positionChart.update()
    })

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

})