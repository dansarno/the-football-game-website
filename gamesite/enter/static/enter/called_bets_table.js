$(document).ready(function () {
  var calledBetsEndpoint = $("#called_bets_table_container").attr("data-url-called-bets-endpoint");

  let ajaxTeamData = $.ajax({
    method: "GET",
    url: calledBetsEndpoint,
    success: function (data) {

      let tableColumns = [
        {
          data: 'question',
        },{
          className: 'dt-body-center',
          render: function ( data, type, row, meta ) {
            return `<a href="${row.post_url}" class="table-link">${row.choice}</a>`
          }
        },
        {
          data: "category",
          className: 'dt-body-center',
        },
        {
          data: "winning_amount",
          className: 'dt-body-center',
        },
        {
          data: "date",
          type: 'datetime-moment',
          // order: 'asc',
          className: 'dt-body-right dt-head-center',
          render: function ( data, type, row ) {
            if (type === 'display' || type === 'filter') {
              return (moment(data).format('HH:mm MMM Do'));
            }
            return data;
          }
        }
      ]

      $('#called_bets_table').DataTable({
        data: data,
        orderClasses: false,
        responsive: {
          details: {
            type: 'column',
            target: 'tr'
          }
        },
        order: [
          [4, "desc"]
        ],
        columns: tableColumns,
        columnDefs: [{
          targets: '_all',
          defaultContent: "-"
        }, {
          targets: [0, 1],
          orderable: false
        }, {
          targets: 0,
          responsivePriority: 1
        }, {
          targets: 1,
          responsivePriority: 2
        }, 
      ]
      })

    },
    error: function (error_data) {
      console.log(error_data)
    }
  })

});