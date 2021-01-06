const css = `body { scroll-behavior: smooth; }`;


function capitalize(word){
	var word = String(word);
	return word.replace(word.charAt(0),word.charAt(0).toUpperCase());
}


function getActiveTab() {
	if(chrome){
		return chrome.tabs.query({active: true, currentWindow: true}, (activeTab) => {getInfo(activeTab)});
	}else {
    	return browser.tabs.query({active: true, currentWindow: true}).then(getInfo);
    }
}
getActiveTab();

function getInfo(tabs){	//tab array -> [tab]
	let tab = tabs.pop();
	var protocol = tab.url.split(':')[0];
	document.querySelector('#current-tab').textContent = tab.index+1;
	document.querySelector('#status').textContent = capitalize(tab.status);
	document.querySelector('#size').textContent = `${tab.width} x ${tab.height}`;
	/*
	tab.url -> return url of active tab
	tab.title -> return title
	tab.height, tab.width -> return size
	tab.index -> return index of tab (zero based)
	tab.incognito -> return boolean
	tab.pinned -> return boolean
	tab.favIconUrl -> return favIcon url
	tab.status -> return status (loading/complete)
	tab.active -> boolean
	*/
	if(protocol == 'http'){
		document.querySelector('#protocol').textContent = capitalize(protocol);
		document.querySelector('#protocol').style.color = '#ff0000';
	}
	else if(protocol == 'https'){
		document.querySelector('#protocol').textContent = capitalize(protocol);
		document.querySelector('#protocol').style.color = '#0bae0b';
	}
	else{
		document.querySelector('#protocol').textContent = capitalize(protocol);
	}
}


function getTabs(){
	if(chrome){
		chrome.tabs.query({}, (tabs) => totalTabs(tabs));
	} else {
		browser.tabs.query({}).then(totalTabs);
	}  
}
getTabs();

function totalTabs(tabs){
	document.querySelector('#tabs').textContent = tabs.length;
}



function httpResquest(){
	document.body.style.opacity = 0.4;
	var url = 'https://ipinfo.io/json/';
	var http = new XMLHttpRequest();
	http.open("GET",url,true);

	http.onload = function(){
		if (http.status == 200 && http.readyState == 4){
			var data = JSON.parse(http.responseText);
			var x = document.querySelector('.request');
			x.style.display = 'none';
			var y = document.querySelector('.response');
			y.style.display = 'block';
			var z = document.body.querySelector('#responde');
			if (data["ip"]){
				z.textContent = data["ip"].toUpperCase();
			} else {
				z.textContent = "Error occured".toUpperCase();
			}
		}
		else {
			var x = document.querySelector('.request');
			x.style.display = 'none';
			var y = document.querySelector('.response');
			y.style.display = 'block';
			var z = document.body.querySelector('#responde')
			z.textContent = "Error occured".toUpperCase();
		}
		document.body.style.opacity = 1;
	}

	http.onerror = function() {
		var x = document.querySelector('.request');
		x.style.display = 'none';
		var y = document.querySelector('.response');
		y.style.display = 'block';
		var z = document.body.querySelector('#responde')
		z.textContent = "Error occured".toUpperCase();
		document.body.style.opacity = 1;
	}

	http.send();
}

function changeTheme(){
	var element = document.body;
	element.classList.toggle('dark-theme');
}

function copyContent(){
	var copyText = document.getElementById('responde');
	navigator.clipboard.writeText(copyText.textContent).then(function(){
		console.log('copied');
		var changeAttrTitle = document.body.querySelector('.copy');
		changeAttrTitle.attributes.title.value = 'Copied';
	}, function(){
		console.error(`Error at copying content`);
	})
}

document.body.addEventListener("click", (e) => {
	var classList = e.target.classList;
	if (classList.contains("copy")){
		copyContent();
	}
	else if (classList.contains("retry") || classList.contains("find") ){
		httpResquest();
	}
	else if (classList.contains('theme-toggle')){
		changeTheme();
	}
});

