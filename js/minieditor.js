var element_style = `
	display: flex; 
	border: 1px solid #b7b5b5;
`
var minieditor_styles = `
<style type="text/css">
	.linenumber {
		width: 5ch; 
		resize: none; overflow: hidden;
		border: none; outline: none;
		text-align: right;
		color: #8e8e8e;
		padding-right: 10px;
	}
	.editable_area {
		width: 100%;
		min-height: 150px;
		resize: vertical;
		overflow: auto; 
		border: none; outline: none;
		tab-size: 4; 
		-moz-tab-size: 4;
		white-space: pre;
	}
	.linenumber, .editable_area {
		line-height: 1.5; font-size: 14px;
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
	this.linenumber = undefined;
	this.editable_area = undefined;
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
	document.head.innerHTML += minieditor_styles;
	linenumber = document.createElement('textarea');
	editable_area = document.createElement('textarea');
	linenumber.className = "linenumber";
	editable_area.className = "editable_area";
	this.element.appendChild(linenumber);
	this.element.appendChild(editable_area);
	linenumber.readOnly = true;
	linenumber.textContent = "1";
	function scroll_t1(e){
		editable_area.scrollTop = linenumber.scrollTop;
	}
	function scroll_t2(e){
		linenumber.scrollTop = editable_area.scrollTop;
	}
	linenumber.addEventListener("scroll", scroll_t1, false);
	editable_area.addEventListener("scroll", scroll_t2, false);
	editable_area.oninput = function(){
		var lines = this.value.split('\n');
		linenumber.value = "";
		for (var i = 1; i < (lines.length+1); i++) {
			linenumber.value += i+"\n";
		}
	}
	this.linenumber = linenumber;
	this.editable_area = editable_area;
	return 0;
}