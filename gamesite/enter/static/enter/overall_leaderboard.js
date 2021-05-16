$(document).ready(function () {
  var anyCalledBets = $("#overall_table_container").attr("data-any-called-bets");
  var entriesDataEndpoint = $("#overall_table_container").attr("data-entries-info-url-endpoint");
  var tableDataEndpoint = $("#overall_table_container").attr("data-url-endpoint");
  var teamsDataEndpoint = $("#overall_table_container").attr("data-teams-url-endpoint");
  var prizesDataEndpoint = $("#overall_table_container").attr("data-prizes-url-endpoint");
  let upcomingColumns = []

  let ajaxTeamData = $.ajax({
    method: "GET",
    url: teamsDataEndpoint,
    success: function (data) {},
    error: function (error_data) {
      console.log(error_data)
    }
  })

  if (anyCalledBets == "False") {
    let ajaxEntriesData = $.ajax({
      method: "GET",
      url: entriesDataEndpoint,
      success: function (data) {},
      error: function (error_data) {
        console.log(error_data)
      }
    })

    $.when(ajaxEntriesData, ajaxTeamData).done(function (a1, a2) {
      let data = a1[0]
      let teamData = a2[0]
    
      let tableColumns = [
        {
          render: function (data, type, row) {
            labelSvg = ''
            svgSize = 15
            if (row.label === "A") {
              labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" height="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M81.5,10.64A13.6,13.6,0,0,0,70.87,4.5H36.54a13.59,13.59,0,0,0-10.63,6.14L8.74,40.37a13.6,13.6,0,0,0,0,12.27L25.91,82.37A13.61,13.61,0,0,0,36.54,88.5H70.87A13.62,13.62,0,0,0,81.5,82.37L98.66,52.64a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-4.78 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M43.83,55.5,38.12,72.8H30.83l18.68-55h8.57l18.77,55H69.26L63.39,55.5Zm18-5.55L56.44,34.12c-1.22-3.59-2-6.85-2.86-10h-.16c-.81,3.26-1.71,6.61-2.77,10L45.26,50Z" transform="translate(-4.78 -2)" fill="#0d1726" stroke="#0d1726" stroke-miterlimit="10" stroke-width="4"/></svg>`
            } else if (row.label == "B") {
              labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" height="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M83.15,10.64A13.6,13.6,0,0,0,72.52,4.5H38.19a13.6,13.6,0,0,0-10.63,6.14L10.39,40.37a13.66,13.66,0,0,0,0,12.27L27.56,82.37A13.62,13.62,0,0,0,38.19,88.5H72.52a13.62,13.62,0,0,0,10.63-6.13l17.16-29.73a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-6.43 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M41,18.25a71.19,71.19,0,0,1,13.36-1.17c7.31,0,12,1.26,15.54,4.11a11.89,11.89,0,0,1,4.7,10c0,5.46-3.61,10.25-9.57,12.43v.17c5.37,1.34,11.67,5.8,11.67,14.2a15.29,15.29,0,0,1-4.78,11.34c-4,3.61-10.34,5.29-19.58,5.29A86.62,86.62,0,0,1,41,74Zm7.31,23.19h6.64c7.73,0,12.26-4,12.26-9.49,0-6.64-5-9.24-12.43-9.24a31.65,31.65,0,0,0-6.47.5Zm0,27.13a39.23,39.23,0,0,0,6.13.34C62,68.91,69,66.13,69,57.9,69,50.17,62.31,47,54.33,47h-6Z" transform="translate(-6.43 -2)" fill="#011627" stroke="#0d1726" stroke-miterlimit="10" stroke-width="3"/></svg>`
            } else if (row.label == "C") {
              labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" height="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M83.15,10.64A13.6,13.6,0,0,0,72.52,4.5H38.19a13.6,13.6,0,0,0-10.63,6.14L10.39,40.37a13.66,13.66,0,0,0,0,12.27L27.56,82.37A13.62,13.62,0,0,0,38.19,88.5H72.52a13.62,13.62,0,0,0,10.63-6.13l17.16-29.73a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-6.43 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M74.58,72.27C71.89,73.61,66.52,75,59.63,75c-16,0-28-10.07-28-28.64,0-17.72,12-29.74,29.57-29.74,7.05,0,11.5,1.52,13.44,2.52l-1.77,6a26.52,26.52,0,0,0-11.42-2.35c-13.27,0-22.09,8.48-22.09,23.35,0,13.86,8,22.76,21.75,22.76a29.24,29.24,0,0,0,11.93-2.35Z" transform="translate(-6.43 -2)" fill="#011627" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/></svg>`
            }
            return `<div class="pic-and-label ml-3"><a href="${row.view_url}" class="pic-link">
                            <img class="rounded-circle account-img-sm" src="${row.profile.profile_picture}" />
                          </a>${row.label ? labelSvg : ''}</div>`;
          }
        },
        {
          data: "profile",
          render: function (data, type, row, meta) {
            if (type === 'display' || type === 'filter') {
              return `<a href="${data.profile_url}" class="text-dark">${data.user.username}</a>`;
            }
            return data.user.username;
          }
        },
        {
          data: "profile",
          render: function (data, type, row) {
            return `${data.user.first_name} ${data.user.last_name}`;
          }
        }
      ]

      $('#all_submitted_entries_table').DataTable({
        data: data,
        orderClasses: false,
        responsive: {
          details: {
            type: 'column',
            target: 'tr'
          }
        },
        order: [
          [1, "asc"]
        ],
        columns: tableColumns, // .splice(5, 0, upcomingColumns),
        columnDefs: [{
          targets: '_all',
          defaultContent: "-"
        }, {
          targets: [0],
          orderable: false
        }, {
          targets: 0,
          responsivePriority: 1
        }, {
          targets: 1,
          responsivePriority: 2
        }, {
          targets: 2,
          responsivePriority: 2
        }, ]
      })

      for (let team of teamData) {

        teamTableColumns = tableColumns;
  
        let teamTable = $(`#team_${team.id}_leaderboard`).DataTable({
          data: data.filter(entry => entry.profile.team === team.id),
          orderClasses: false,
          responsive: {
            details: {
              type: 'column',
              target: 'tr'
            }
          },
          order: [
            [1, "asc"]
          ],
          columns: tableColumns,
          columnDefs: [{
            targets: '_all',
            defaultContent: "-"
          }, {
            targets: [0],
            orderable: false
          }, {
            targets: 0,
            responsivePriority: 1
          }, {
            targets: 1,
            responsivePriority: 2
          }, {
            targets: 2,
            responsivePriority: 2
          }, ]
        })
  
      }

    })

  } else {

    let ajaxTableData = $.ajax({
      method: "GET",
      url: tableDataEndpoint,
      success: function (data) {},
      error: function (error_data) {
        console.log(error_data)
      }
    })

    let ajaxPrizeData = $.ajax({
      method: "GET",
      url: prizesDataEndpoint,
      success: function (data) {},
      error: function (error_data) {
        console.log(error_data)
      }
    })

    $.when(ajaxTableData, ajaxTeamData, ajaxPrizeData).done(function (a1, a2, a3) {
      let data = a1[0]
      let teamData = a2[0]
      let prizeData = a3[0]

      prizePositions = []
      for (let prize of prizeData) {
        prizePositions.push(prize.position)
      }

      i = 0
      for (let upcoming of data[0].upcoming) {
        $(`<th data-toggle="tooltip" data-placement="bottom" title="Upcoming bet"><small>${upcoming.question}</small></th>`).insertBefore('.correct-bets-header')
        // $(`<th>${upcoming.question}</th>`).insertBefore('.correct-bets-footer')

        upcomingColumns.push({
          data: `upcoming.${i}`,
          width: "5%",
          orderable: false,
          className: 'dt-body-center dt-head-center text-muted',
          render: function (data, type, row) {
            return `<span data-toggle="tooltip" data-placement="top" title="${data.winning_amount} points">${data.choice}</span>`
          }
        })

        i++
      }

      let tableColumns = [{
          data: "current_position",
          render: function (data, type, row, meta) {
            if (type === 'display' || type === 'filter') {
              if (data != null) {
                let latestPositionLog = row.position_logs[row.position_logs.length - 1];
                let previousPositionLog = row.position_logs[row.position_logs.length - 2];
                let positionPrefix = ""

                if (previousPositionLog) {
                  if (data === 1) {
                    positionPrefix = '🥇 ';
                  } else if (data === 2) {
                    positionPrefix = '🥈 ';
                  } else if (data === 3) {
                    positionPrefix = '🥉 ';
                  } else if (prizePositions.includes(data)) {
                    positionPrefix = '💰 ';
                  }

                  if (latestPositionLog.position > previousPositionLog.position) {
                    return `<div>${data}${positionPrefix}</div> <div class="arrow-down"></div>`;
                  } else if (latestPositionLog.position < previousPositionLog.position) {
                    return `<div class="arrow-up"></div> <div>${data}${positionPrefix}</div>`;
                  } else {
                    return data + positionPrefix;
                  }
                } else {
                  return data;
                }
              } else {
                return "---"
              }
            }
            return data;
          }
        },
        {
          render: function (data, type, row) {
            labelSvg = ''
            svgSize = 15
            if (row.label === "A") {
              labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" height="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M81.5,10.64A13.6,13.6,0,0,0,70.87,4.5H36.54a13.59,13.59,0,0,0-10.63,6.14L8.74,40.37a13.6,13.6,0,0,0,0,12.27L25.91,82.37A13.61,13.61,0,0,0,36.54,88.5H70.87A13.62,13.62,0,0,0,81.5,82.37L98.66,52.64a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-4.78 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M43.83,55.5,38.12,72.8H30.83l18.68-55h8.57l18.77,55H69.26L63.39,55.5Zm18-5.55L56.44,34.12c-1.22-3.59-2-6.85-2.86-10h-.16c-.81,3.26-1.71,6.61-2.77,10L45.26,50Z" transform="translate(-4.78 -2)" fill="#0d1726" stroke="#0d1726" stroke-miterlimit="10" stroke-width="4"/></svg>`
            } else if (row.label == "B") {
              labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" height="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M83.15,10.64A13.6,13.6,0,0,0,72.52,4.5H38.19a13.6,13.6,0,0,0-10.63,6.14L10.39,40.37a13.66,13.66,0,0,0,0,12.27L27.56,82.37A13.62,13.62,0,0,0,38.19,88.5H72.52a13.62,13.62,0,0,0,10.63-6.13l17.16-29.73a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-6.43 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M41,18.25a71.19,71.19,0,0,1,13.36-1.17c7.31,0,12,1.26,15.54,4.11a11.89,11.89,0,0,1,4.7,10c0,5.46-3.61,10.25-9.57,12.43v.17c5.37,1.34,11.67,5.8,11.67,14.2a15.29,15.29,0,0,1-4.78,11.34c-4,3.61-10.34,5.29-19.58,5.29A86.62,86.62,0,0,1,41,74Zm7.31,23.19h6.64c7.73,0,12.26-4,12.26-9.49,0-6.64-5-9.24-12.43-9.24a31.65,31.65,0,0,0-6.47.5Zm0,27.13a39.23,39.23,0,0,0,6.13.34C62,68.91,69,66.13,69,57.9,69,50.17,62.31,47,54.33,47h-6Z" transform="translate(-6.43 -2)" fill="#011627" stroke="#0d1726" stroke-miterlimit="10" stroke-width="3"/></svg>`
            } else if (row.label == "B") {
              labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" height="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M83.15,10.64A13.6,13.6,0,0,0,72.52,4.5H38.19a13.6,13.6,0,0,0-10.63,6.14L10.39,40.37a13.66,13.66,0,0,0,0,12.27L27.56,82.37A13.62,13.62,0,0,0,38.19,88.5H72.52a13.62,13.62,0,0,0,10.63-6.13l17.16-29.73a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-6.43 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M74.58,72.27C71.89,73.61,66.52,75,59.63,75c-16,0-28-10.07-28-28.64,0-17.72,12-29.74,29.57-29.74,7.05,0,11.5,1.52,13.44,2.52l-1.77,6a26.52,26.52,0,0,0-11.42-2.35c-13.27,0-22.09,8.48-22.09,23.35,0,13.86,8,22.76,21.75,22.76a29.24,29.24,0,0,0,11.93-2.35Z" transform="translate(-6.43 -2)" fill="#011627" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/></svg>`
            }
            return `<div class="pic-and-label ml-3"><a href="${row.view_url}" class="pic-link">
                            <img class="rounded-circle account-img-sm" src="${row.profile.profile_picture}" />
                          </a>${row.label ? labelSvg : ''}</div>`;
          }
        },
        {
          data: "profile",
          render: function (data, type, row, meta) {
            if (type === 'display' || type === 'filter') {
              return `<a href="${data.profile_url}" class="table-link">${data.user.username}</a>`;
            }
            return data;
          }
        },
        {
          data: "profile",
          render: function (data, type, row) {
            return `${data.user.first_name} ${data.user.last_name}`;
          }
        },
        {
          data: "form",
          render: function (data, type, row) {
            let form_arr = '';
            if (!data.length) {
              return "---"
            } 
            for (let bet of data) {
              if (bet.success) {
                form_arr += `<span data-toggle="tooltip" data-placement="top" title="${bet.outcome}">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#27A599" class="bi bi-check-circle correct" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                        <path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/>
                      </svg>
                    </span>`;
              } else {
                form_arr += `<span data-toggle="tooltip" data-placement="top" title="${bet.outcome}">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#EA3449" class="bi bi-x-circle incorrect" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                      </svg>
                    </span>`;
              }
            }
            return form_arr;
          }
        },
        {
          data: "correct_bets",
          orderSequence: ["desc", "asc"],
          className: 'dt-body-center',
          width: "5%",
          render: function (data, type, row) {
            if (type === 'sort') {
              return data * -1;
            }
            return data;
          },
        },
        {
          data: "current_score",
          className: 'dt-body-right dt-head-center',
          render: $.fn.dataTable.render.number(',')
        },
      ]

      tableColumns.splice(5, 0, ...upcomingColumns)

      $('#overall_leaderboard').DataTable({
        data: data,
        // processing: true,
        orderClasses: false,
        responsive: {
          details: {
            type: 'column',
            target: 'tr'
          }
        },
        order: [
          [0, "asc"]
        ],
        columns: tableColumns, // .splice(5, 0, upcomingColumns),
        columnDefs: [{
          targets: '_all',
          defaultContent: "-"
        }, {
          targets: [1, 4, 5],
          orderable: false
        }, {
          targets: [0],
          orderData: [0, 6, 3]
        }, {
          targets: 0,
          className: 'column-bolded'
        }, {
          targets: 0,
          responsivePriority: 1
        }, {
          targets: 2,
          responsivePriority: 3
        }, {
          targets: -1,
          responsivePriority: 2
        }, ],
      })

      for (let team of teamData) {

        teamTableColumns = tableColumns;

        teamTableColumns[0] = {
          data: "current_team_position",
          render: function (data, type, row, meta) {
            if (type === 'display' || type === 'filter') {
              if (data != null) {
                return data;
              } else {
                return "---"
              }
            }
            return data;
          }
        }

        let teamTable = $(`#team_${team.id}_leaderboard`).DataTable({
          data: data.filter(entry => entry.profile.team === team.id),
          // processing: true,
          orderClasses: false,
          responsive: {
            details: {
              type: 'column',
              target: 'tr'
            }
          },
          order: [
            [0, "asc"]
          ],
          columns: teamTableColumns,
          columnDefs: [{
            targets: '_all',
            defaultContent: "-"
          }, {
            targets: [1, 4, 5],
            orderable: false
          }, {
            targets: [0],
            orderData: [0, 6, 3]
          }, {
            targets: 0,
            className: 'column-bolded'
          }, {
            targets: 0,
            responsivePriority: 1
          }, {
            targets: 2,
            responsivePriority: 3
          }, {
            targets: -1,
            responsivePriority: 2
          },
        ],
        })

      }

    })
  }
});