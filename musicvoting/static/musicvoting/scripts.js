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
		url: urls["vote"],	
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
		url: urls["unvote"],
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
		url: urls["pause"],
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
		url: urls["unpause"],
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
		url: urls["next"],
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

function shutdown(){
	
	$.ajax({
		url: urls["shutdown"],
		type: "POST",
		dataType: "html",
		headers: {
			"X-CSRFToken": csrftoken,
		},
		beforeSend: function(){
			$('#modal-shutdown-label')[0].innerHTML = "Trying to shut down the device." ;
		},
	});
}

function import_progress(){
	$.ajax({
		url: urls["importstatus"],
		type: "GET",
		dataType: "json",
		success: function(json){
			var progress;
			var progress_text;
			if(json.number_of_files != -3){
				if(json.number_of_files == -1 || json.number_processed == 0){
					progress = 0;
					progress_text = "Counting tracks"
				}
				else if(json.number_of_files == -2){
					progress = 100;
					progress_text = "Finished. " + json.number_processed + " tracks imported.";
				}
				else{
					progress = Math.round(json.number_processed / json.number_of_files * 100);
					progress_text = json.number_processed + "/" + json.number_of_files + " tracks";
				}
				var progressbar = $('.progress-bar');
				progressbar.css('width', progress+'%').attr('aria-valuenow', progress);
				progressbar[0].innerHTML = progress_text;
				setTimeout(import_progress, 2000);
			}
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
