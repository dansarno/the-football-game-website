let balls = [];

let threshold = 30;
let accChangeX = 0;
let accChangeY = 0;
let accChangeT = 0;


function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}

function setup() {

    let clientHeight = document.getElementById('sign-up').clientHeight;
    let clientWidth = document.getElementById('sign-up').clientWidth;

    let canvas = createCanvas(clientWidth, clientHeight);  // clientHeight - 56
    canvas.position(0, 0);  // (0, 56)
    // canvas.style('z-index', '3');
    canvas.parent("sign-up");

    let colorSet = [color(231, 29, 54),
        color(255, 159, 28),
        color(46, 196, 182),
        color(1, 22, 39)
    ]

    for (let i = 0; i < 20; i++) {
        let colorSetIndex = i % colorSet.length;
        let quotient = Math.floor(i / colorSet.length)
        let ballColor = colorSet[colorSetIndex]
        balls.push(new Ball(ballColor));
    }
}

function draw() {
    background(255, 255, 255, 60);

    for (let i = 0; i < balls.length; i++) {
        balls[i].move();
        balls[i].display();
    }

    checkForShake();
}

function checkForShake() {
    // Calculate total change in accelerationX and accelerationY
    accChangeX = abs(accelerationX - pAccelerationX);
    accChangeY = abs(accelerationY - pAccelerationY);
    accChangeT = accChangeX + accChangeY;
    // If shake
    if (accChangeT >= threshold) {
        for (let i = 0; i < balls.length; i++) {
            balls[i].shake();
            balls[i].turn();
        }
    }
    // If not shake
    else {
        for (let i = 0; i < balls.length; i++) {
            balls[i].stopShake();
            balls[i].turn();
            balls[i].move();
        }
    }
}

// Ball class
class Ball {
    constructor(ballColor) {
        this.x = random(width);
        this.y = random(height);
        this.diameter = 30;
        this.angle = random(0, 6.2);
        this.speed = random(1, 3);
        this.xspeed = this.speed * cos(this.angle);
        this.yspeed = this.speed * sin(this.angle);
        this.oxspeed = this.xspeed;
        this.oyspeed = this.yspeed;
        this.xdirection = 0.7;
        this.ydirection = 0.7;
        this.c = ballColor;
    }

    move() {
        this.x += this.xspeed * this.xdirection;
        this.y += this.yspeed * this.ydirection;
    }

    // Bounce when touch the edge of the canvas
    turn() {
        if (this.x - this.diameter / 2 < 0) {
            this.x = this.diameter / 2;
            this.xdirection = -this.xdirection;

        } else if (this.y - this.diameter / 2 < 0) {
            this.y = this.diameter / 2;
            this.ydirection = -this.ydirection;

        } else if (this.x + this.diameter / 2 > width) {
            this.x = width - this.diameter / 2;
            this.xdirection = -this.xdirection;

        } else if (this.y + this.diameter / 2 > height) {
            this.y = height - this.diameter / 2;
            this.ydirection = -this.ydirection;

        }
    }

    // Add to xspeed and yspeed based on
    // the change in accelerationX value
    shake() {
        this.xspeed += random(5, accChangeX / 3);
        this.yspeed += random(5, accChangeX / 3);
    }

    // Gradually slows down
    stopShake() {
        if (this.xspeed > this.oxspeed) {
            this.xspeed -= 0.6;
        } else {
            this.xspeed = this.oxspeed;
        }
        if (this.yspeed > this.oyspeed) {
            this.yspeed -= 0.6;
        } else {
            this.yspeed = this.oyspeed;
        }
    }

    display() {
        fill(this.c);
        noStroke();
        ellipse(this.x, this.y, this.diameter, this.diameter);
    }
}