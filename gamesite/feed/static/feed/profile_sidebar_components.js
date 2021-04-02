$(document).ready(function () {
    var scoreDataEndpoint = $("#account-profile").attr("data-url-endpoint");
    jQuery.easing.def = "easeOutQuad";

    $.ajax({
        method: "GET",
        url: scoreDataEndpoint,
        success: function (data) {
            addScoreDials(data)
            addPositionCounters(data)
        },
        error: function (error_data) {
            console.log(error_data)
        }
    })

});

function addScoreDials(data) {
    if (data.length > 0) {
        for (let entryData of data) {
            $("#scores-container").append(`<div id="score-bar-${entryData.label}" class="score-bar"><strong></strong></div>`);
            $(`#score-bar-${entryData.label}`).circleProgress({
                //size: ($('.sidebar').width() - 100) / data.length,
                value: entryData.current_score / entryData.top_score,
                startAngle: Math.PI / 2,
                animation: {
                    duration: (entryData.current_score / entryData.top_score) * 3000,
                    easing: "swing"
                }
                //fill: {color: '#037bfc'}
            }).on('circle-animation-progress', function (event, progress) {
                $(this).find('strong').text(Math.round(progress * entryData.current_score).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ','));
            });
        }
    } else {
        $("#scores-container").append("<small>You have no entries</small>");
    }
}

function addPositionCounters(data) {
    if (data.length > 0) {
        for (let entryData of data) {
            $("#positions-container").append(`<div id="position-${entryData.label}" class="position-counter"></div>`);
            duration = (entryData.current_score / entryData.top_score) * 3000
            animateValue(`position-${entryData.label}`, entryData.last_place, entryData.current_position, duration)
        }
    } else {
        $("#positions-container").append("<small>You have no entries</small>");
    }
}

function animateValue(id, start, end, duration) {
    if (start === end) return;
    var range = end - start;
    var current = start;
    var increment = end > start? 1 : -1;
    var stepTime = Math.abs(Math.floor(duration / range));
    var obj = document.getElementById(id);
    if (end === null) {
        obj.innerHTML = "---"
        return
    } else {
        obj.innerHTML = ordinal_suffix_of(start)
    }
    var timer = setInterval(function() {
        current += increment;
        obj.innerHTML = ordinal_suffix_of(current);
        if (current == end) {
            clearInterval(timer);
        }
    }, stepTime);
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