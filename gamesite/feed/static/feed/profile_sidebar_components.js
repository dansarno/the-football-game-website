$(document).ready(function () {
    var scoreDataEndpoint = $("#account-profile").attr("data-url-endpoint");
    var prizeDataEndpoint = $("#account-profile").attr("data-prize-url-endpoint");
    jQuery.easing.def = "easeOutQuad";
    
    let ajaxPrizeData = $.ajax({
        method: "GET",
        url: prizeDataEndpoint,
        success: function (data) {},
        error: function (error_data) {
          console.log(error_data)
        }
      })

    let ajaxProfileData = $.ajax({
        method: "GET",
        url: scoreDataEndpoint,
        success: function (data) {},
        error: function (error_data) {
            console.log(error_data)
        }
    })

    $.when(ajaxProfileData, ajaxPrizeData).done(function (a1, a2) {
        let data = a1[0]
        let prizeData = a2[0]

        addScoreDials(data)
        addPositionCounters(data, prizeData)
        addFormData(data)
    })

});

function addScoreDials(data) {
    if (data.length > 0) {
        for (let entryData of data) {
            $("#scores-container").append(`<div id="score-bar-${entryData.label}" class="score-bar" style="height: 90px;"><strong></strong></div>`);
            labelSvg = ''
            svgSize = 25
            if (entryData.label === "A") {
                labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M81.5,10.64A13.6,13.6,0,0,0,70.87,4.5H36.54a13.59,13.59,0,0,0-10.63,6.14L8.74,40.37a13.6,13.6,0,0,0,0,12.27L25.91,82.37A13.61,13.61,0,0,0,36.54,88.5H70.87A13.62,13.62,0,0,0,81.5,82.37L98.66,52.64a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-4.78 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M43.83,55.5,38.12,72.8H30.83l18.68-55h8.57l18.77,55H69.26L63.39,55.5Zm18-5.55L56.44,34.12c-1.22-3.59-2-6.85-2.86-10h-.16c-.81,3.26-1.71,6.61-2.77,10L45.26,50Z" transform="translate(-4.78 -2)" fill="#0d1726" stroke="#0d1726" stroke-miterlimit="10" stroke-width="4"/></svg>`
            } else if (entryData.label == "B") {
                labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M83.15,10.64A13.6,13.6,0,0,0,72.52,4.5H38.19a13.6,13.6,0,0,0-10.63,6.14L10.39,40.37a13.66,13.66,0,0,0,0,12.27L27.56,82.37A13.62,13.62,0,0,0,38.19,88.5H72.52a13.62,13.62,0,0,0,10.63-6.13l17.16-29.73a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-6.43 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M41,18.25a71.19,71.19,0,0,1,13.36-1.17c7.31,0,12,1.26,15.54,4.11a11.89,11.89,0,0,1,4.7,10c0,5.46-3.61,10.25-9.57,12.43v.17c5.37,1.34,11.67,5.8,11.67,14.2a15.29,15.29,0,0,1-4.78,11.34c-4,3.61-10.34,5.29-19.58,5.29A86.62,86.62,0,0,1,41,74Zm7.31,23.19h6.64c7.73,0,12.26-4,12.26-9.49,0-6.64-5-9.24-12.43-9.24a31.65,31.65,0,0,0-6.47.5Zm0,27.13a39.23,39.23,0,0,0,6.13.34C62,68.91,69,66.13,69,57.9,69,50.17,62.31,47,54.33,47h-6Z" transform="translate(-6.43 -2)" fill="#011627" stroke="#0d1726" stroke-miterlimit="10" stroke-width="3"/></svg>`
            } else if (entryData.label == "C") {
                labelSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgSize}px" viewBox="0 0 97.84 89.01"><path d="M83.15,10.64A13.6,13.6,0,0,0,72.52,4.5H38.19a13.6,13.6,0,0,0-10.63,6.14L10.39,40.37a13.66,13.66,0,0,0,0,12.27L27.56,82.37A13.62,13.62,0,0,0,38.19,88.5H72.52a13.62,13.62,0,0,0,10.63-6.13l17.16-29.73a13.6,13.6,0,0,0,0-12.27Z" transform="translate(-6.43 -2)" fill="none" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/><path d="M74.58,72.27C71.89,73.61,66.52,75,59.63,75c-16,0-28-10.07-28-28.64,0-17.72,12-29.74,29.57-29.74,7.05,0,11.5,1.52,13.44,2.52l-1.77,6a26.52,26.52,0,0,0-11.42-2.35c-13.27,0-22.09,8.48-22.09,23.35,0,13.86,8,22.76,21.75,22.76a29.24,29.24,0,0,0,11.93-2.35Z" transform="translate(-6.43 -2)" fill="#011627" stroke="#0d1726" stroke-miterlimit="10" stroke-width="5"/></svg>`
            }
            $(`#score-bar-${entryData.label}`).append(`<a href="${entryData.view_url}">${labelSvg}</a>`);
            let dialValue = 0
            let animationDuration = 0
            if (entryData.current_score != 0) {
                dialValue = entryData.current_score / entryData.top_score
                animationDuration = (entryData.current_score / entryData.top_score) * 4000
            } else {
                dialValue = 0.03
                animationDuration = 50
            }
            $(`#score-bar-${entryData.label}`).circleProgress({
                // size: ($('.sidebar').width() - 100) / data.length,
                size: 55,
                thickness: 5,
                value: dialValue,
                lineCap: "round",
                startAngle: Math.PI / 2,
                animation: {
                    duration: animationDuration,
                    easing: "swing"
                },
                fill: {
                    gradient: ["#CAF1EB", "#2EC4B6"]
                }
            }).on('circle-animation-progress', function (event, progress) {
                if (entryData.current_score != 0) {
                    $(this).find('strong').text(Math.round(progress * entryData.current_score).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ','));
                } else {
                    $(this).find('strong').text("0");
                }

            });
        }
    } else {
        $("#scores-container").append("<div class='sidebar-placeholder-box'><small class='test-muted'>You have no entries</small></div>");
    }
}

function addPositionCounters(data, prizeData) {
    if (data.length > 0) {
        let prizePositions = []
        for (let prize of prizeData) {
            prizePositions.push(prize.position)
        }

        for (let entryData of data) {
            if (entryData.label) {
                $("#positions-container").append(`<div class="text-muted"><a class="entry-label" href="${entryData.view_url}">Entry ${entryData.label}</a></div><div id="position-${entryData.label}" class="position-counter"></div>`);
            } else {
                $("#positions-container").append(`<div id="position-${entryData.label}" class="position-counter"></div>`);
            }
            let duration = 0
            if (entryData.current_score != 0) {
                duration = (entryData.current_score / entryData.top_score) * 4000
            } else {
                duration = 50
            }
            animateValue(`position-${entryData.label}`, entryData.last_place, entryData.current_position, duration, prizePositions)
        }
    } else {
        $("#positions-container").append("<div class='sidebar-placeholder-box'><small class='test-muted'>You have no entries</small></div>");
    }
}

function addFormData(data) {
    if (data.length > 0) {
        for (let entryData of data) {
            if (entryData.label) {
                $("#form-container").append(`<div class="mt-2"><a class="entry-label" href="${entryData.view_url}">Entry ${entryData.label}</a></div><div id="form-${entryData.label}" class="mt-1"></div>`)
            } else {
                $("#form-container").append(`<div id="form-${entryData.label}" class="mt-1"></div>`)
            }
            if (entryData.form.length > 0) {
                for (let bet of entryData.form) {
                    if (bet.success === true) {
                        $(`#form-${entryData.label}`).append(
                            `<span data-toggle="tooltip" data-placement="top" title="${bet.outcome}">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#27A599"
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
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#EA3449"
                            class="bi bi-x-circle incorrect" viewBox="0 0 16 16">
                            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
                            <path
                            d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z" />
                            </svg>
                        </span>`
                        )
                    }
                }
            } else {
                $(`#form-${entryData.label}`).append("<strong>---</strong>")
            }
        }
    // } else if (data[0].form.length > 0) {
    //     $("#form-container").append(`<div class="sidebar-placeholder-box mt-1">No bets have been called</div>`)
    } else {
        $("#form-container").append("<div class='sidebar-placeholder-box'><small class='test-muted'>You have no entries</small></div>");
    }
}

function animateValue(id, start, end, duration, prizePositions) {
    var range = end - start;
    var current = start;
    var increment = end > start ? 1 : -1;
    var stepTime = Math.abs(Math.floor(duration / range));
    var obj = document.getElementById(id);

    if (start === end && end && start) {
        obj.innerHTML = "<strong>" + ordinal_suffix_of(start) + "</strong>"
        return
    }
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
            let positionPrefix = ""

            if (current === 1) {
                positionPrefix = '🥇 ';
              } else if (current === 2) {
                positionPrefix = '🥈 ';
              } else if (current === 3) {
                positionPrefix = '🥉 ';
              } else if (prizePositions.includes(current)) {
                positionPrefix = '💰 ';
              } else {
                positionPrefix = " ";
              }
            
              obj.innerHTML = "<strong>" + ordinal_suffix_of(current) + positionPrefix + "</strong>";
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