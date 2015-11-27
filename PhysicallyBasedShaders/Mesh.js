"use strict";

function Mesh(loader, url){
	var that=this;
	var vbuff;
	var ibuff;
	this.vertexNum=0;
	this.indexNum=0;
	this.defaultMaterial = new Material({});
	this.centroids = [];
	loader.loadArrayBuffer("models/"+url,function(abuffer){
			that.setup(abuffer,loader);
		});
	}
	
Mesh.prototype.getVertexNum = function(){
	return (this.vertexNum);
}
Mesh.prototype.getIndexNum = function(){
	return (this.indexNum);
}

Mesh.prototype.setup = function(ab, loader){
	var idx = 0;
	var dv = new DataView(ab);
	function readLine(){
		var s = "";
		while(idx<dv.byteLength){
			var c = dv.getUint8(idx++);
			c = String.fromCharCode(c);
			if (c == '\n')
				break;
			else if (c == '\r')
				;
			else
			s += c;
		}
		return s;
	}
	
	var vertexData;
	var indexData;
	var line;
	line = readLine();
	if (line !== "mesh_5")
		throw new Error("Bad header");
	while (true){
		line = readLine();
		if (line==""){
			break;
		}
		var lineSplit = line.split(' ');
		if (lineSplit[0] === "vertices")
			this.vertexNum = parseInt(lineSplit[1])
		else if (lineSplit[0] === "indices")
			this.indexNum = parseInt(lineSplit[1]);
		else if (lineSplit[0] === "albetoMap_file"){
			this.defaultMaterial.albetoMap = new tdl.Texture2D(loader, "art/"+lineSplit[1],{format: tdl.gl.RGB});
			}
		else if (lineSplit[0] === "reflectanceMap_file"){
			this.defaultMaterial.reflectanceMap = new tdl.Texture2D(loader, "art/"+lineSplit[1],{format: tdl.gl.RGB});
			}
		else if (lineSplit[0] === "roughnessMap_file"){
			this.defaultMaterial.roughnessMap = new tdl.Texture2D(loader, "art/"+lineSplit[1],{format: tdl.gl.LUMINANCE});
			}
		else if (lineSplit[0] === "normalMap_file"){
			this.defaultMaterial.normalMap = new tdl.Texture2D(loader, "art/"+lineSplit[1],{format: tdl.gl.RGB});
			}
		else if (lineSplit[0] === "vertex_data"){
			this.vdata = new Float32Array(ab, idx, this.vertexNum);
			idx += this.vdata.byteLength;
		}
		else if (lineSplit[0] === "index_data"){
			this.idata = new Uint16Array(ab, idx, this.indexNum);
			idx += this.idata.byteLength;
		}
		else if(lineSplit[0] === "centroid"){
			var cat = [parseFloat(lineSplit[2]),parseFloat(lineSplit[3]),parseFloat(lineSplit[4])];
			cat.push(1.0);
			this.centroids.push(cat);
		}
	}
	this.vbuff = gl.createBuffer();
	gl.bindBuffer(gl.ARRAY_BUFFER, this.vbuff);
	gl.bufferData(gl.ARRAY_BUFFER, this.vdata, gl.STATIC_DRAW);
	this.ibuff = gl.createBuffer();
	gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.ibuff);
	gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, this.idata, gl.STATIC_DRAW);	
}
Mesh.prototype.draw = function(prog){
    //prog.use();	
    gl.bindBuffer(gl.ARRAY_BUFFER,this.vbuff);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,this.ibuff);
	prog.setVertexFormat("position",3,gl.FLOAT,"texcord",2,gl.FLOAT,"vertexNormal",3,gl.FLOAT,"vertexTangent",3,gl.FLOAT);		
    gl.drawElements(gl.TRIANGLES,this.indexNum,gl.UNSIGNED_SHORT,0);	
}