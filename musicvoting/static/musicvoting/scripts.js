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
		url: "/vote/" + track_id + "/",	
		type: "POST",
		dataType: "html",
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
		url: "/unvote/" + track_id + "/",
		type: "POST",
		dataType: "html",
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
	//myAjax = new XMLHttpRequest();
	
	spinner = new Spinner(spinner_small_opts);
	player_control = document.getElementById("player_control");
	pause_play_button = document.getElementsByName("pause_play_button")[0];
	next_button = document.getElementsByName("next_button")[0];
	
	$.ajax({
		url: "/pause/",
		type: "POST",
		dataType: "html",
		headers: {
			"X-CSRFToken": csrftoken,
		},
		context:{
			spinner: spinner,
			pause_play_button: pause_play_button,
			next_button: next_button,
		},
		beforeSend: function(){
			spinner.spin();
			pause_play_button.style.visibility = "hidden";
			next_button.style.visibility = "hidden";
			player_control.appendChild(spinner.el);
		},
		success: function(html){
			this.pause_play_button.onclick = unpause;
			this.pause_play_button.value = "Unpause";
		},
		complete: function(xhr, status){
			this.pause_play_button.style.visibility = "visible";
			this.next_button.style.visibility = "visible";
			this.spinner.stop();
		},
	});
	
	/*
	myAjax.onreadystatechange=function(){
		if(myAjax.readyState==4 && myAjax.status==200){	
			pause_play_button.onclick = unpause;
			pause_play_button.value = "Unpause";
			pause_play_button.style.visibility = "visible";
			next_button.style.visibility = "visible";
			spinner.stop();
		}
		else {
			spinner.spin();
			pause_play_button.style.visibility = "hidden";
			next_button.style.visibility = "hidden";
			player_control.appendChild(spinner.el);
		}
	};
	myAjax.open("POST", "/pause/", true);
	myAjax.setRequestHeader("X-CSRFToken", csrftoken);
	myAjax.send();
	*/
}

function unpause(){
	//myAjax = new XMLHttpRequest();
	
	spinner = new Spinner(spinner_small_opts);
	player_control = document.getElementById("player_control");
	pause_play_button = document.getElementsByName("pause_play_button")[0];
	next_button = document.getElementsByName("next_button")[0];
	
	$.ajax({
		url: "/unpause/",
		type: "POST",
		dataType: "html",
		headers: {
			"X-CSRFToken": csrftoken,
		},
		context:{
			spinner: spinner,
			pause_play_button: pause_play_button,
			next_button: next_button,
		},
		beforeSend: function(){
			spinner.spin();
			pause_play_button.style.visibility = "hidden";
			next_button.style.visibility = "hidden";
			player_control.appendChild(spinner.el);
		},
		success: function(html){
			this.pause_play_button.onclick = pause;
			this.pause_play_button.value = "Pause";
		},
		complete: function(hxr, status){
			this.pause_play_button.style.visibility = "visible";
			this.next_button.style.visibility = "visible";
			this.spinner.stop();
		},
	});
		
	/*
	myAjax.onreadystatechange=function(){
		if(myAjax.readyState==4 && myAjax.status==200){
			pause_play_button.onclick = pause;
			pause_play_button.value = "Pause";
			pause_play_button.style.visibility = "visible";
			next_button.style.visibility = "visible";
			spinner.stop();
		}
		else {
			spinner.spin();
			pause_play_button.style.visibility = "hidden";
			next_button.style.visibility = "hidden";
			player_control.appendChild(spinner.el);
		}
	};
	myAjax.open("POST", "/unpause/", true);
	myAjax.setRequestHeader("X-CSRFToken", csrftoken);
	myAjax.send();
	*/
}

function next(){
	//myAjax = new XMLHttpRequest();
	
	spinner = new Spinner(spinner_small_opts);
	player_control = document.getElementById("player_control");
	pause_play_button = document.getElementsByName("pause_play_button")[0];
	next_button = document.getElementsByName("next_button")[0];

	$.ajax({
		url: "/next/",
		type: "POST",
		dataType: "html",
		headers: {
			"X-CSRFToken": csrftoken,
		},
		context:{
			spinner: spinner,
			pause_play_button: pause_play_button,
			next_button: next_button,
		},
		beforeSend: function(){
			spinner.spin();
			pause_play_button.style.visibility = "hidden";
			next_button.style.visibility = "hidden";
			player_control.appendChild(spinner.el);
		},
		success: function(html){
			document.getElementById("player").outerHTML = html;
			this.pause_play_button.onclick = pause;
			this.pause_play_button.value = "Pause";
		},
		complete: function(xhr, status){
			this.pause_play_button.style.visibility = "visible";
			this.next_button.style.visibility = "visible";
			this.spinner.stop();
		},
	});
			
	/*	
	myAjax.onreadystatechange=function(){
		if(myAjax.readyState==4 && myAjax.status==200){
			document.getElementById("player").outerHTML = myAjax.responseText;
			pause_play_button.onclick = pause;
			pause_play_button.value = "Pause";
			pause_play_button.style.visibility = "visible";
			next_button.style.visibility = "visible";
			spinner.stop();
		}
		else {
			spinner.spin();
			pause_play_button.style.visibility = "hidden";
			next_button.style.visibility = "hidden";
			player_control.appendChild(spinner.el);
		}
	};
	myAjax.open("POST", "/next/", true);
	myAjax.setRequestHeader("X-CSRFToken", csrftoken);
	myAjax.send();
	*/
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
