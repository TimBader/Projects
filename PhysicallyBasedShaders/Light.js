"use strict";
function Light(opts){
	this.pos = (opts.pos !== undefined) ? opts.pos : [0,0,0,1];
	this.color = (opts.color !== undefined) ? opts.color : [1,1,1,1];
	//this.shineDirection  = (opts.shineDirection !== undefined) ? opts.shineDirection : [0,0,1,1];
	this.attenuate = (opts.attenuate !== undefined) ? opts.attenuate : [1.0,0.1,0.01];
	this.laser = (opts.laser !== undefined) ? opts.laser : 0;
	this.ambientDiffuseMaxPower = (opts.ambientDiffuseMaxPower !== undefined) ? opts.ambientDiffuseMaxPower : 0.10;
}

Light.prototype.draw = function(prog){
	//var worldMatrix = tdl.translation(this.pos);
	prog.setUniform("lightPos", this.pos);
	prog.setUniform("lightColor", this.color);
	//prog.setUniform("lightShineDirection", this.shineDirection);
	prog.setUniform("lightAttenuate", tdl.mul(1/100,this.attenuate));
	prog.setUniform("ambientDiffuseMaxPower", this.ambientDiffuseMaxPower);
	//prog.setUniform("lights["+num+"].laser", this.laser);
}

Light.prototype.drawPhase2 = function(prog){
	prog.setUniform("lightPos", this.pos);
	prog.setUniform("lightColor", this.color);
	prog.setUniform("ambientDiffuseMaxPower", this.ambientDiffuseMaxPower);
	prog.setUniform("lightAttenuate", tdl.mul(1/100,this.attenuate));
}
