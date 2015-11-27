function KeyboardHandler(){
	var tmp = document.getElementsByTagName("body");
	this.body = tmp[0];	
	this.evList = []; //spot = ASCII number being pressed
}
	
KeyboardHandler.prototype.checkForKey = function(keyCode, pressed){
	var pressed = pressed || 0;
	//console.log(this.evList);
	if (this.evList.length > 0)
		for (var i=0;i<this.evList.length;i++){
			if (this.evList[i].keyCode === keyCode)
				if (pressed === 0)
					return (1);
				else
					return (0);
		}
	if (pressed === 0)
		return (0);
	else
		return (1);
}