$(document).ready(function() {
  var tableDataEndpoint = $("#table_container").attr("data-url-endpoint");
  createTable();

  function createTable() {
    $('#overall_leaderboard').DataTable({
      ajax: {
        "url": tableDataEndpoint,
        "dataSrc": ""
      },
      // processing: true,
      orderClasses: false,
      responsive: true,
      order: [
        [0, "asc"]
      ],
      columns: [{
          data: "current_position",
          render: function(data, type, row, meta) {
            if (type === 'display' || type === 'filter') {
              let latestPositionLog = row.position_logs[row.position_logs.length - 1];
              let previousPositionLog = row.position_logs[row.position_logs.length - 2];
              if (previousPositionLog) {
                if (latestPositionLog.position > previousPositionLog.position) {
                  return `<div>${data}</div> <div class="arrow-down"></div>`;
                } else if (latestPositionLog.position < previousPositionLog.position) {
                  return `<div class="arrow-up"></div> <div>${data}</div>`;
                } else {
                  return data;
                }
              } else {
                return data;
              }
            }
            return data;
          }
        },
        {
          data: "profile",
          render: function(data, type, row) {
            return `<a href="/profile/${data.user.username}" class="pic-link">
                              <img class="rounded-circle account-img-sm" src="${data.profile_picture}" />
                            </a>
                            ${row.label ? row.label : ''}`;
          }
        },
        {
          data: "profile.user.username",
          render: function(data, type, row, meta) {
            if (type === 'display' || type === 'filter') {
              return `<a href="/profile/${data}" class="text-dark">${data}</a>`;
            }
            return data;
          }
        },
        {
          data: "profile",
          render: function(data, type, row) {
            return `${data.user.first_name} ${data.user.last_name}`;
          }
        },
        {
          data: "form",
          render: function(data, type, row) {
            form_arr = '';
            for (let bet of data) {
              if (bet.success) {
                form_arr += `<span data-toggle="tooltip" data-placement="top" title="${bet.outcome}">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle correct" viewBox="0 0 16 16">
                          <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                          <path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/>
                        </svg>
                      </span>`;
              } else {
                form_arr += `<span data-toggle="tooltip" data-placement="top" title="${bet.outcome}">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle incorrect" viewBox="0 0 16 16">
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
          data: "profile",
          render: function(data, type, row) {
            return `${data.user.first_name} ${data.user.last_name}`;
          }
        },
        {
          data: "current_score",
          render: $.fn.dataTable.render.number(',')
        },
      ],
      columnDefs: [{
        targets: '_all',
        defaultContent: "-"
      }, {
        targets: [1, 4, 5],
        orderable: false
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
    });
  }
});