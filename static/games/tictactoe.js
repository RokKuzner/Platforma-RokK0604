let boardWidth = 500;
let boardHeight = 500;
let size = 100;
let raw = "XOX#X#OXO" // v taki obliki dobimo iz baze
let game = [
    ["#", "O", "#"],
    ["#", "X", "#"],
    ["O", "O", "O"]
]
let fieldWithBg = null;

let player = "X" // or O
let next_player = "..."
let player_x = "..."
let player_o = "..."

let ended

function setup() {
    createCanvas(boardWidth, boardHeight + 200);
}

function draw() {
    clear()
    drawLines()
    drawGame(game)
    drawText()
    if(fieldWithBg){
        drawBackground(fieldWithBg[0], fieldWithBg[1])
    }

    if (ended == 1) {
      drawWinner()
    }
}

function mouseMoved() {
    let [y, x] = detectPostion(mouseX, mouseY)
    fill("yellow")
    // console.log(x, y)

    if(0 <= y && y < 3 && 0 <= x && x < 3 ){
        fieldWithBg = [x, y]
    }else{
        fieldWithBg = null
    }
}

async function mouseClicked() {
     let [y, x] = detectPostion(mouseX, mouseY)
    // if polje že ima X ali O potem nič ne rišemo
    // preverimo, če smo na vrsti

    // TODO: preverimo, če še ni konec igre!

    console.log(next_player)

    await getTictactoe()
  
    if (current_user == next_player && ended == 0) {
        console.log("smo na potezi")
        
        if (game[x][y] == "#") {
            game[x][y] = player
            updateTictactoe()
        } else {
            console.log("zasedeno!")
        }
    } else {
        console.log("nismo na potezi")
    }
    
    
}

function detectPostion(x, y) {
    a = Math.floor(x / (boardWidth / 3))
    b = Math.floor(y / (boardHeight / 3))
    return [a, b] // [0, 2]
}

function drawLines() {
    strokeWeight(3) // debelina črte
    stroke(0) // barva črte 0 -> rgb(0, 0, 0)
    line(boardWidth / 3, 0, boardWidth / 3, boardHeight)
    line(2 * boardWidth / 3, 0, 2 * boardWidth / 3, boardHeight)
    line(0, boardHeight / 3, boardWidth, boardHeight / 3)
    line(0, 2 * boardHeight / 3, boardWidth, 2 * boardHeight / 3)
}

function drawX(x, y) {
    line(x - size / 2, y - size / 2, x + size / 2, y + size / 2)
    line(x - size / 2, y + size / 2, x + size / 2, y - size / 2)
}

function drawO(x, y) {
    fill("BLACK")
    ellipse(x, y, size)
}

// želimo da je input takle: [1, 2]
function drawBackground(a, b) {
// iz a in b pridimo do končega x in y
    y = a * boardWidth / 3 + boardWidth / 6
    x = b * boardHeight / 3 + boardHeight / 6
    fill("GREY")
    fill('rgba(0, 0, 0, 0.1)')
    //noStroke()
    strokeWeight(0)
    rectMode(CENTER)
    // background("WHITE")
    if (a < 3 && b < 3 && isEmptyField(a, b)) {
        rect(x, y, size * 1.4) // or square    
    }
}

function isEmptyField(a, b) { // a --> 0 or 1 or 2
    if (game[a][b] != "#") {
        return false
    } return true
} // vrne true ali false

function drawGame(game) {
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            if (game[i][j] == "X")
                drawX(j * boardWidth / 3 + boardWidth / 6, i * boardHeight / 3 + boardHeight / 6)
            else if (game[i][j] == "O")
                drawO(j * boardWidth / 3 + boardWidth / 6, i * boardHeight / 3 + boardHeight / 6)
        }
    }
}

function drawText() {
    textSize(24)
    textAlign(CENTER)
    if (ended != 1) {
      text("Igralec X: " + player_x, boardWidth / 2, boardHeight + 50)
      text("Igralec O: " + player_o, boardWidth / 2, boardHeight + 80)
      // if next player == current_player
      if (next_player == current_user) {
          text("Ti si na vrsti!", boardWidth / 2, boardHeight + 110)
      } else {
           text("Na vrsti je: " + next_player, boardWidth / 2, boardHeight + 110)   
      }
    } else {
      text("Game over!", boardWidth / 2, boardHeight + 50)
    }
    
}

function drawWinner(start, stop) {
  for (let i; i<3; i++) {
    game[i][0] == [i][1]
  }
  
  line(50, 250, 450, 250)
}


async function getTictactoe() {
    let response = await fetch("https://platforma-rokk0604.team-grace.repl.co/game/tictactoe/" + game_id + "/get")
    let data = (await response.json())
    game = data["state"]
    player_x = data["player_x"]
    player_o = data["player_o"]
    ended = data["ended"]
    if (current_user == player_x) {
        player = "X"
    } else {
        player = "O"
    }
    next_player = data["next_player"]
}

getTictactoe()

async function updateTictactoe() {
    await fetch("https://platforma-rokk0604.team-grace.repl.co/game/tictactoe/" + game_id + "/update", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"state": game})
    })
}

console.log("TEST: " + current_user)
console.log("TEST 2: " + game_id)

setInterval(async function () {
  await getTictactoe();
  console.log(ended);
}, 1000);