socket.on('connect', function() {
	console.log("connected");
});

socket.on('alert room', function(data){
	show_toast(data);
});

socket.on('notify click', function(data){
	console.log('there was a click');
	var json_data = JSON.parse(data);
	recieve_click_td(json_data['index'], json_data['team']);
});

socket.on('rejoin game', function(data){
	join_group();
	close_next_round_modal();
});

