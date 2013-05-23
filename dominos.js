// This allows the Javascript code inside this block to only run when the page
// has finished loading in the browser.
$(function() {
    var canvas = document.getElementById("board");
    var ctx = canvas.getContext('2d');

    var game = new Game();

    var drawGame = function(ctx, game) {
      var spacing = 40;
	  ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "#006600";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      for (var domino_i = 0; domino_i < game.hands[0].length; domino_i++){
      	var domino = game.hands[0][domino_i];
      	domino.image.style.position = "absolute";
      	domino.image.style.top = "535px";
      	domino.image.style.left = (540 + domino_i * spacing).toString() + "px";
      	document.body.appendChild(domino.image);
      }

      for (var domino_i = 0; domino_i < game.hands[1].length; domino_i++){
      	var domino = game.hands[1][domino_i];
      	domino.image.style.position = "absolute";
      	domino.image.style.top = (150 + domino_i * spacing).toString() + "px";
      	domino.image.style.left = "110px";
      	document.body.appendChild(domino.image);
      }

      for (var domino_i = 0; domino_i < game.hands[2].length; domino_i++){
      	var domino = game.hands[2][domino_i];
      	domino.image.style.position = "absolute";
      	domino.image.style.top = "25px";
      	domino.image.style.left = (540 + domino_i * spacing).toString() + "px";
      	document.body.appendChild(domino.image);
      }

      for (var domino_i = 0; domino_i < game.hands[3].length; domino_i++){
      	var domino = game.hands[3][domino_i];
      	domino.image.style.position = "absolute";
      	domino.image.style.top = (150 + domino_i * spacing).toString() + "px";
      	domino.image.style.left = "1220px";
      	document.body.appendChild(domino.image);
      }

      var domino = game.chain[game.chain_center];
      domino.image.style.position = "absolute";
      domino.image.style.top = "250px";
   	  domino.image.style.left = "660px";
      document.body.appendChild(domino.image);

      var position = 691;
      for (var domino_i = game.chain_center + 1; domino_i < game.chain.length; domino_i++) {
      	var domino = game.chain[domino_i];
        domino.image.style.position = "absolute";
      	domino.image.style.left = position.toString() + "px";
      	if (domino.first == domino.second) {
          domino.setOrientation("b");
          domino.image.style.top = "250px";
          position += 31;
      	} else {
          if (game.directions[domino_i] == "in") {
            domino.setOrientation("l");
          } else {
            domino.setOrientation("r");
          }
          domino.image.style.top = "265px";
          position += 61;
      	}
        document.body.appendChild(domino.image);
      }

      position = 660;
      for (var domino_i = game.chain_center - 1; domino_i >= 0; domino_i--) {
      	var domino = game.chain[domino_i];
      	if (domino.first == domino.second) {
          domino.setOrientation("b");
          domino.image.style.top = "250px";
          position -= 31;
      	} else {
          domino.image.style.top = "265px";
          position -= 61;
          if (game.directions[domino_i] == "in") {
            domino.setOrientation("r");
          } else {
            domino.setOrientation("l");
          }
      	}
      	domino.image.style.left = position.toString() + "px";
        domino.image.style.position = "absolute";
        document.body.appendChild(domino.image);
      }
	}

    $("#btnAutoMove").click(function() {
      var moves = game.getMoves();
      var move;
      if (moves.length == 0) {
      	move = {domino_i : -1, side : "pass"};
      } else {
      	move = moves[Math.floor(Math.random() * moves.length)];
      }
      console.log(moves);
      console.log(move);
      game.makeMove(move.domino_i, move.side);
      drawGame(ctx, game);
      game.print();
	});

	drawGame(ctx, game);
	game.print();
});