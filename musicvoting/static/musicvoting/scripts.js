var csrftoken = getCookie('csrftoken');

var spinner_small_opts = {
	length: 3.5,
	width: 2.5,
	radius: 5,
}

function vote(track_id){
	
	button = $('#vote_unvote_button-' + track_id);
	votes = $('#votes-' + track_id);
	
	$.ajax({
		url: "/vote/",	
		type: "POST",
		dataType: "html",
		data: {
			track_id: track_id,
		},
		headers: {
			"X-CSRFToken": csrftoken,
		},
		context: {
			button: button,
			votes: votes,
		},
		beforeSend: function(){
			button.button('loading');
		},
		success: function(html){
			this.button[0].onclick = function() { unvote(track_id);};
			this.button.button('unvote');
			this.votes.html(html);
		},
		error: function (xhr, ajaxOptions, thrownError) {
			this.button.button('vote');
		},
	});
}

function unvote(track_id){

	button = $('#vote_unvote_button-' + track_id);
	votes = $('#votes-' + track_id);
	
	$.ajax({
		url: "/unvote/",
		type: "POST",
		dataType: "html",
		data: {
			track_id: track_id,
		},
		headers: {
			"X-CSRFToken": csrftoken,
		},
		context:{
			button: button,
			votes: votes,
		},
		beforeSend: function(){
			button.button('loading')
		},
		success: function(html){
			this.button[0].onclick = function() { vote(track_id);};
			this.button.button('vote');
			this.votes.html(html);
		},
		error: function (xhr, ajaxOptions, thrownError) {
			this.button.button('unvote');
		},
	});
}

function pause(){
	
	pause_play_button = $('#pause_play_button');
	next_button = $('#next_button');
	
	$.ajax({
		url: "/pause/",
		type: "POST",
		dataType: "html",
		headers: {
			"X-CSRFToken": csrftoken,
		},
		context:{
			pause_play_button: pause_play_button,
			next_button: next_button,
		},
		beforeSend: function(){
			//Show loading
			pause_play_button.button('loading');
			next_button.button('loading');
		},
		success: function(html){
			this.pause_play_button[0].onclick = unpause;
			this.pause_play_button.button('unpause');
		},
		error: function (xhr, ajaxOptions, thrownError) {
			this.pause_play_button.button('pause');
		},
		complete: function(xhr, status){
			this.next_button.button('reset');
		},
	});
	
}

function unpause(){
	
	pause_play_button = $('#pause_play_button');
	next_button = $('#next_button');
	
	$.ajax({
		url: "/unpause/",
		type: "POST",
		dataType: "html",
		headers: {
			"X-CSRFToken": csrftoken,
		},
		context:{
			pause_play_button: pause_play_button,
			next_button: next_button,
		},
		beforeSend: function(){
			//Show loading
			pause_play_button.button('loading');
			next_button.button('loading');
		},
		success: function(html){
			this.pause_play_button[0].onclick = pause;
			this.pause_play_button.button('pause');
		},
		error: function (xhr, ajaxOptions, thrownError) {
			this.pause_play_button.button('unpause');
		},
		complete: function(hxr, status){
			this.next_button.button('reset');
		},
	});
		
}

function next(){
	
	pause_play_button = $('#pause_play_button');
	next_button = $('#next_button');
	pause_play_button_text = pause_play_button.text();

	$.ajax({
		url: "/next/",
		type: "POST",
		dataType: "html",
		headers: {
			"X-CSRFToken": csrftoken,
		},
		context:{
			pause_play_button: pause_play_button,
			next_button: next_button,
			pause_play_button_text: pause_play_button_text,
		},
		beforeSend: function(){
			//Show loading
			pause_play_button.button('loading');
			next_button.button('loading');
		},
		success: function(html){
			document.getElementById("player").outerHTML = html;
			this.pause_play_button[0].onclick = pause;
			this.pause_play_button.button('pause');
		},
		error: function (xhr, ajaxOptions, thrownError) {
			if(this.pause_play_button_text == 'Pause'){
				this.pause_play_button.button('pause');
			}
			else if(this.pause_play_button_text == 'Unpause'){
				this.pause_play_button.button('unpause');
			}
		},
		complete: function(xhr, status){
			this.next_button.button('reset');
		},
	});

}

function getCookie(cname){
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i=0; i<ca.length; i++){
		var c = ca[i];
		while (c.charAt(0) == ' '){
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0){
			return c.substring(name.length, c.length);
		}
	}
	return "";
}
