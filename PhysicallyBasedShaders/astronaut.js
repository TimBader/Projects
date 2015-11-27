"use strict"

function Astronaut(opts){
	this.mesh = opts.mesh;
	this.gunMesh = opts.gunMesh;
	//this.pos = [0,35,-13,1];
	this.pos = (opts.pos !== undefined) ? opts.pos : [0,0,0,1];
	this.right = [1,0,0,0];
	this.up = [0,1,0,0];
	this.look = [0,0,1,0];
	this.antilook = [0,0,-1,0];
	//this.origin = [0,1.3,0,1];
	this.origin = (opts.origin !== undefined) ? opts.origin : [0,0,0,1];
	//this.coi = tdl.add(tdl.add(this.origin, this.pos),tdl.mul(-1,this.antilook));
	this.coi = tdl.add(this.pos, this.look);
	this.computeM();
	this.cannonLeftPos;
	this.cannonRightPos;
	this.updateCannonPositions();
}

Astronaut.prototype.computeM = function(){
	this.look = tdl.normalize(tdl.sub(this.coi, this.pos));//W in notes
	this.antilook = tdl.mul(-1,this.look);
	this.right = tdl.normalize(tdl.cross(this.up,this.look)); //W x V //its kinda the right
	this.right.push(0);
	this.up = tdl.normalize(tdl.cross(this.look, this.right));
	this.up.push(0);
	/*this.matrix = tdl.mul(
	[1,0,0,0,
	0,1,0,0,
	0,0,1,0,
	this.pos[0],this.pos[1],this.pos[2],1],
	[this.right[0],this.up[0],this.antilook[0],0,
	this.right[1],this.up[1],this.antilook[1],0,
	this.right[2],this.up[2],this.antilook[2],0,
	0,0,0,1]
	);*/
	this.matrix = [this.right[0],this.up[0],this.antilook[0],0,
	this.right[1],this.up[1],this.antilook[1],0,
	this.right[2],this.up[2],this.antilook[2],0,
	0,0,0,1];
	this.matrix = tdl.mul(-1,this.matrix);
	}

Astronaut.prototype.strafe = function(h, v, d){
	var tmp = tdl.add(tdl.mul(h, this.right), tdl.mul(v, this.up));
	tmp = tdl.add(tmp, tdl.mul(d, this.look));
	var M = tdl.translation(tmp);
	this.pos = tdl.mul(this.pos,M);
	this.coi = tdl.mul(this.coi,M);
	this.computeM();
}

Astronaut.prototype.turn = function(amt){
	var M = tdl.mul(tdl.translation(tdl.mul(-1, this.pos)),
		tdl.axisRotation(this.up, amt), 
		tdl.translation(this.pos));
	this.coi = tdl.mul(this.coi, M);
	this.computeM();
}

Astronaut.prototype.tilt = function(amt){
	var M = tdl.mul(tdl.translation(tdl.mul(-1, this.pos)),
		tdl.axisRotation(this.right, amt), 
		tdl.translation(this.pos));
	this.coi = tdl.mul(this.coi,M);
	this.up = tdl.mul(this.up,M);
	this.computeM();
}

Astronaut.prototype.roll = function(amt){
	var M = tdl.axisRotation(this.antilook, amt);
	//var M = tdl.mul(tdl.translation(tdl.mul(-1, this.eye)),
	//	tdl.axisRotation(this.antilook, amt),
	//	tdl.translation(this.eye));
	this.right = tdl.mul(this.right,M);
	this.up = tdl.mul(this.up,M);
	this.computeM();
}
	
Astronaut.prototype.createRM = function(){
	var x = Math.atan2(this.matrix[6], this.matrix[10]);
	var cy = Math.sqrt(this.matrix[0]*this.matrix[0]+this.matrix[1]*this.matrix[1]);
	var y = Math.atan2(-1*this.matrix[2], cy);
	var sx = Math.sin(x);
	var cx = Math.cos(x);
	var z = Math.atan2(sx*this.matrix[8]-cx*this.matrix[4],cx*this.matrix[5]-sx*this.matrix[9]);
	this.rotM = tdl.mul(tdl.rotation([0,0,1,0],-z),tdl.rotation([0,1,0,0],-y),tdl.rotation([1,0,0,0],-x));
}

Astronaut.prototype.update = function(elapsed){
	this.updateCannonPositions();
}

Astronaut.prototype.updateCannonPositions = function(){
	var centroid = this.gunMesh.centroids[2];
	var x = tdl.mul(this.right, centroid[0]);
	var y = tdl.mul(tdl.mul(-1,this.up), centroid[1]-this.origin[1]);
	var z = tdl.mul(this.look, centroid[2]);
	var meow = tdl.mul(1,tdl.add(tdl.add(z,tdl.mul(y,1)),x));
	var meow2 = tdl.mul(1,tdl.add(tdl.add(z,tdl.mul(y,1)),tdl.mul(-1,x)));
	this.cannonLeftPos = tdl.add(tdl.add(this.pos,tdl.mul(0,this.origin)), meow);
	this.cannonRightPos = tdl.add(tdl.add(this.pos,tdl.mul(0,this.origin)), meow2);
	this.cannonLeftPos[3] = 1;this.cannonRightPos[3] = 1;
}

Astronaut.prototype.draw = function(prog){
	this.createRM();
	var worldMatrix = tdl.mul(tdl.translation(tdl.mul(-1,this.origin)),this.rotM,tdl.translation(this.pos));
	prog.setUniform("worldMatrix",worldMatrix);
	prog.setUniform("stopLighting",0);
	this.mesh.draw(prog);
	this.gunMesh.draw(prog);
}