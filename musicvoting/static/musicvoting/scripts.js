var csrftoken = getCookie('csrftoken');

var spinner_small_opts = {
	length: 3.5,
	width: 2.5,
	radius: 5,
}

function vote(track_id){
	
	spinner = new Spinner();
	track_vote = document.getElementById("track-" + track_id).getElementsByClassName("track_vote")[0];
	button = track_vote.getElementsByTagName("input")[0];
	votes = track_vote.getElementsByClassName("votes")[0];
	
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
			spinner: spinner,
		},
		beforeSend: function(){
			spinner.spin();
			button.style.visibility = "hidden";
			votes.style.visibility = "hidden";
			track_vote.appendChild(spinner.el);
		},
		success: function(html){
			this.button.onclick = function() { unvote(track_id);};
			this.button.value = "Unvote";
			this.votes.innerHTML = html;
		},
		complete: function(xhr, status){
			this.button.style.visibility = "visible";
			this.votes.style.visibility = "visible";
			this.spinner.stop();
		},
	});
}

function unvote(track_id){

	spinner = new Spinner();
	track_vote = document.getElementById("track-" + track_id).getElementsByClassName("track_vote")[0];
	button = track_vote.getElementsByTagName("input")[0];
	votes = track_vote.getElementsByClassName("votes")[0];
	
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
			spinner: spinner,
		},
		beforeSend: function(){
			spinner.spin();
			button.style.visibility = "hidden";
			votes.style.visibility = "hidden";
			track_vote.appendChild(spinner.el);
		},
		success: function(html){
			this.button.onclick = function() { vote(track_id);};
			this.button.value = "Vote";
			this.votes.innerHTML = html;
		},
		complete: function(xhr, status){
			this.button.style.visibility = "visible";
			this.votes.style.visibility = "visible";
			this.spinner.stop();
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
