function become_spymaster(){
	is_spymaster = true;
	show_spymaster_key();
	socket.emit("user spymaster");
}

function get_group_url(join_or_create){
	var url = undefined;
	if(join_or_create == 'join'){
		console.log('joining group');
		url = '/joingroup/';
	}
	if(join_or_create == 'create'){
		console.log('creating group');
		url = '/creategroup/';
	}
	return url;
}

function group_select(join_or_create){
	var url = get_group_url(join_or_create);

	var username = $("#username").val();
	var groupname = $("#groupname").val();
	
	if(valid_username(username) && valid_groupname(groupname)){
		$.post(url, {'user':username, 'group':groupname}).done(function(data){
			var result = JSON.parse(data);
			if(result['status']){
				start_game(result['gameboard']);
				$("#login_modal").modal('hide');
				socket.emit('user login', {'user':username, 'group':groupname});
			} else{
				console.log("unable to join or create group");
			}
		});
	} else{
		console.log("invalid username");
	}
}

function start_new_round(){
	console.log('starting new round');
	socket.emit('another round');
}

function join_red_team(){
	team = 'red';
	socket.emit('join red');
}

function join_blue_team(){
	team = 'blue';
	socket.emit('join blue');
}

$(document).ready(function(){
	$("#join_button").click(function(){
		group_select('join');	
	});
	$("#create_button").click(function(){
		group_select('create');
	});
});