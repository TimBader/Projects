"use strict";


function Heightmap(loader,imagefile,xsize,ysize,zsize,material){
    //loader is the tdl loader object.
    //imagefile is the image from which we will obtain our height data.
    var that=this;
    var xmin = -xsize/2;
    var ymin = 0;
    var zmin = -zsize/2;
    this.xmin = xmin;
    this.ymin = ymin;
    this.zmin = zmin;
    this.xsize=xsize;
    this.ysize=ysize;
    this.zsize=zsize;
	
	this.material = material;

    this.mins = [xmin,ymin,zmin];
    this.maxs = [xmin+xsize,ymin+ysize,zmin+zsize];
    this.sizes = [this.xsize,this.ysize,this.zsize];
   
    loader.loadImage(imagefile,function(img){
        that.img = img;
        
        if(!Heightmap.grids[img.width] || !Heightmap.grids[img.width][img.height] )
            Heightmap.make_grid(img.width,img.height);
        
        //for debugging
        var dbgimg = document.getElementById("heightmap");
        if( dbgimg )
            dbgimg.src=imagefile;
        
        //extract image data
        var cvs = document.createElement("canvas");
        cvs.width = img.width;
        cvs.height = img.height;
        var ctx = cvs.getContext("2d");
        ctx.drawImage(img,0,0);
        var id = ctx.getImageData(0,0,cvs.width,cvs.height);

        //extract height data
        that.heightdata=[];
        for(var y=0;y<cvs.height;++y){
            for(var x=0;x<cvs.width;++x){
                var idx = y*cvs.width*4+x*4;
                var red = id.data[idx];
                that.heightdata.push( red ); //(red/255)*ysize );
            }
        }
        
        that.heighttexture = new tdl.ColorTexture({width:cvs.width,height:cvs.height,
                pixels: that.heightdata, format: gl.LUMINANCE});
        that.heighttexture.setParameter(gl.TEXTURE_MIN_FILTER,gl.LINEAR);
        that.heighttexture.setParameter(gl.TEXTURE_MAG_FILTER,gl.LINEAR);
       
    });
    this.texture = new tdl.SolidTexture([150,190,94,255]);
}

Heightmap.grids={};

Heightmap.prototype.load = function(loader){
    //Heightmap.prog = new tdl.Program(loader,"hmapvs.txt","hmapfs.txt");
}

Heightmap.make_grid = function(w,h)
{        
    
    if(w*h>1165536)
        throw new Error("Too big");
        
    if( !Heightmap.grids[w] )
        Heightmap.grids[w]={};
        
    if( Heightmap.grids[w][h] !== undefined )
        return;
        
    //each vertex has s,t
    var vdata=[];
    for(var z=0;z<h;++z){
        var t = (z+0.5)/h
        for(var x=0;x<w;++x){
            var s = (x+0.5)/w;
            vdata.push(s,t);
        }
    }
    
    vdata = new Float32Array(vdata);
    var vbuff = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vbuff);
    gl.bufferData(gl.ARRAY_BUFFER, vdata, gl.STATIC_DRAW);
        
    //generate index data to link them together.
    //Use triangle strip.
    var J=[];
    var initial,final,inc
    for(var i=0;i< h-1; i++){
        if( i%2 === 0 ){    //L to R
            initial=0;
            final=w;
            inc=1;
        }
        else{
            initial=w-1;    //R to L
            final=-1;
            inc=-1;
        }
        for(var j=initial; j!=final; j+=inc ){
            J.push(w*i+j);
            J.push(w*(i+1)+j);
        }
        if( i != h-2 )
            J.push( J[J.length-1] );
    }
    
    var idata = new Uint16Array(J);
    var ibuff = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibuff);
    gl.bufferData( gl.ELEMENT_ARRAY_BUFFER, idata, gl.STATIC_DRAW);
    var ni = J.length;         
    
    Heightmap.grids[w][h] = {vbuff:vbuff,ibuff:ibuff,ni:ni};
}

/*Heightmap.prototype.draw = function(camera,lightPos){
    var prog = Heightmap.prog;
    prog.use();
    camera.draw(prog);
    prog.setUniform("lightPos",lightPos);
    prog.setUniform("texture",this.texture);
    prog.setUniform("heighttexture",this.heighttexture);
    prog.setUniform("mins",this.mins);
    prog.setUniform("maxs",this.maxs);
    
    var img=this.img;
    var B=Heightmap.grids[img.width][img.height];
    gl.bindBuffer(gl.ARRAY_BUFFER,B.vbuff);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,B.ibuff);
    prog.setVertexFormat( "a_texcoord",2,gl.FLOAT );
    gl.drawElements( gl.TRIANGLE_STRIP, B.ni, gl.UNSIGNED_SHORT, 0);
}*/

Heightmap.prototype.draw = function(prog){
	//prog.setUniform("texture", this.texture);
	prog.setUniform("heighttexture", this.heighttexture);
	prog.setUniform("heighttexture_size",[this.xsize,this.ysize,1/this.xsize,1/this.ysize]);
	prog.setUniform("mins", this.mins);
	prog.setUniform("maxs", this.maxs);
	prog.setUniform("worldMatrix",[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
	this.material.draw(prog);
	
    var B=Heightmap.grids[this.img.width][this.img.height];
    gl.bindBuffer(gl.ARRAY_BUFFER,B.vbuff);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,B.ibuff);
    prog.setVertexFormat( "a_texcoord",2,gl.FLOAT );
    gl.drawElements( gl.TRIANGLE_STRIP, B.ni, gl.UNSIGNED_SHORT, 0);	
}

Heightmap.prototype.drawShadow = function(prog){
	//prog.setUniform("texture", this.texture);
	prog.setUniform("heighttexture", this.heighttexture);
	prog.setUniform("heighttexture_size",[this.xsize,this.ysize,1/this.xsize,1/this.ysize]);
	prog.setUniform("mins", this.mins);
	prog.setUniform("maxs", this.maxs);
	prog.setUniform("worldMatrix",[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);

    var B=Heightmap.grids[this.img.width][this.img.height];
    gl.bindBuffer(gl.ARRAY_BUFFER,B.vbuff);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,B.ibuff);
    prog.setVertexFormat( "a_texcoord",2,gl.FLOAT );
    gl.drawElements( gl.TRIANGLE_STRIP, B.ni, gl.UNSIGNED_SHORT, 0);
}
