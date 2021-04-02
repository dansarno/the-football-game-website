$(document).ready(function () {
    var scoreDataEndpoint = $("#scores-container").attr("data-url-endpoint");
    jQuery.easing.def = "easeOutQuad";

    $.ajax({
        method: "GET",
        url: scoreDataEndpoint,
        success: function (data) {
            if (data.length > 0) {
                for (let entryScoreData of data) {
                    $("#scores-container").append(`<div id="score-bar-${entryScoreData.label}" class="score-bar"><strong></strong></div>`);
                    $(`#score-bar-${entryScoreData.label}`).circleProgress({
                        //size: ($('.sidebar').width() - 100) / data.length,
                        value: entryScoreData.current_score / entryScoreData.top_score,
                        startAngle: Math.PI / 2,
                        animation: {
                            duration: (entryScoreData.current_score / entryScoreData.top_score) * 3000,
                            easing: "swing"
                        }
                        //fill: {color: '#037bfc'}
                    }).on('circle-animation-progress', function (event, progress) {
                        $(this).find('strong').text(Math.round(progress * entryScoreData.current_score).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ','));
                    });
                }
            } else {
                $("#scores-container").append("<small>You have no entries</small>");
            }

        },
        error: function (error_data) {
            console.log(error_data)
        }
    })

});