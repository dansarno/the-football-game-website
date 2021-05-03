$(document).ready(function () {
    $(".randomise-btn").on('click', function(event){
        randomiseChoices($(this).parent().attr('id'))
    })
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
    }
    }, delay);
}