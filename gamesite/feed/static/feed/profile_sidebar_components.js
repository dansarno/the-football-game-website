$(document).ready(function () {
    var scoreDataEndpoint = $("#account-profile").attr("data-url-endpoint");
    jQuery.easing.def = "easeOutQuad";

    $.ajax({
        method: "GET",
        url: scoreDataEndpoint,
        success: function (data) {
            addScoreDials(data)
            addPositionCounters(data)
            addFormData(data)
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

function addFormData(data) {
    if (data.length > 0) {
        for (let entryData of data) {
            $("#form-container").append(`<div id="form-${entryData.label}" class="mt-1"></div>`)
            for (let bet of entryData.form) {
                if (bet.success === true) {
                    $(`#form-${entryData.label}`).append(
                        `<span data-toggle="tooltip" data-placement="top" title="${bet.outcome}">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-check-circle correct" viewBox="0 0 16 16">
                            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
                            <path
                                d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z" />
                            </svg>
                        </span>`
                    )
                } else {
                    $(`#form-${entryData.label}`).append(
                        `<span data-toggle="tooltip" data-placement="top" title="${bet.outcome}">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-x-circle incorrect" viewBox="0 0 16 16">
                            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
                            <path
                            d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z" />
                            </svg>
                        </span>`
                    )
                }
            }
        }
    } else if (data[0].form.length > 0) {
        $("#form-container").append(`<div class="mt-1">No bets have been called</div>`)
    } else {
        $("#form-container").append("<small>You have no entries</small>");
    }
}

function animateValue(id, start, end, duration) {
    if (start === end) return;
    var range = end - start;
    var current = start;
    var increment = end > start ? 1 : -1;
    var stepTime = Math.abs(Math.floor(duration / range));
    var obj = document.getElementById(id);
    if (end === null) {
        obj.innerHTML = "<strong>---</strong>"
        return
    } else {
        obj.innerHTML = "<strong>" + ordinal_suffix_of(start) + "</strong>"
    }
    var timer = setInterval(function () {
        current += increment;
        obj.innerHTML = "<strong>" + ordinal_suffix_of(current) + "</strong>";
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