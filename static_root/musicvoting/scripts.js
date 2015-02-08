var csrftoken = getCookie('csrftoken');

function vote(track_id){
	myAjax = new XMLHttpRequest();

	myAjax.onreadystatechange=function(){
		if(myAjax.readyState==4 && myAjax.status==200){
			track_vote = document.getElementById("track-" + track_id).getElementsByClassName("track_vote")[0];
			button = track_vote.getElementsByTagName("input")[0];
			button.onclick = function() { unvote(track_id);};
			button.value = "Unvote";
			track_vote.getElementsByClassName("votes")[0].innerHTML = myAjax.responseText;
		}
	}; 
	myAjax.open("POST", "/vote/" + track_id + "/", true);
	myAjax.setRequestHeader("X-CSRFToken", csrftoken);
	myAjax.send();
}

function unvote(track_id){
	myAjax = new XMLHttpRequest();
	
	myAjax.onreadystatechange=function(){
		if(myAjax.readyState==4 && myAjax.status==200){
			track_vote = document.getElementById("track-" + track_id).getElementsByClassName("track_vote")[0];
			button = track_vote.getElementsByTagName("input")[0];
			button.onclick = function() { vote(track_id);};
			button.value = "Vote";				
			track_vote.getElementsByClassName("votes")[0].innerHTML = myAjax.responseText;
		}
	}; 
	myAjax.open("POST", "/unvote/" + track_id + "/", true);
	myAjax.setRequestHeader("X-CSRFToken", csrftoken);
	myAjax.send();
}

function pause(){
	myAjax = new XMLHttpRequest();

	myAjax.onreadystatechange=function(){
		if(myAjax.readyState==4 && myAjax.status==200){
			button = document.getElementsByName("pause_play_button")[0];
			button.onclick = unpause;
			button.value = "Unpause";
		}
	};
	myAjax.open("POST", "/pause/", true);
	myAjax.setRequestHeader("X-CSRFToken", csrftoken);
	myAjax.send();
}

function unpause(){
	myAjax = new XMLHttpRequest();

	myAjax.onreadystatechange=function(){
		if(myAjax.readyState==4 && myAjax.status==200){
			button = document.getElementsByName("pause_play_button")[0];
			button.onclick = pause;
			button.value = "Pause";
		}
	};
	myAjax.open("POST", "/unpause/", true);
	myAjax.setRequestHeader("X-CSRFToken", csrftoken);
	myAjax.send();
}

function next(){
	myAjax = new XMLHttpRequest();

	myAjax.onreadystatechange=function(){
		if(myAjax.readyState==4 && myAjax.status==200){
			document.getElementById("player").outerHTML = myAjax.responseText;
			button = document.getElementsByName("pause_play_button")[0];
			button.onclick = pause;
			button.value = "Pause";
		}
	};
	myAjax.open("POST", "/next/", true);
	myAjax.setRequestHeader("X-CSRFToken", csrftoken);
	myAjax.send();
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
