function letter_to_color(letter){
	if(letter == 'R'){
		return 'red';
	} 
	if(letter == 'B'){
		return 'blue';
	} 
	if(letter == 'A'){
		return 'black';
	} 
	if(letter== 'C'){
		return 'green';
	}
}

function get_words_request(){
	return $.get("/getwords/");
}

function valid_username(username){
	console.log("valid user name");
	return true;
}

function valid_groupname(groupname){
	console.log("valid group name");
	return true;
}

function valid_word_list(word_list){
	if(word_list.length == 25){
		return true;
	}
	console.log("invalid game board");
	return false;
}

function calculate_index(i, j){
	return i*5 + j;
}

function reverse_index(index){
	return [Math.floor(index/5), index % 5]
}

function show_toast(data){
	
}