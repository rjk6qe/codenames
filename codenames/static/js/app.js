$(document).ready(function(){

	var IO = {
		init : function(){
			console.log('init IO');
			IO.socket = io.connect(
				window.location.protocol + "//" + document.domain + ':' + location.port, 
				{ 
					'reconnection': true, 
					'reconnectionDelay': 1000, 
					'reconnectionDelayMax' : 5000, 
					'reconnectionAttempts': 5
				}
				);

			App.role = 'Player';
			App.game_role = 'Agent'
			App.team = undefined;
			App.round_started = false;


			App.teamTurn = undefined;
			localStorage.debug = '*';

			IO.bindEvents();
		},

		bindEvents : function(){
			IO.socket.on('alert room', App.alertRoom );
			IO.socket.on('alert click', App.Gameboard.alertClickOccurred );
			IO.socket.on('join room', App.Group.alertJoinRoom );
			IO.socket.on('switch turn', App.Group.alertSwitchTurn );
			IO.socket.on('round over', App.Group.alertRoundOver );
			IO.socket.on('clue submitted', App.Group.alertSetUpAgentTurn );
		},

	};

	var App = {

		init : function(){
			console.log('init app');
			App.bindElements();
			App.bindEvents();

			App.joinGroupModal.modal('show');
		},

		bindEvents : function(){
			App.gameboard_table.on('click', "td", App.onWordClick );
			App.joinGroupButton.on('click', App.Group.clickJoinGroup );
			App.createGroupButton.on('click', App.Group.clickCreateGroup );
			App.nextRoundButton.on('click', App.clickStartNewRound );
		},

		bindElements : function(){
			App.navbar = $("#navbar");
			App.snackbar = $("#snackbar");
			App.gameboard_table = $("#game_board");
			App.joinGroupModal = $("#login_modal");
			App.joinGroupButton = $("#join_button");
			App.createGroupButton = $("#create_button");
			App.userName = $("#username");
			App.groupName = $("#groupname");


			App.nextRoundSettings = $("#next_round_options");
			App.nextRoundButton = $("#start_new_round");

			App.endGameLabel = $("#end_game_beginning");
			App.winnerLabel = $("#end_game_winner");
			App.winnerModal = $("#end_game_modal");

			App.currentTurnLabel = $("#current_turn");
			App.currentClueLabel = $("#current_clue");
			App.currentTeamLabel = $("#your_team");
			App.currentRoleLabel = $("#your_role");

			App.statusLabel = $("#status");
			App.numClicksLabel = $("#clicks_remaining");
		},

		alertRoom : function(string){
			App.snackbar.html(string);
			App.snackbar.attr('class', 'show');
			setTimeout(function(){
				App.snackbar.attr('class', '');
			}, 3000);
		},

		clickStartNewRound : function(){
			if(App.role == 'Host'){
				IO.socket.emit('start new round');
			}
		},

		onWordClick : function(){
			console.log($(this).attr('clicked'));
			if($(this).attr('clicked') == 'false'){
				if(App.game_role == 'Agent'){
					if(App.round_started){
						if(App.teamTurn == App.team){
							if(App.clicksRemaining > 0){
								var selected = $(this);
								var selected_index = $(selected).attr('index');
								IO.socket.emit("click word", {'index': selected_index});
							} else{
								console.log("tried to click when no clicks were available");
							}
						} else{
							console.log('tried to click when it was not their turn')
						}
					} else{
						console.log("the round is not started'");
					}
				} else{
					console.log('tried to click when role was not right');
				}
			}
		},

		alertSetUpAgentTurn : function(json_string){
			data = JSON.parse(json_string);


			App.current_clue = data['clue'];						
			App.clicksRemaining = data['guesses'] + 1;
			App.clueSubmitted = true;

			App.currentClueLabel.text("Clue: " + App.current_clue);
			App.numClicksLabel.text("Clicks: " + App.clicksRemaining.toString());

			//set App.teamTurn to the right team
		},

		Gameboard : {

			calculate_index : function(i, j){
				return i*5 + j;
			},

			calculate_reverse_index : function(index){
				return [Math.floor(index/5), index % 5]
			},

			updateGameScore : function(data, onLoad){
				console.log('score updated, it is ' + onLoad.toString() + ' that this is an old score');
				var red_count = "#red_count";
				var blue_count = "#blue_count";
				App.navbar.find(red_count).text(data['red']);
				App.navbar.find(blue_count).text(data['blue']);

				if(onLoad){
					if(data['red'] == 0){
						App[App.role].win('red', onLoad);
					}
					if(data['blue'] == 0){
						App[App.role].win('blue', onLoad);
					}	
				}
				
			},

			convertColor : function(color){
				if(color.length > 1){
					return color;
				}
				if(color == 'R'){
					return 'red';
				}
				if(color == 'B'){
					return 'blue';
				}
				if(color == 'A'){
					return 'black';
				}
				if(color == 'C'){
					return 'green';
				}
			},


			showClickColor : function(index, c){
				var color = App.Gameboard.convertColor(c);
				console.log('showing index ' + index.toString() + ' and it has color ' + color);
				var ij = App.Gameboard.calculate_reverse_index(index);
				$(App.gameboard_table.find("tr:eq(" + ij[0].toString() + ") td:eq(" + ij[1].toString() + ")")).css('background-color', color);

			},

			setUpBoard : function(data) {
				var word_list = data['word_list'];
				var gameboard = data['key'];
				var click_map = data['click_map'];
				var starter = data['starter'];

				for(var i = 0; i < 5; i++){
					for(var j=0; j < 5; j++){

						var td = App.gameboard_table.find("tr:eq(" + i.toString() + ") td:eq(" + j.toString() + ")")
						var index = App.Gameboard.calculate_index(i,j);
						var td = $(td).attr("color", gameboard[index]).attr("clicked", click_map[index]).text(word_list[index]);


						if(click_map[index]){
							App.Gameboard.showClickColor($(td).attr('index'),$(td).attr('color'));
						}
					}
				}
			},

			alertClickOccurred : function(json_string){
				console.log(json_string);
				//expects score dict, index, color
				var data = JSON.parse(json_string);
				App.Gameboard.updateGameScore(data['score'], false);
				App.Gameboard.showClickColor(data['index'], data['color']);
			},
		},


		Group : {
			clickJoinGroup : function(){
				console.log('joining group');
				App.role = 'Player';
				IO.socket.emit(
					'join group', 
					{
						'username' : App.userName.val(), 
						'groupname': App.groupName.val(),
					});
			},

			clickCreateGroup : function(){
				console.log('creating group');
				App.role = 'Host';
				IO.socket.emit(
					'create group',{
						'username' : App.userName.val(), 
						'groupname': App.groupName.val(),
					});
			},

			clickSwitchTurn : function(){
				IO.socket.emit('switch turn');
			},

			alertJoinRoom : function(json_string){
				App.clicksRemaining = 500;

				var json_data = JSON.parse(json_string);
				console.log(json_data);

				console.log('updating score in joinRoom');
				App.Gameboard.updateGameScore(json_data['score'], true);


				App.role = json_data['role'];
				App.team = json_data['team'];
				App.teamTurn = json_data['current_turn'];

				App.Gameboard.setUpBoard(json_data['gameboard']);
				App.joinGroupModal.modal('hide');
				App[App.role].startRound();
			},

			alertSwitchTurn : function(json_string){
				var data = JSON.parse(json_string);
				App.teamTurn = data['current_turn'];

				App.currentTurnLabel.text('The ' + App.teamTurn + ' team is going right now...');
			},

			alertRoundOver : function(json_string){
				var data = JSON.parse(json_string);
				App[App.role].win(data['winner'], false);
			}

		},

		Player : {
			win : function(color, onLoad){
				console.log('as a player, the ' + color + ' team won.');
				console.log('onLoad: ' + onLoad.toString());
				//as a player, view the voting screen
				if(!onLoad){
					App.winnerLabel.text(color.charAt(0).toUpperCase() + color.substring(1, color.length) + " Team");
				} else{
					if(App.role == 'Host'){
						App.endGameLabel.text("This group ended on a won game. Would you like to restart?");
					} else{
						App.endGameLabel.text("This group ended on a won game. The host will decide to restart.");
					}
				}

				App.winnerModal.modal('show');
				
			},

			startRound : function(){
				App.currentRoleLabel.text('Your role is ' + App.role + '...');
				App.currentTeamLabel.text('Your team is ' + App.team + '...');
				App.currentTurnLabel.text('The ' + App.teamTurn + ' team is going right now...');
				App.statusLabel.text('Join room. Waiting for ' + App.teamTurn + ' to finish their turn');
				App.round_started = true; 
				
				console.log('starting round');
				//if room is ready, show game immediately

				//if room is not ready, show waiting room board
			},

		},

		Host : {
			win : function(color, onLoad){
				console.log('as a host, the ' + color + ' team won.');
				App.Player.win(color, onLoad);
			},

			startRound : function(){
				App.Player.startRound();
			},
		},
	};

	IO.init();
	App.init();

});