"use strict";

//Tim Bader

//node Desktop/Lab7Graphics/objConverter.js Desktop/Lab7Graphics/spaceship2.obj


//
// Code From TDL so i can do operations in here
function VectorSubVector(a, b) {
  var r = [];
  var aLength = a.length;
  for (var i = 0; i < aLength; ++i)
    r[i] = a[i] - b[i];
  return r;
};
function VectorSub(a,b){
    if( a.length === b.length && (a.length === 3 || a.length === 4 ) )
        return VectorSubVector(a,b);
    console.trace();
    throw(new Error("Cannot subtract things of size "+a.length+" and "+b.length));
};
function VectorCross(a, b) {
  return [a[1] * b[2] - a[2] * b[1],
          a[2] * b[0] - a[0] * b[2],
          a[0] * b[1] - a[1] * b[0]];
};
function VectorNormalize(a) {
  var r = [];
  var n = 0.0;
  var aLength = a.length;
  for (var i = 0; i < aLength; ++i)
    n += a[i] * a[i];
  n = Math.sqrt(n);
  if (n > 0.00001) {
    for (var i = 0; i < aLength; ++i)
      r[i] = a[i] / n;
  } else {
    r = [0,0,0];
  }
  return r;
};	
// End of tdl objects
//

function computeTangent(q, r, s, qtex, rtex, stex){
	//q = vertex1.xyz, r = vertex2.xyz, s = vertex3.xyz;
	//qtex = vertex1.st, rtex = vertex2.st, stex = vertex3.st;
	var did = false;
	var r_ = VectorSubVector(r,q);
	var s_ = VectorSubVector(s,q);
	var rtex_ = VectorSubVector(rtex,qtex);
	var stex_ = VectorSubVector(stex,qtex);
	if (rtex_[0]*stex_[1]-stex_[0]*rtex_[1] == 0){
		throw new Error("Bad Texture Coordinates, Unable to make suitable tangent vectors for bumpmapping");
		tmp = 1.0;
	}
	else{
		var tmp = 1.0/(rtex_[0]*stex_[1]-stex_[0]*rtex_[1]);
	}
	var R00 = tmp*stex_[1];
	var R01 = tmp*-1*rtex_[1];
	var Tangent = [
		R00*r_[0]+R01*s_[0],
		R00*r_[1]+R01*s_[1],
		R00*r_[2]+R01*s_[2]
	];
	return Tangent;
}


var fs = require("fs");
function Writer(fname){
	this.stream = fs.createWriteStream(fname);
	this.offset = 0;
}

Writer.prototype.write = function(x){
	this.stream.write(x);
	this.offset += x.length;
}

Writer.prototype.end = function(){
	this.stream.end();
}

Writer.prototype.tell = function(){
	return this.offset;
}

var infile = process.argv[2];
var objdata = fs.readFileSync(infile,{encoding:"utf8"});
objdata = objdata.split("\n");
//console.log(objdata);
var vertexData = [];
var textureData = [];
var vertexNormalData = [];
var faceData = [];
var triangles = [];

var objCentList = [["DefualtMeow",0,0,0,0]];
var currObj = 0;

var mdict = {};
var currmtl;
var vertexNum = 0;
var COUNT = 0;
var cc = 0;

for (var i=0;i<objdata.length;i++){
	var lineSplited = objdata[i].split(' ');
	if (lineSplited[0] === "o" || lineSplited[0] === "g"){
		currObj++;
		objCentList.push([lineSplited[1],0,0,0,0]);
	}
	else if (lineSplited[0] === "mtllib"){
		var ML = fs.readFileSync(lineSplited[1],{encoding:"utf8"});
		ML = ML.split(/[\n\r]+/);//Regular expression for splitting. Syntax "/[" plus stuff you wan to remeove plus "]+/"
		var mname;
		for (var ii=0;ii<ML.length;ii++){
			var tmp = ML[ii].split(" ");
			//console.log("tmp: " + tmp)
			if (tmp[0] === "newmtl"){
				mname = tmp[1];
				console.log("Setting " + mname);
				mdict[mname] = {};
			}
			else if (tmp[0] === "map_Kd"){
				mdict[mname].map_Kd = tmp[1];
				console.log("AlbetoMapFound: " + mname);
			}
			else if (tmp[0] === "map_Ns"){
				mdict[mname].map_Ns = tmp[1];
				console.log("ReflectanceMapFound: " + mname);
			}
			else if (tmp[0] === "map_Ke"){
				mdict[mname].map_Ke = tmp[1];
				console.log("RoughnessMapFound: " + mname);
			}
			else if (tmp[0] === "map_Bump"){
				mdict[mname].map_Bump = tmp[1];
				console.log("normalMapFound: " + mname);
			}
		}	
	}
		
	else if (lineSplited[0]==='usemtl'){
		currmtl = lineSplited[1];
		}
	
	else if (lineSplited[0]==='v'){
		var vList = [];
		for (var ii=1;ii<lineSplited.length;ii++){
			vList.push(parseFloat(lineSplited[ii]));
			objCentList[currObj][ii] += parseFloat(lineSplited[ii]);
		}
		objCentList[currObj][4]++;
		vertexData.push(vList);
	}
	
	else if (lineSplited[0]==='vn'){
		var vnList = [];
		for (var ii=1;ii<lineSplited.length;ii++){
			vnList.push(parseFloat(lineSplited[ii]));
		}
		vertexNormalData.push(vnList);
	}
	
	else if (lineSplited[0]==='vt'){
		var vtList = [];
		for (var ii=1;ii<lineSplited.length;ii++){
			vtList.push(parseFloat(lineSplited[ii]));
		}
		textureData.push(vtList);
	}
	
	else if (lineSplited[0]==='f'){
		//console.log("doing face stuff!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		if (lineSplited.length != 4){
			throw new Error("-!!!FAILURE!!! The imported .obj file MUST be Triangulated!");
		}
		var t=[];
		for (var c=1;c<4;c++){
			var tmp = lineSplited[c].split("/"); //Split it again to seperate vertex Index and texture index
			var vi = parseInt(tmp[0],10)-1;
			var ti = tmp[1]; //Check to see if the iSplited got something back
			var vni = tmp[2];			
			if (tmp.length != 3 || ti.length === 0 || vni.length === 0){
				throw new Error("-!!!FAILURE!!! The imported .obj file MUST have Texture Coordinates AND Vertex Normals");
			}
			ti = parseInt(ti,10)-1;
			vni = parseInt(vni,10)-1;
			t.push(vi,ti,vni);
		}
		triangles.push(t);
		}
	}
	
console.log("Successfully Parsed!");
console.log("VERTEX_NUMBER: " + vertexData.length);	
console.log("TEXTURE_NUMBER: " + textureData.length);
console.log("VERTEXNORMAL_NUMBER: " + vertexNormalData.length);
console.log("TRIANGLE_NUMBER: " + triangles.length);
	
var vmap = {};
var vNum = 0;
var vData = [];
for (var i=0;i<triangles.length;i++){
	//console.log(T);
	var T = triangles[i];
	for (var j=0;j<3;j++){
		//console.log("CATX");
		var j2 = j*3;
		var vi = T[j2];
		var ti = T[j2+1];
		var vni = T[j2+2];
		var key = vi + "," + ti + "," + vni;
		if (vmap[key] === undefined){ //So if there is not already the same key in place make a new key/item
			vmap[key] = vNum;
			//console.log(vertexData.length);
			//console.log(vi);
			//console.log(vertexData[vi][0]);
			vData.push(vertexData[vi][0],vertexData[vi][1],vertexData[vi][2], //3d for draw coordinates
			textureData[ti][0],textureData[ti][1],
			//0,0,0);
			vertexNormalData[vni][0],vertexNormalData[vni][1],vertexNormalData[vni][2],
			0.0,0.0,0.0); //extra for tangents
			vNum++;
		}
		faceData.push(vmap[key]);
	}
}


//Computing NormalPoints
for (var ti=0;ti<faceData.length;ti+=3){
	var qi = faceData[ti];
	var ri = faceData[ti+1];
	var si = faceData[ti+2];
	var q = [vData[qi*11], vData[qi*11+1], vData[qi*11+2]];
	var r = [vData[ri*11], vData[ri*11+1], vData[ri*11+2]];
	var s =	[vData[si*11], vData[si*11+1], vData[si*11+2]];
	var qtex = [vData[qi*11+3], vData[qi*11+4]];
	var rtex = [vData[ri*11+3], vData[ri*11+4]];
	var stex = [vData[si*11+3], vData[si*11+4]];
	
	//some limitations if texture cords our
	var tangent;
	if (qtex[0] == 0 && qtex[1] == 0){
		qtex[0] = 1;qtex[1] = 0
		tangent = [1.0,0.0,0.0];
		}
	else if (rtex[0] == 0 && rtex[1] == 0){
		rtex[0] = 1;rtex[1] = 0
		tangent = [1.0,0.0,0.0];
		}
	else if (stex[0] == 0 && stex[1] == 0){
		stex[0] = 1;stex[1] = 0
		tangent = [1.0,0.0,0.0];
		}
	else{
		tangent = computeTangent(q, r, s, qtex, rtex, stex);}
		
	tangent = VectorNormalize(tangent);
	//console.log(tangent);
	for (var tmp = 0; tmp < 3; tmp++){
		vData[qi*11+8+tmp] += tangent[tmp];
		vData[ri*11+8+tmp] += tangent[tmp];
		vData[si*11+8+tmp] += tangent[tmp];
	}
}

console.log("TRIANGLES_AFTER: " + vData.length/11);

//console.log(vertexNum);
//console.log(vertexData);
var fname = '';
for (var i=0;i<infile.length-4;i++)
	fname = fname + infile[i];
var ofp = new Writer(fname+".mesh");
ofp.write("mesh_5\n");
ofp.write("vertices "+vData.length+"\n");
//console.log(vData.length)
//for (var i = 0;i<5;i++)
//	console.log(vData[i]);
ofp.write("indices "+faceData.length+"\n");

//console.log(currmtl);
console.log(mdict);
if (mdict[currmtl].map_Kd !== undefined)
	ofp.write("albetoMap_file " + mdict[currmtl].map_Kd + "\n");
if (mdict[currmtl].map_Ns !== undefined)
	ofp.write("reflecatnceMap_file " + mdict[currmtl].map_Ns + "\n");
if (mdict[currmtl].map_Ke !== undefined)
	ofp.write("roughnessMap_file " + mdict[currmtl].map_Ke + "\n");
if (mdict[currmtl].map_Bump !== undefined)
	ofp.write("normalMap_file " + mdict[currmtl].map_Bump + "\n");

for (var i=0;i<objCentList.length;i++){
	ofp.write("centroid " + objCentList[i][0]);
	for (var j=1;j<4;j++){
		ofp.write(" ");
		var a = objCentList[i][j]/objCentList[i][4];
		ofp.write(""+a+"");
	}
	ofp.write("\n");
}	
	
ofp.write("vertex_data");
while((ofp.tell()+1)%4 !== 0)
	ofp.write(" ");
ofp.write("\n");

var b = new Buffer(vData.length*4);
for (var i=0;i<vData.length;i++){
	b.writeFloatLE(vData[i], i*4);
	}
ofp.write(b)

ofp.write("index_data");
while((ofp.tell()+1)%4 !== 0)
	ofp.write(" ");
ofp.write("\n");

var b = new Buffer(faceData.length*4);
for (var i=0;i<faceData.length;i++)
	b.writeUInt16LE(faceData[i], i*2);
ofp.write(b)
ofp.end();

console.log("Conversion Successful!");

/*for (var i=0;i<objCentList.length;i++)
	for (var j=0;j<objCentList[i].length;j++){
		//console.log("\n");
		console.log(objCentList[i][j]);
	}*/
//console.log(ofp.tell());



