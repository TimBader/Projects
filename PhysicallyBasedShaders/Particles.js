/* 
    Daniel Fairbanks
    Computer Graphics: Hudson
    5 May 2015
--------------------------------------------------------------------------------
Particle.js:
    This file creates a randomized Particle based upon the parameters passed. The
    particle will have a random spawn location and velocity and have a limited time
    to live. The color of the particle will be passed by the user to allow for 
    variation. The particle is stored in a list in main.js.
*/
"use strict";


function Particles(np){
    var w = 1;
    var h = Math.floor(np/100);
    np = w*h;
    
    this.w = w;
    this.h = h;
    this.idx = 0;
    this.lifeleft = 0;
    this.nump = np;
    
    this.pos = [];
    this.vel = [];
    
    for(var i=0;i<2;++i){
        var f = new tdl.Framebuffer( w,h, { depth: false, format: [ [gl.RGBA,gl.FLOAT] ] } );
        f.texture.setParameter(gl.TEXTURE_MIN_FILTER,gl.NEAREST);
        f.texture.setParameter(gl.TEXTURE_MAG_FILTER,gl.NEAREST);
        f.texture.setParameter(gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);
        f.texture.setParameter(gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
        this.pos.push(f);
        f = new tdl.Framebuffer( w,h, { depth: false, format: [ [gl.RGBA,gl.FLOAT] ] } );
        f.texture.setParameter(gl.TEXTURE_MIN_FILTER,gl.NEAREST);
        f.texture.setParameter(gl.TEXTURE_MAG_FILTER,gl.NEAREST);
        f.texture.setParameter(gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);
        f.texture.setParameter(gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
        this.vel.push(f);
    }
    
    if( Particles.vbuffers[np] === undefined ){
        var vdata = [];
        for(var i=0;i<h;++i){
            for(var j=0;j<w;++j){
                vdata.push( (j+0.5)/w, (i+0.5)/h );
            }
        }
        Particles.vbuffers[np] = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, Particles.vbuffers[np]);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vdata), gl.STATIC_DRAW);
    }
};
Particles.load = function(loader){
    Particles.updateprog = new tdl.Program(loader,"psys-updatevs.txt","psys-updatefs.txt");
    Particles.drawprog = new tdl.Program(loader,"psys-drawvs.txt","psys-drawfs.txt");
    Particles.usq = new UnitSquare();
    Particles.vbuffers=[];
    Particles.dummytex = new tdl.SolidTexture([255,255,255,255]);
};
Particles.prototype.randrange = function(n,x){
    return n + Math.random() * (x-n);
};
Particles.prototype.init = function(startpos, color){
    this.idx = 0;
    
    //the whole system has a total life of 4000msec = 4sec
    this.lifeleft = 4000;
    
    //all the starting positions are the same
    var tmp = startpos.slice(0,3).concat(0);
    this.pos[0].clear( tmp );

    //make a bunch of random velocities + lifetimes
    var V=[];
    for(var i=0;i<this.nump;++i){
        var v = [
            this.randrange( -0.003,0.003 ),
            -0.002,
            this.randrange( -0.003,0.003),
            this.randrange(0.2*this.lifeleft, 1.0*this.lifeleft)
        ];
        V.push(v[0],v[1],v[2],v[3]);
    }
    this.vel[0].initializeData(V);
    this.color=color;
    
};
Particles.prototype.update = function(elapsed){
    if(this.lifeleft <= 0)
        return;

    //gl.disable(gl.BLEND);
    //Particles.updateprog.use();
    Particles.updateprog.setUniform("postex",this.pos[this.idx]);
    Particles.updateprog.setUniform("veltex",this.vel[this.idx]);
	//Particles.updateprog.setUniform("texs",[this.pos[this.idx],this.vel[this.idx]]);	
    
    //gravity: units per msec
    //Particles.updateprog.setUniform("g",[0,-0.000005,0]);
    
    //in msec
    //Particles.updateprog.setUniform("elapsed",elapsed);
    
    //update positions
    Particles.updateprog.setUniform("mode", 0);
    this.pos[1-this.idx].bind();
    Particles.usq.drawS(Particles.updateprog);
    this.pos[1-this.idx].unbind();
    
    //update velocities + life left
    Particles.updateprog.setUniform("mode", 1);
    this.vel[1-this.idx].bind();
    Particles.usq.drawS(Particles.updateprog);
    this.vel[1-this.idx].unbind();
    
    this.idx = 1 - this.idx;
    this.lifeleft -= elapsed;
    //gl.enable(gl.BLEND);
};

Particles.prototype.draw = function(/*camera*/){
    if(this.lifeleft <= 0)
        return;
 
    //Particles.drawprog.use();
    //camera.draw(Particles.drawprog);
    //Particles.drawprog.setUniform("color", this.color);
    Particles.drawprog.setUniform("postex", this.pos[this.idx]);
    Particles.drawprog.setUniform("veltex", this.vel[this.idx]);
    gl.bindBuffer(gl.ARRAY_BUFFER, Particles.vbuffers[this.nump]);
    Particles.drawprog.setVertexFormat("position", 2, gl.FLOAT);
    gl.drawArrays(gl.POINTS, 0, this.nump);
    
    //make sure we can update the pos and vel textures on the next go-round
    //Particles.drawprog.setUniform("postex", Particles.dummytex);
    //Particles.drawprog.setUniform("veltex", Particles.dummytex);
    
};