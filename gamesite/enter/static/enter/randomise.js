$(document).ready(function () {
    updateProgressBar();
    $(".randomise-btn").on('click', function(event){
        randomiseChoices($(this).parent().attr('id'))
    })
    $("input:radio").change(updateProgressBar)
});

function randomiseChoices(sectionID) {
    const radios = $(`#${sectionID} input[type='radio']`)
    let radioNamesSet = new Set()
    for (let radio of radios) {
        radioNamesSet.add(radio.name)
    }
    
    randomChoice(radioNamesSet, Math.floor(Math.random()*5) + 5, 50)
}

function callRandom(elName) {
    var array = document.getElementsByName(elName);
    var randomNumber=Math.floor(Math.random()*array.length);
  
    array[randomNumber].checked = true;
  }

function randomChoice(radioNamesSet, times, delay) {
    var time = 1;

    var interval = setInterval(function() { 
    if (time <= times) { 
        for (let radioName of radioNamesSet) {
            callRandom(radioName)
        }
        time++;
    }
    else { 
        clearInterval(interval);
        updateProgressBar();
    }
    }, delay);
}

function totalChoices() {
    const radios = $('input:radio')
    let radioNamesSet = new Set()
    for (let radio of radios) {
        radioNamesSet.add(radio.name)
    }
    return radioNamesSet.size
}

function updateProgressBar() {
    const total = totalChoices()
    let numChecked = $('input:radio:checked').length
    let percentage = (numChecked / total) * 100
    $('.progress-bar')[0].style.width = `${Math.floor(percentage)}%`
    $('.progress-bar')[1].style.width = `${Math.floor(percentage)}%`
    $('.progress-text').html(`Entry Progress (${numChecked} of ${total})`)
}
