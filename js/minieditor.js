var element_style = `
	display: flex; 
	border: 1px solid #b7b5b5;
`
var minieditor_styles = `
<style type="text/css">
	{} .linenumber {
		width: 5ch; 
		resize: none; overflow: hidden;
		border: none; outline: none;
		text-align: right;
		color: #8e8e8e;
		padding-right: 10px;
		border-right: 1px solid #cccccc;
		border-right-style: dashed;
	}
	{} .editable_area {
		width: 100%;
		min-height: 400px;
		resize: vertical;
		overflow: auto; 
		border: none; outline: none;
		tab-size: 4; 
		-moz-tab-size: 4;
		-o-tab-size: 4;
		white-space: pre;
	}
	{} .linenumber, {} .editable_area {
		line-height: 1.5; font-size: 16px;
	}
</style>
`
// mini multiline editor utilize 2 textarea
// 1st -> used to display linenumber (readOnly)
// 2nd -> allow used write and edit content
/*
	// MiniEditor(element)
	var foobar = new MiniEditor('.foo');
	foobar.build();
*/

var MiniEditor = function(selector){
	this.element = document.querySelector(selector);
	this.selector = selector;
	this.classes = ["linenumber","editable_area"];
	return this;
}

// function return number of lines
MiniEditor.prototype.lines = function(){
	return this.editable_area.value.split("\n").length;
}

// function to build multiline editor 
// textarea, t1, t2 
MiniEditor.prototype.build = function(){
	this.element.style.cssText = element_style;
	document.head.innerHTML += minieditor_styles.replaceAll('{}', this.selector);

	linenumber = document.createElement('textarea');
	editable_area = document.createElement('textarea');
	this.element.appendChild(linenumber);
	this.element.appendChild(editable_area);
	
	linenumber.className = this.classes[0];
	editable_area.className = this.classes[1];
	
	linenumber.readOnly = true;
	linenumber.textContent = "1";
	editable_area.autofocus = true;
	
	editable_area.onscroll = function(){
		this.previousElementSibling.scrollTop = this.scrollTop;
	}
	
	editable_area.oninput = function(){
		var lines = this.value.split('\n');
		this.previousElementSibling.value = "";
		for (var i = 1; i < (lines.length+1); i++) {
			this.previousElementSibling.value += i+"\n";
		}
	}

	this.linenumber = linenumber;
	this.editable_area = editable_area;
	
	return 0;
}