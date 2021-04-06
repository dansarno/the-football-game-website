$(document).ready(function () {
  var winnersAndLosersDataEndpoint = $("#table_container").attr("data-url-endpoint");
  createTable('winners-leaderboard', 'biggest_winners');
  createTable('losers-leaderboard', 'biggest_losers');

  function createTable(elementID, winnersOrLosers) {
    let order = ""
    if (winnersOrLosers === 'biggest_winners') {
      order = "desc"
    } else {
      order = "asc"
    }

    $(`#${elementID}`).DataTable({
      ajax: {
        "url": winnersAndLosersDataEndpoint,
        "dataSrc": winnersOrLosers
      },
      orderClasses: false,
      responsive: {
        details: false
      },
      scrollY: "150px",
      scrollCollapse: true,
      searching: false,
      paging: false,
      info: false,
      order: [
        [3, order]
      ],
      columns: [{
          data: `entry.profile`,
          render: function (data, type, row) {

            return `<a href="/profile/${data.user.username}" class="pic-link">
                              <img class="rounded-circle account-img-sm" src="${data.profile_picture}" />
                            </a>${row.entry.label ? row.entry.label : ''}`;
          }
        },
        // {
        //   data: `entry.profile.user.username`,
        //   render: function (data, type, row, meta) {
        //     if (type === 'display' || type === 'filter') {
        //       return `<a href="/profile/${data}" class="text-dark">${data}</a>`;
        //     }
        //     return data;
        //   }
        // },
        {
          data: `previous_position`,
          render: function (data, type, row) {
            return ordinal_suffix_of(data)
          }
        },
        {
          data: `new_position`,
          render: function (data, type, row) {
            return ordinal_suffix_of(data)
          }
        },
        {
          data: `position_change`,
          render: function (data, type, row) {
            if (data > 0) {
              return `+${data}`
            } else {
              return data
            }
          }
        },
      ],
      columnDefs: [{
        targets: '_all',
        defaultContent: "-"
      }, {
        targets: '_all',
        orderable: false
      }, {
        targets: 0,
        responsivePriority: 1
      }, {
        targets: -1,
        responsivePriority: 2
      }, ],
    });
  }

  function ordinal_suffix_of(i) {
    var j = i % 10
    var k = i % 100

    if (i == null) {
      return i
    }
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

});