
function getPosts() { 

	var req = new XMLHttpRequest(); 
	req.onreadystatechange = function() {
		if (req.readyState !=4) return;
		if (req.status != 200) return;
		var posts = JSON.parse(req.responseText);
		updatePosts(posts)
	}
	
	req.open("GET", "/socialnetwork/get-posts-json", true);
	req.send();
}

function updatePosts() {
	
	var posts = document.getElementById("posts"); 
	while (posts.hasChildNodes()) { 
		posts.removeChild(posts.firstChild);
	}
	
	for (var i=0, i< posts.length; i++) { 
	
		var username = posts[i]["fields"]["user"];
		var post_text = posts[i]["fields"]["post_text"];
		var post_date = posts[i]["fields"]["post_date"];
		
		var newPost = document.createElement("div");
		newPost.innerHTML = username + post_text  + post_date; 
		
		posts.appendChild(newPost);
	}
	
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}
	
function postItem() { 

	var postText = document.getElementById("post").value; 
	var req = new XMLHttpRequest(); 
	req.onreadystatechange = function() { 
		if (req.readyState != 4) return; 
		if (req.status != 200) return; 
		var posts = JSON.parse(req.responseText);
		updatePosts(posts);
	}
	
	req.open("POST", "/socialnetwork/global-stream", true);
	req.setRequestHeader("Content-type", "application/x-www-form-urlencoded"); 
	req.send("post=" + postText + "&csrfmiddlewaretoken="+getCSRFToken());

}

window.onload = getPosts; 

window.setInterval(getPosts, 5000); 
