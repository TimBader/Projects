"use strict";

function Object3d(opts){
	//pos, moveAxis, vel, startRot, rotAxis, rotVel, size, mesh, origin, time2Live
	this.pos = opts.pos; 
	this.moveVector = (opts.moveVector !== undefined) ? opts.moveVector : [0,0,0,1];
	this.vel = (opts.vel !== undefined) ? opts.vel : 0;
	this.startRot = (opts.startRot !== undefined) ? opts.startRot : [0,0,0,1];
	this.rotAxis = (opts.rotAxis !== undefined) ? opts.rotAxis : [0,1,0,0];
	this.rot = (opts.rot !== undefined) ? opts.rot : 0;
	this.rotVel = (opts.rotVel !== undefined) ? opts.rotVel : 0;
	this.size = (opts.size !== undefined) ? opts.size : 1;
	this.mesh = opts.mesh;
	this.origin = (opts.origin !== undefined) ? opts.origin : [0,0,0,1];
	this.time2Live = (opts.time2Live !== undefined) ? opts.time2Live : undefined;
	this.extraMove = (opts.extraMove !== undefined) ? opts.extraMove : [0,0,0,0];
	this.boundingRadius = (opts.boundingRadius !== undefined) ? opts.boundingRadius : 1;
	this.transparent = (opts.transparent !== undefined) ? opts.transparent : false;
	this.collisionRadiusSqrd = (opts.collisionRadiusSqrd !== undefined) ? opts.collisionRadiusSqrd : 1;
	this.material = (opts.material !== undefined) ? opts.material : this.mesh.defaultMaterial.copyMe();
	if (this.startRot.length != 16)
		this.startRot = [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1];	
	this.origin = tdl.mul(this.size,this.origin);
	this.deleteMe = false;
	this.worldMatrix;
	this.updateWorldMatrix();	
}

Object3d.prototype.update = function(elapsed){
	var updateMe = false;
	if (this.vel != 0.0){
		this.pos = tdl.add(this.pos, tdl.mul(elapsed, tdl.mul(this.vel, this.moveVector)));
		this.pos = tdl.add(this.pos, tdl.mul(1, this.extraMove));
		this.pos[3] = 1;
		updateMe = true;
	}
	if (this.rotVel != 0.0){
		this.rot += this.rotVel*elapsed;
		if (this.time2Live != undefined){
			this.time2Live -= elapsed;
			if (this.time2Live <= 0)
				this.deleteMe = true;
		}
		updateMe = true;
	}
	if (updateMe == true){
		this.updateWorldMatrix();
	}
}

Object3d.prototype.updateWorldMatrix = function(){
	this.worldMatrix = tdl.mul(tdl.scaling([this.size,this.size,this.size]), this.startRot, tdl.translation(tdl.mul(-1,this.origin)), tdl.axisRotation(this.rotAxis,this.rot), tdl.translation(this.pos));
}

Object3d.prototype.draw = function(prog){
	prog.setUniform("worldMatrix", this.worldMatrix);
	this.material.draw(prog);
	this.mesh.draw(prog);
}

Object3d.prototype.drawShadow = function(prog){
	prog.setUniform("worldMatrix", this.worldMatrix);
	this.mesh.draw(prog);
}