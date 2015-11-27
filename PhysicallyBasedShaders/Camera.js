"use strict";

function Camera (opts){
	this.fov = (opts.fov !== undefined) ? opts.fov : 90.0*3.14/180;
	this.aspect_ratio = opts.canvasWidth / opts.canvasHeight;
	this.eye = (opts.eye !== undefined) ? opts.eye : [0,0,0,1];
	this.coi = (opts.coi !== undefined) ? opts.coi : [0,0,0,1];
	this.up = (opts.up !== undefined) ? opts.up : [0,1,0,0];
	this.hither = (opts.hither !== undefined) ? opts.hither : 0.1;
	this.yon = (opts.yon !== undefined) ? opts.yon : 1000;
	this.computePM();
}

Camera.prototype.computePM = function(){
	var av = this.fov/2;
	var ah = this.aspect_ratio*av;
	var R = this.hither*Math.tan(ah);var L = -1*R;
	var T = this.hither*Math.tan(av);var B = -1*T;
	this.projectionMatrix = [
		2*this.hither/(R-L),0,0,0,
		0,2*this.hither/(T-B),0,0,
		1+2*L/(R-L), 1+2*B/(T-B), this.yon/(this.hither-this.yon),-1,
		0,0,this.hither*this.yon/(this.hither-this.yon),0];
}

Camera.prototype.set = function(eye, coi, up){
	this.eye=eye;           
	this.coi=coi;
	this.up=up;
	this.computeVM();
}

Camera.prototype.computeVM = function(){
	this.antilook = tdl.normalize(tdl.sub(this.eye, this.coi));
	this.right = tdl.normalize(tdl.cross(this.up,this.antilook)); //W x V //its kinda the right
	this.up = tdl.normalize(tdl.cross(this.antilook, this.right));
	this.viewMatrix = tdl.mul(
	[1,0,0,0,
	0,1,0,0,
	0,0,1,0,
	-1*this.eye[0],-1*this.eye[1],-1*this.eye[2],1],
	[this.right[0],this.up[0],this.antilook[0],0,
	this.right[1],this.up[1],this.antilook[1],0,
	this.right[2],this.up[2],this.antilook[2],0,
	0,0,0,1]
	);
	
	}

Camera.prototype.strafe = function(h, v, d){
	var tmp = tdl.add(tdl.mul(h, this.right), tdl.mul(v, this.up));
	tmp = tdl.add(tmp, tdl.mul(d, this.antilook));
	var M = tdl.translation(tmp);
	this.eye = tdl.mul(this.eye,M);
	this.coi = tdl.mul(this.coi,M);
	this.computeVM();
}

Camera.prototype.turn = function(amt){
	var M = tdl.mul(tdl.translation(tdl.mul(-1, this.eye)),
		tdl.axisRotation(this.up, amt), 
		tdl.translation(this.eye));
	this.coi = tdl.mul(this.coi, M);
	this.computeVM();
}

Camera.prototype.tilt = function(amt){
	var M = tdl.mul(tdl.translation(tdl.mul(-1, this.eye)),
		tdl.axisRotation(this.right, amt), 
		tdl.translation(this.eye));
	this.coi = tdl.mul(this.coi,M);
	this.up = tdl.mul(this.up,M);
	this.computeVM(); 
}

Camera.prototype.roll = function(amt){
	var M = tdl.axisRotation(this.antilook, amt);
	//var M = tdl.mul(tdl.translation(tdl.mul(-1, this.eye)),
	//	tdl.axisRotation(this.antilook, amt),
	//	tdl.translation(this.eye));
	this.right = tdl.mul(this.right,M);
	this.up = tdl.mul(this.up,M);
	this.computeVM();
}

Camera.prototype.draw = function(prog){
	var pv = tdl.mul(this.viewMatrix,this.projectionMatrix);
	prog.setUniform("viewProjMatrix", pv);
	prog.setUniform("eyePos",this.eye);
	//prog.setUniform("eyePos",[0,0,0,1]);
    //prog.setUniform("cameraU",this.up.slice(0,3));
    //prog.setUniform("cameraV",this.right.slice(0,3));
    //prog.setUniform("cameraW",this.antilook.slice(0,3)); //0.3?
}

Camera.prototype.drawPhase2 = function(prog){
	prog.setUniform("eyePos",this.eye);
}

Camera.prototype.drawShadow = function(prog){
	prog.setUniform("projMatrix", this.projectionMatrix);
	prog.setUniform("viewMatrix", this.viewMatrix);
	prog.setUniform("hitheryon",[this.hither, this.yon, this.yon-this.hither]);
}