function find_td(index){
	var ij = reverse_index(index);
	return $("#game_board").find("tr:eq(" + ij[0].toString() + ") td:eq(" + ij[1].toString() + ")");
}

function show_color(td){
	var color = letter_to_color($(td).attr('color'));
	$(td).css('background-color', color);
	return color;
}

function emit_word_click(){
	if(!is_spymaster){
		var selected = $(this);
		var selected_index = $(selected).attr('index');
		socket.emit("click", {'index': selected_index});
	}
}

function win(color){
	$("#end_game_winner").text(color.charAt(0).toUpperCase() + color.substring(1, color.length) + " Team");

	if(is_spymaster && color == team){
		$("#next_round_options").attr("style", "display:block");
	} else{
		$("#next_round_display").attr("style", "display:block");
	}

	$("#end_game_modal").modal('show');
}

function close_next_round_modal(){
	$("#end_game_modal").modal('toggle');
}

function opposite_color(color){
	if(color == 'red'){
		return 'blue';
	}
	if(color == 'blue'){
		return 'red';
	}
}

function click_color(color, team){
	if(color == 'red' || color == 'blue'){
		if(color == 'red'){
		var id = "#red_count";
		}
		if(color == 'blue'){
			var id = "#blue_count";
		}	
		var count_html = $("#navbar").find(id);
		var count = parseInt($(count_html).text());
		count--;
		if(count == 0){
			win(color);
		}
		$(count_html).text(count.toString());
	}
	
	if(color == 'black'){
		win(opposite_color(team));
	}
}


function recieve_word_click(index, team){
	var td = find_td(index);
	var color = show_color(td);
	click_color(color, team);
}

function make_words_clickable(){
	$("#game_board").unbind();
	$("#game_board").on('click', "td[name='word']", emit_word_click);
}

function set_score(color){
	if(color == 'R'){
		$("#red_count").text("9");
		$("#blue_count").text("8");
	}
	if(color == 'B'){
		$("#blue_count").text("9");
		$("#red_count").text("8");
	}
}

function convert_gameboard_to_html_table(data){
	word_list = data['word_list'];
	gameboard = data['gameboard'];
	locations = data['selected'];
	starter = data['starter'];

	set_score(starter);

	var html = $("<tbody>");
	for(var i = 0; i < 5; i++){
		var tr = $("<tr>");
		for(var j=0; j < 5; j++){
			var index = calculate_index(i,j);
			var td = $("<td>").attr("index", index.toString()).attr("name", "word").attr("color", gameboard[index]).attr("clicked", locations[index]);
			if(locations[index]){
				click_color(show_color(td));
			}
			$(td).append(word_list[index].toString());
			$(tr).append($(td));
		}
		$(html).append($(tr));
	}

	make_words_clickable();
	return $(html)[0].outerHTML;
}

function show_spymaster_key(){
	for(var i=0; i < 25; i++){
		show_color(find_td(i));
	}
}

function start_game(gameboard){
	var j_data = JSON.parse(gameboard);
	var word_list = j_data['word_list'];
	if(valid_word_list(word_list)){
		var html = convert_gameboard_to_html_table(j_data);
		$("#game_board").html(html);
	}
}

$(document).ready(function(){
	$("#login_modal").modal('show');
	$("#join_red_team").click(join_red_team);
	$("#join_blue_team").click(join_blue_team);
	$("#start_new_round").click(start_new_round);
});