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
		},

		alertClickOccurred : function(data){
			App.Gameboard.updateGameScore(data['color'])
			App.Gameboard.showClickColor(data['index'], data['color']);
		},

		alertRoom : function(data){
			console.log('alert room');
			App.snackbar.html(data);
			App.snackbar.attr('class', 'show');
			setTimeout(function(){
				App.snackbar.attr('class', '');
			}, 3000);
		},

		onWordClick : function(){
			console.log('clicking word');
			if(App.game_role == 'Agent'){
				var selected = $(this);
				var selected_index = $(selected).attr('index');
				IO.socket.emit("click word", {'index': selected_index});
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

			updateGameScore : function(color_abbr){
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
						// win(color);
						console.log('win');
					}
					$(count_html).text(count.toString());
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

			showClickColor : function(index, color){
				var ij = App.Gameboard.calculate_reverse_index(index);
				console.log(App.Gameboard.convertColor(color));
				$(App.gameboard_table.find("tr:eq(" + ij[0].toString() + ") td:eq(" + ij[1].toString() + ")")).css('background-color', App.Gameboard.convertColor(color));

			},

			setUpBoard : function(data) {
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
								'color': $(td).attr('color')
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
				if(data['num_players'] > 0){
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
			
		},

		Host : {
			
		},
	};

	IO.init();
	App.init();

});