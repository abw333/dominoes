var Domino = function(first, second) {
	this.first = first;
	this.second = second;

	this.image = new Image();
	this.image.src = "images/" + first + second + "b.jpg";

	this.setOrientation = function(orientation) {
      this.image.src = this.image.src.replace("b.", orientation + ".");
      this.image.src = this.image.src.replace("t.", orientation + ".");
      this.image.src = this.image.src.replace("l.", orientation + ".");
      this.image.src = this.image.src.replace("r.", orientation + ".");
	}
}

var Game = function() {
	this.max_dots = 6;
	this.num_players = 4;
	this.hands = {};
	this.chain = [];
	this.chain_center = 0;
    this.chain_left = this.max_dots;
    this.chain_right = this.max_dots;
    this.turn = 0;

	var dominos = [];
	for (var first = 0; first <= this.max_dots; first++) {
	  for (var second = first; second <= this.max_dots; second++) {
        dominos.push(new Domino(first, second))
	  }
	}

    var i = dominos.length, j, temp;
    while ( --i ) {
      j = Math.floor(Math.random() * (i + 1));
      temp = dominos[i];
      dominos[i] = dominos[j]; 
      dominos[j] = temp;
    }

    for (var player_num= 0; player_num < this.num_players; player_num++) {
      this.hands[player_num] = [];
    }

    for (var domino_i = 0; domino_i < dominos.length; domino_i++) {
      var domino = dominos[domino_i];
      var player_num = domino_i % this.num_players;
      if (domino.first == this.max_dots && domino.second == this.max_dots) {
        this.turn = (player_num + 1) % this.num_players;
        this.chain.push(domino);
      } else {
        this.hands[player_num].push(domino);
      }
    }

    for (var domino_i = 0; domino_i < this.hands[1].length; domino_i++) {
    	this.hands[1][domino_i].setOrientation("r");
    }

    for (var domino_i = 0; domino_i < this.hands[3].length; domino_i++) {
    	this.hands[3][domino_i].setOrientation("r");
    }

    this.print = function() {
    	console.log("Game:");
    	console.log("  Turn: " + this.turn);
    	console.log("  Chain Left: " + this.chain_left);
    	console.log("  Chain Center: " + this.chain_center);
    	console.log("  Chain Right: " + this.chain_right);
    	console.log("  Hands:");
    	for (var player_num = 0; player_num < this.num_players; player_num++) {
    		var hand = this.hands[player_num];
    		console.log("    Player " + player_num + ": (" + hand.length + ")");
    		for (var domino_i = 0; domino_i < hand.length; domino_i++) {
    			var domino = hand[domino_i];
    			console.log("      " + domino.first + "-" + domino.second);
    		}
    	}
    	console.log("  Chain:");
    	for (var domino_i = 0; domino_i < this.chain.length; domino_i++) {
    		var domino = this.chain[domino_i];
    		console.log("    " + domino.first + "-" + domino.second);
    	}
    }

    this.getMoves = function() {
      var moves = [];

      var hand = this.hands[this.turn];
      for (var domino_i = 0; domino_i < hand.length; domino_i++) {
        var domino = hand[domino_i];
        if (domino.first == this.chain_left || domino.second == this.chain_left) {
          moves.push({domino_i : domino_i, side : "left"});
        }
        if (domino.first == this.chain_right || domino.second == this.chain_right) {
          moves.push({domino_i : domino_i, side : "right"})
        }
      }

      return moves
    }

    this.moveIsValid = function(domino, side) {
      var side_value;
      if (side == "left") {
        side_value = this.chain_left;
      } else if (side == "right") {
        side_value = this.chain_right;
      } else {
      	// side is invalid
      	return false;
      }

      return side_value == domino.first || side_value == domino.second;
    }

    this.makeMove = function(domino_i, side) {
      if (side == "pass") {
        if (this.getMoves().length != 0) {
        	//move is invalid
        	alert("invalid move");
        	return;
        }

        this.turn = (this.turn + 1) % this.num_players;
        return;
      }

      var hand = this.hands[this.turn];
      if (domino_i >= hand.length) {
      	// move is invalid
      	alert("invalid move");
      	return;
      }

      var domino = hand[domino_i];
      if (!this.moveIsValid(domino, side)) {
      	// move is invalid
      	alert("invalid move");
      	return;
      }

      hand.splice(domino_i, 1);

      if (side == "right") {
      	this.chain.push(domino);
      	if (this.chain_right == domino.first) {
      		this.chain_right = domino.second;
      	} else {
      		this.chain_right = domino.first;
      	}
      } else {
      	this.chain.unshift(domino);
      	this.chain_center++;
      	if (this.chain_left == domino.first) {
      		this.chain_left = domino.second;
      	} else {
      		this.chain_left = domino.first;
      	}
      }

      this.turn = (this.turn + 1) % this.num_players;
      return;
    }
}