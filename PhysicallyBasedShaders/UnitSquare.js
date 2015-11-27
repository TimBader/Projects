"use strict";
function UnitSquare(){
    var vdata;
    //x,y,z, s,t nx,ny,nz
    vdata=new Float32Array(
        [
            -1, 1, 0,   0,1,
            -1,-1, 0,   0,0,
             1, 1, 0,   1,1,
             1,-1, 0,   1,0
        ]
    );
    var vb = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER,vb);
    gl.bufferData(gl.ARRAY_BUFFER,vdata,gl.STATIC_DRAW);
    this.vbuff=vb;
}
UnitSquare.prototype.draw = function(prog){
    gl.bindBuffer(gl.ARRAY_BUFFER,this.vbuff);
    prog.setVertexFormat(
        "position",3,gl.FLOAT,
        "texcord",2,gl.FLOAT
    );
    gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
}

UnitSquare.prototype.drawS = function(prog){
	gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
}

UnitSquare.prototype.drawS0 = function(prog){
    gl.bindBuffer(gl.ARRAY_BUFFER,this.vbuff);
    prog.setVertexFormat(
        "position",3,gl.FLOAT,
        "texcord",2,gl.FLOAT
    );
}