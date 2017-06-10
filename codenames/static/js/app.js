$(document).ready(function(){

	var IO = {
		init : function(){
			console.log('init IO');
			IO.socket = io.connect(window.location.protocol + "//" + document.domain + ':' + location.port);
			App.role = 'Player';
			App.game_role = 'Agent'
			App.team = undefined;
			App.round_started = false;

			IO.bindEvents();
		},

		bindEvents : function(){
			IO.socket.on('alert room', App.alertRoom );
			IO.socket.on('alert click', App.alertClickOccurred );
			IO.socket.on('join room', App.Group.joinRoom );
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

			App.winnerLabel = $("#end_game_winner");
			App.winnerModal = $("#end_game_modal")
		},

		alertClickOccurred : function(data){
			App.Gameboard.updateGameScore(data['color'], data['team'], data['onLoad'])
			App.Gameboard.showClickColor(data['index'], data['color']);
		},

		alertRoom : function(data){
			App.snackbar.html(data);
			App.snackbar.attr('class', 'show');
			setTimeout(function(){
				App.snackbar.attr('class', '');
			}, 3000);
		},

		onWordClick : function(){
			if(App.game_role == 'Agent'){
				if(App.round_started){
					var selected = $(this);
					var selected_index = $(selected).attr('index');
					IO.socket.emit("click word", {'index': selected_index});
				} else{
					console.log("the round is not started'");
				}
			}
		},

		Gameboard : {

			setMaxScore : function(color){
				if(color == 'R'){
					$("#red_count").text("9");
					$("#blue_count").text("8");
				}
				if(color == 'B'){
					$("#blue_count").text("9");
					$("#red_count").text("8");
				}
			},

			calculate_index : function(i, j){
				return i*5 + j;
			},

			calculate_reverse_index : function(index){
				return [Math.floor(index/5), index % 5]
			},

			updateGameScore : function(color_abbr, team, onLoad){
				var color = App.Gameboard.convertColor(color_abbr);
				if(color == 'red' || color == 'blue'){
					if(color == 'red'){
						var id = "#red_count";
					}
					if(color == 'blue'){
						var id = "#blue_count";
					}	
					var count_html = App.navbar.find(id);
					var count = parseInt($(count_html).text());
					count--;
					if(count == 0){
						App[App.role].win(color);
					}
					$(count_html).text(count.toString());
				}

				if(color == 'black'){
					App[App.role].win(App.Gameboard.oppositeColor(team), onLoad);
				}
			},

			convertColor : function(color){
				var diff_color;
				switch(color) {
					case 'R':
						diff_color = 'red';
						break;
					case 'B':
						diff_color = 'blue';
						break;
					case 'C':
						diff_color = 'green';
						break;
					case 'A':
						diff_color = 'black';
						break;
				}
				return diff_color;
			},

			oppositeColor : function(color){
				if(color == 'red'){
					return 'blue';
				}
				if(color == 'blue'){
					return 'red';
				}
			},

			showClickColor : function(index, color){
				var ij = App.Gameboard.calculate_reverse_index(index);
				$(App.gameboard_table.find("tr:eq(" + ij[0].toString() + ") td:eq(" + ij[1].toString() + ")")).css('background-color', App.Gameboard.convertColor(color));

			},

			setUpBoard : function(data) {
				App.round_started = true;

				var word_list = data['word_list'];
				var gameboard = data['key'];
				var locations = data['click_map'];
				var starter = data['starter'];

				App.Gameboard.setMaxScore(starter);

				for(var i = 0; i < 5; i++){
					for(var j=0; j < 5; j++){

						var td = App.gameboard_table.find("tr:eq(" + i.toString() + ") td:eq(" + j.toString() + ")")
						var index = App.Gameboard.calculate_index(i,j);
						var td = $(td).attr("color", gameboard[index]).attr("clicked", locations[index]).text(word_list[index]);

						if(locations[index]){
							App.alertClickOccurred(
								{'index':$(td).attr('index'),
								'color': $(td).attr('color'),
								'onLoad':true,
								'team':'blue'
								}
							);
						}
					}
				}
			}
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
						'role' : App.role
					});
			},

			clickCreateGroup : function(){
				console.log('creating group');
				App.role = 'Host';
				IO.socket.emit(
					'create group', 
					{
						'username' : App.userName.val(), 
						'groupname': App.groupName.val(),
						'role' : App.role
					});
			},

			joinRoom : function(data){
				json_data = JSON.parse(data);
				console.log('joining room');
				if(data['num_players'] > 1){
					App.role = 'Player';
					console.log('you are a player');
				} else{
					App.role = 'Host';
					console.log('you are a host');
				}

				App.Gameboard.setUpBoard(json_data['gameboard']);
				App.joinGroupModal.modal('hide');
			},

		},

		Player : {
			win : function(color, onLoad){
				console.log('as a player, the ' + color + ' team won.');

				//as a player, view the voting screen
				App.winnerLabel.text(color.charAt(0).toUpperCase() + color.substring(1, color.length) + " Team");
				App.winnerModal.modal('show');
			},

			vote : function(data){
				IO.socket.emit('vote', {'vote' : 'yes'});
			}


		},

		Host : {
			win : function(color, onLoad){
				console.log('as a host, the ' + color + ' team won.');
				App.Player.win(color);

				if(onLoad){
					console.log('but, it occurred at another time');
				} else{
					IO.socket.emit('team won round', {'winner': color});
				}
			},

			startNewRound : function(){
				//in the case the group votes to start a new round, ping the server to make a new board for the current group
				console.log('starting new round');
				IO.socket.emit('start new round');
			},

			closeGroup : function(){
				console.log('closing group');
				//
			},

		},
	};

	IO.init();
	App.init();

});