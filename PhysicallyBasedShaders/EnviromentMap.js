"use strict"

function EnviromentMap(opts){
	this.urls = opts.urls;
}

EnviromentMap.prototype.loadImages = function(loader){
	this.imgs = [];
	for (var i = 0; i < 6; i++){	
		this.imgs.push(new tdl.Texture2D(loader,this.urls[i],{flipY:false}));
		this.imgs[i].setParameter(gl.TEXTURE_WRAP_S, gl.MIRRORED_REPEAT);
		this.imgs[i].setParameter(gl.TEXTURE_WRAP_T, gl.MIRRORED_REPEAT);
	}
	this.nonBlurredBuffer = new tdl.CubeMap(loader,
				{ px: this.urls[0],nx: this.urls[1], py: this.urls[2],ny: this.urls[3],pz: this.urls[4],nz: this.urls[5]}
            );
}

EnviromentMap.prototype.createBuffers = function(){
	this.imgSize = this.imgs[0].width;

    this.blurredBuffer = new tdl.Framebuffer(this.imgSize,this.imgSize,
        {format:[ [gl.RGBA,gl.FLOAT] ], cubemap: true});

	this.secondBlurBuffer = new tdl.Framebuffer(this.imgSize,this.imgSize,
        {format:[ [gl.RGBA,gl.FLOAT] ]});
}

EnviromentMap.prototype.makeBlur = function(blurProgram, copyProgram, scrUnitSqr){
	blurProgram.use();
	blurProgram.setUniform("basetexture_size",[this.imgSize,this.imgSize,1.0/this.imgSize,1.0/this.imgSize]);
	//blurProgram.setUniform("cubeMap",this.nonBlurredBuffer);
	for (var i = 0; i < 6; i++){
		gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT );
		blurProgram.setUniform("deltas", [1,0]);
		blurProgram.setUniform("image",this.imgs[i]);//uniform sampler2D image
		this.secondBlurBuffer.bind();
		scrUnitSqr.draw(blurProgram);
		this.secondBlurBuffer.unbind();
		this.blurredBuffer.bind(i);
		this.secondBlurBuffer.texture.setParameter(gl.TEXTURE_WRAP_S, gl.MIRRORED_REPEAT);
		this.secondBlurBuffer.texture.setParameter(gl.TEXTURE_WRAP_T, gl.MIRRORED_REPEAT);
		blurProgram.setUniform("deltas", [0,1]);
		blurProgram.setUniform("image", this.secondBlurBuffer.texture);
		scrUnitSqr.draw(blurProgram);
		this.blurredBuffer.unbind();		
	}
}

EnviromentMap.prototype.copyBuffer = function(copyProgram, buffer, scrUnitSqr, imgs){
	copyProgram.use();
	for (var j = 0; j < 6; j++){
		gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT );
		//console.log(imgs[i]);
		copyProgram.setUniform("baseTexture",imgs[j]);
		buffer.bind(j);
		scrUnitSqr.draw(copyProgram);
		buffer.unbind();
	}
}