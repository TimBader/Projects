"use strict";

function Material(opts){
	//this.albetoMap = (opts.albetoMap !== undefined) ? opts.albetoMap : new tdl.SolidTexture([209, 22, 7, 255]/*[255, 255, 255, 255]*/);
	//this.reflectanceMap = (opts.reflectanceMap !== undefined) ? opts.reflectanceMap : new tdl.SolidTexture([0.50*255, 0.50*255, 0.50*255, 255]/*[80,80,80,255]*/);	
	//this.roughnessMap = (opts.roughnessMap !== undefined) ? opts.roughnessMap : new tdl.SolidTexture([0.90*255, 0, 0, 255]/*[30,30,30,255]*/);
	//this.normalMap = (opts.normalMap !== undefined) ? opts.normalMap : new tdl.SolidTexture([255/2,255/2,255,255]);

	this.albetoMap = (opts.albetoMap !== undefined) ? opts.albetoMap : new tdl.ColorTexture({width:1,height:1,pixels:[209, 22, 7]},tdl.gl.RGB);
	this.reflectanceMap = (opts.reflectanceMap !== undefined) ? opts.reflectanceMap : new tdl.ColorTexture({width:1,height:1,pixels:[0.50*255, 0.50*255, 0.50*255]},tdl.gl.RGB);	
	this.roughnessMap = (opts.roughnessMap !== undefined) ? opts.roughnessMap : new tdl.ColorTexture({width:1,height:1,pixels:[[0.90*255]]},tdl.gl.LUMINANCE);
	this.normalMap = (opts.normalMap !== undefined) ? opts.normalMap : new tdl.ColorTexture({width:1,height:1,pixels:[255/2,255/2,255]},tdl.gl.RGB);
}

Material.prototype.draw = function(prog){
	prog.setUniform("albetoMap",this.albetoMap);
	prog.setUniform("reflectanceMap",this.reflectanceMap);
	prog.setUniform("roughnessMap",this.roughnessMap);
	prog.setUniform("normalMap", this.normalMap);
}

Material.prototype.copyMe = function(){
	return new Material({albetoMap:this.albetoMap,reflectanceMap:this.reflectanceMap,roughnessMap:this.roughnessMap,normalMap:this.normalMap});
}