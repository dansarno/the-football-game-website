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
            labelSvg = ''
            svgSize = 15
            if (row.entry.label === "A") {
              labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M81.5,10.64A13.6,13.6,0,0,0,70.87,4.5H36.54a13.59,13.59,0,0,0-10.63,6.14L8.74,40.37a13.6,13.6,0,0,0,0,12.27L25.91,82.37A13.61,13.61,0,0,0,36.54,88.5H70.87A13.62,13.62,0,0,0,81.5,82.37L98.66,52.64a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-4.78 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M43.83,55.5,38.12,72.8H30.83l18.68-55h8.57l18.77,55H69.26L63.39,55.5Zm18-5.55L56.44,34.12c-1.22-3.59-2-6.85-2.86-10h-.16c-.81,3.26-1.71,6.61-2.77,10L45.26,50Z" transform="translate(-4.78 -2)" fill="#0d1726" stroke="#0d1726" stroke-miterlimit="10" stroke-width="4"/></svg>`
            } else if (row.entry.label == "B") {
              labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M83.15,10.64A13.6,13.6,0,0,0,72.52,4.5H38.19a13.6,13.6,0,0,0-10.63,6.14L10.39,40.37a13.66,13.66,0,0,0,0,12.27L27.56,82.37A13.62,13.62,0,0,0,38.19,88.5H72.52a13.62,13.62,0,0,0,10.63-6.13l17.16-29.73a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-6.43 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M41,18.25a71.19,71.19,0,0,1,13.36-1.17c7.31,0,12,1.26,15.54,4.11a11.89,11.89,0,0,1,4.7,10c0,5.46-3.61,10.25-9.57,12.43v.17c5.37,1.34,11.67,5.8,11.67,14.2a15.29,15.29,0,0,1-4.78,11.34c-4,3.61-10.34,5.29-19.58,5.29A86.62,86.62,0,0,1,41,74Zm7.31,23.19h6.64c7.73,0,12.26-4,12.26-9.49,0-6.64-5-9.24-12.43-9.24a31.65,31.65,0,0,0-6.47.5Zm0,27.13a39.23,39.23,0,0,0,6.13.34C62,68.91,69,66.13,69,57.9,69,50.17,62.31,47,54.33,47h-6Z" transform="translate(-6.43 -2)" fill="#011627" stroke="#0d1726" stroke-miterlimit="10" stroke-width="3"/></svg>`
            } else if (row.entry.label == "B") {
              labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M83.15,10.64A13.6,13.6,0,0,0,72.52,4.5H38.19a13.6,13.6,0,0,0-10.63,6.14L10.39,40.37a13.66,13.66,0,0,0,0,12.27L27.56,82.37A13.62,13.62,0,0,0,38.19,88.5H72.52a13.62,13.62,0,0,0,10.63-6.13l17.16-29.73a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-6.43 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M74.58,72.27C71.89,73.61,66.52,75,59.63,75c-16,0-28-10.07-28-28.64,0-17.72,12-29.74,29.57-29.74,7.05,0,11.5,1.52,13.44,2.52l-1.77,6a26.52,26.52,0,0,0-11.42-2.35c-13.27,0-22.09,8.48-22.09,23.35,0,13.86,8,22.76,21.75,22.76a29.24,29.24,0,0,0,11.93-2.35Z" transform="translate(-6.43 -2)" fill="#011627" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/></svg>`
            }
            return `<div class="pic-and-label ml-3"><a href="/profile/${data.user.username}" class="pic-link">
                          <img class="rounded-circle account-img-sm" src="${data.profile_picture}" />
                        </a>${row.entry.label ? labelSvg : ''}</div>`;
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