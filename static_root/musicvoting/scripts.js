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
	myAjax.open("GET", "/vote/" + track_id + "/", true);
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
	myAjax.open("GET", "/unvote/" + track_id + "/", true);
	myAjax.send();
}
