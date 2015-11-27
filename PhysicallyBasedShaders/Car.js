"use strict"

function Car(opts){
	this.bodyMesh = opts.bodyMesh;
	this.wheelMesh = opts.wheelMesh;
	//this.pos = [0,35,-13,1];
	this.pos = (opts.pos !== undefined) ? opts.pos : [0,0,0,1];
	this.right = [1,0,0,0];
	this.up = [0,1,0,0];
	this.look = [0,0,1,0];
	this.antilook = [0,0,-1,0];
	this.size = (opts.size !== undefined) ? opts.size : 1;
	this.wheelSize = (opts.wheelSize !== undefined) ? opts.wheelSize : this.size;
	//this.origin = [0,1.3,0,1];
	this.origin = (opts.origin !== undefined) ? opts.origin : [0,0,0,1];
	//this.coi = tdl.add(tdl.add(this.origin, this.pos),tdl.mul(-1,this.antilook));
	this.coi = tdl.add(this.pos, this.look);
	/*
	this.rightFrontWheelLocalPos = tdl.mul([-4.111,1.508,5.861,0],this.size);
	this.leftFrontWheelLocalPos = tdl.mul([4.111,1.508,5.861,0],this.size);
	this.rightBackWheelLocalPos = tdl.mul([-4.111,1.508,-5.704,0],this.size);
	this.leftBackWheelLocalPos = tdl.mul([4.111,1.508,-5.704,0],this.size);
	*/
	this.rightFrontWheelLocalPos = tdl.mul([1.236,-0.285,-1.893,0],this.size);
	this.leftFrontWheelLocalPos = tdl.mul([-1.236,-0.285,-1.893,0],this.size);
	this.rightBackWheelLocalPos = tdl.mul([1.001,-0.285,1.784,0],this.size);
	this.leftBackWheelLocalPos = tdl.mul([-1.001,-0.285,1.704,0],this.size);
	this.rightFrontWheelPos = this.rightFrontWheelLocalPos;
	this.leftFrontWheelPos = this.leftFrontWheelLocalPos;
	this.rightBackWheelPos = this.rightBackWheelLocalPos;
	this.leftBackWheelPos = this.leftBackWheelLocalPos;
	this.wheelRotation = 0.0;
	this.wheelRotationSpeed = 0;
	this.transparent = false;
	this.bodyMaterial = (opts.bodyMaterial !== undefined) ? opts.bodyMaterial : this.bodyMesh.defaultMaterial.copyMe();
	this.wheelMaterial = (opts.wheelMaterial !== undefined) ? opts.wheelMaterial : this.wheelMesh.defaultMaterial.copyMe();
	
	this.updateScaleOriginMatrix();
	this.updateWheelScaleOriginMatrix();
	this.computeM();
	this.createRM();
	
	this.worldMatrix;
	this.worldMatrix = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1];	
	this.wheelMatrixs = [];
	
	
	this.updateMe = false;
	this.updateWheelPositions();
	this.updateWorldMatrix();	
}

Car.prototype.changeScale = function(scale){
	this.size = scale;
	this.updateScaleOriginMatrix();
}

Car.prototype.changeOrigin = function(vector){
	this.origin = vector;
	this.updateScaleOriginMatrix();
}

Car.prototype.updateScaleOriginMatrix = function(){
	this.scaleOriginMatrix = tdl.mul(tdl.scaling([this.size,this.size,this.size]), tdl.translation(tdl.mul(-1,this.origin)));
}

Car.prototype.updateWheelScaleOriginMatrix = function(){
	this.wheelScaleOriginMatrix = tdl.mul(tdl.scaling([this.wheelSize,this.wheelSize,this.wheelSize]), tdl.translation(tdl.mul(-1,this.origin)));
}

Car.prototype.computeM = function(){
	this.look = tdl.normalize(tdl.sub(this.coi, this.pos));//W in notes
	this.antilook = tdl.mul(-1,this.look);
	this.right = tdl.normalize(tdl.cross(this.up,this.look)); //W x V //its kinda the right
	//this.right.push(0);
	this.up = tdl.normalize(tdl.cross(this.look, this.right));
	//this.up.push(0);
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
	this.matrix = [this.right[0],this.up[0],this.look[0],0,
	this.right[1],this.up[1],this.look[1],0,
	this.right[2],this.up[2],this.look[2],0,
	0,0,0,1];
	//this.matrix = tdl.mul(-1,this.matrix);
	}

Car.prototype.strafe = function(h, v, d){
	var tmp = tdl.add(tdl.mul(h, this.right), tdl.mul(v, this.up));
	tmp = tdl.add(tmp, tdl.mul(d, this.look));
	var M = tdl.translation(tmp);
	this.pos = tdl.mul(this.pos,M);
	this.coi = tdl.mul(this.coi,M);
	this.updateMe = true;	
	//this.computeM();
}

Car.prototype.turn = function(amt){
	var M = tdl.mul(tdl.translation(tdl.mul(-1, this.pos)),
		tdl.axisRotation(this.up, amt), 
		tdl.translation(this.pos));
	this.coi = tdl.mul(this.coi, M);
	this.updateMe = true;
	this.computeM();
}

Car.prototype.tilt = function(amt){
	var M = tdl.mul(tdl.translation(tdl.mul(-1, this.pos)),
		tdl.axisRotation(this.right, amt), 
		tdl.translation(this.pos));
	this.coi = tdl.mul(this.coi,M);
	this.up = tdl.mul(this.up,M);
	this.updateMe = true;
	this.computeM();
}

Car.prototype.roll = function(amt){
	var M = tdl.axisRotation(this.antilook, amt);
	//var M = tdl.mul(tdl.translation(tdl.mul(-1, this.eye)),
	//	tdl.axisRotation(this.antilook, amt),
	//	tdl.translation(this.eye));
	this.right = tdl.mul(this.right,M);
	this.up = tdl.mul(this.up,M);
	this.updateMe = true;
	this.computeM();
}
	
Car.prototype.createRM = function(){
	var x = Math.atan2(this.matrix[6], this.matrix[10]);
	var cy = Math.sqrt(this.matrix[0]*this.matrix[0]+this.matrix[1]*this.matrix[1]);
	var y = Math.atan2(-1*this.matrix[2], cy);
	var sx = Math.sin(x);
	var cx = Math.cos(x);
	var z = Math.atan2(sx*this.matrix[8]-cx*this.matrix[4],cx*this.matrix[5]-sx*this.matrix[9]);
	this.rotM = tdl.mul(tdl.rotation([0,0,1,0],-z),tdl.rotation([0,1,0,0],-y),tdl.rotation([1,0,0,0],-x));
}

Car.prototype.update = function(elapsed){
	this.wheelRotation += this.wheelRotationSpeed*elapsed;
	if (this.updateMe == true){
		this.computeM();
		this.updateWheelPositions();
		this.updateWorldMatrix();
		this.updateMe = false;
	}
}

Car.prototype.updateWheelPositions = function(){
	this.rightFrontWheelPos = this.updateLocalPosition(this.rightFrontWheelLocalPos);
	this.leftFrontWheelPos = this.updateLocalPosition(this.leftFrontWheelLocalPos);
	this.rightBackWheelPos = this.updateLocalPosition(this.rightBackWheelLocalPos);
	this.leftBackWheelPos = this.updateLocalPosition(this.leftBackWheelLocalPos);
}

Car.prototype.updateLocalPosition = function(localPosition){
	var x = tdl.mul(localPosition[0],this.right);
	var y = tdl.mul(localPosition[1],this.up);
	var z = tdl.mul(localPosition[2],this.look);
	return tdl.add(tdl.add(x,y),z);
}

Car.prototype.updateWorldMatrix = function(){
	this.createRM();
	var scaleRotMat = tdl.mul(this.scaleOriginMatrix,this.rotM);
	this.worldMatrix = tdl.mul(scaleRotMat,tdl.translation(this.pos));

	scaleRotMat = tdl.mul(this.wheelScaleOriginMatrix, this.rotM);
	
	this.wheelMatrixs[0] = tdl.mul(scaleRotMat, tdl.axisRotation(this.right,this.wheelRotation),tdl.axisRotation(this.up, 3.14159/4),tdl.translation(tdl.add(this.pos,this.rightFrontWheelPos)));
	this.wheelMatrixs[1] = tdl.mul(scaleRotMat, tdl.axisRotation(this.right,tdl.mul(this.wheelRotation,-1)),tdl.axisRotation(this.up, 3.14159+3.14159/4),tdl.translation(tdl.add(this.pos,this.leftFrontWheelPos)));	
	this.wheelMatrixs[2] = tdl.mul(scaleRotMat, tdl.axisRotation(this.right,this.wheelRotation),tdl.translation(tdl.add(this.pos,this.rightBackWheelPos)));
	this.wheelMatrixs[3] = tdl.mul(scaleRotMat, tdl.axisRotation(this.right,tdl.mul(this.wheelRotation,-1)),tdl.axisRotation(this.up, 3.14159),tdl.translation(tdl.add(this.pos,this.leftBackWheelPos)));
}

Car.prototype.draw = function(prog){
	//this.createRM();
	//var worldMatrix = tdl.mul(this.scaleOriginMatrix,this.rotM,tdl.translation(this.pos));
	prog.setUniform("worldMatrix",this.worldMatrix);
	this.bodyMaterial.draw(prog);
	this.bodyMesh.draw(prog);
	
	//var baseWheelMatrix = tdl.mul(this.scaleOriginMatrix,this.rotM);
	this.wheelMaterial.draw(prog);
	
	//prog.setUniform("worldMatrix",tdl.mul(baseWheelMatrix,tdl.axisRotation(this.right,this.wheelRotation),tdl.axisRotation(this.up, 3.14159/4),tdl.translation(tdl.add(this.pos,this.rightFrontWheelPos))));	
	prog.setUniform("worldMatrix", this.wheelMatrixs[0]);
	this.wheelMesh.draw(prog);
	//prog.setUniform("worldMatrix",tdl.mul(baseWheelMatrix,tdl.axisRotation(this.right,tdl.mul(this.wheelRotation,-1)),tdl.axisRotation(this.up, 3.14159+3.14159/4),tdl.translation(tdl.add(this.pos,this.leftFrontWheelPos))));	
	prog.setUniform("worldMatrix", this.wheelMatrixs[1]);
	this.wheelMesh.draw(prog);
	//prog.setUniform("worldMatrix",tdl.mul(baseWheelMatrix,tdl.axisRotation(this.right,this.wheelRotation),tdl.translation(tdl.add(this.pos,this.rightBackWheelPos))));	
	prog.setUniform("worldMatrix", this.wheelMatrixs[2]);
	this.wheelMesh.draw(prog);
	//prog.setUniform("worldMatrix",tdl.mul(baseWheelMatrix,tdl.axisRotation(this.right,tdl.mul(this.wheelRotation,-1)),tdl.axisRotation(this.up, 3.14159),tdl.translation(tdl.add(this.pos,this.leftBackWheelPos))));		
	prog.setUniform("worldMatrix", this.wheelMatrixs[3]);
	this.wheelMesh.draw(prog);
}

Car.prototype.drawShadow = function(prog){
	prog.setUniform("worldMatrix",this.worldMatrix);
	this.bodyMesh.draw(prog);
	
	prog.setUniform("worldMatrix", this.wheelMatrixs[0]);
	this.wheelMesh.draw(prog);
	prog.setUniform("worldMatrix", this.wheelMatrixs[1]);
	this.wheelMesh.draw(prog);
	prog.setUniform("worldMatrix", this.wheelMatrixs[2]);
	this.wheelMesh.draw(prog);
	prog.setUniform("worldMatrix", this.wheelMatrixs[3]);
	this.wheelMesh.draw(prog);	
}