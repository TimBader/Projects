"use strict";
function LightHandler(){
	this.lights = [];
}

LightHandler.prototype.drawLights = function(prog,screenUSqr){
	for (var i=0;i<this.lights.length;i++){
		this.lights[i].draw(prog);
		screenUSqr.draw(prog);
	}
}

LightHandler.prototype.drawLightsPhase2 = function(prog, screenUSqr){
	for (var i=0;i<this.lights.length;i++){
		this.lights[i].drawPhase2(prog);
		screenUSqr.draw(prog);
	}
}