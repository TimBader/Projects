"use strict";
//Tim Bader
var fs = require("fs");

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
	var r_ = VectorSubVector(r,q);
	var s_ = VectorSubVector(s,q);
	var rtex_ = VectorSubVector(rtex,qtex);
	var stex_ = VectorSubVector(stex,qtex);
	if (rtex_[0]*stex_[1]-stex_[0]*rtex_[1] == 0){
		console.log("Warning!, Bad Texture Coordinates!");
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
var vertexData = [];
var textureData = [];
var vertexNormalData = [];
var faceData = [];
var triangles = [];

var objCentList = [];
var currObj = -1;

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
		if (lineSplited.length<4){
			throw new Error("YO! You don't have at least three vertices listed");
		}
		/*if (lineSplited.length > 5){
			throw new Error("This converter can only handle quads and triangles, please use editing software to convert polygons to tris or quads");		
		}*/
		var pointList = [];
		for (var c=1;c<lineSplited.length;c++){
			pointList.push(lineSplited[c]);
		}
		var iterator = 1; //Gonna start at the second index
		//a 1,2,3,4,5 polygon tessalates into 1,2,3 & 1,3,4 & 1,4,5 polygons
		//Getting first value(s) since we need it always
		var firstTmp = pointList[0].split("/");
		var firstV = parseInt(firstTmp[0],10)-1;
		if (textureData.length != 0)
			var firstVT = parseInt(firstTmp[1],10)-1;
		if (vertexNormalData.length != 0)
			var firstVN = parseInt(firstTmp[2],10)-1;
		while (true){
			//adding first value(s) to the thing
			var t = [];
			//console.log(firstV);
			t.push(firstV);
			if (textureData.length != 0)
				t.push(firstVT);
			if (vertexNormalData.length != 0)
				t.push(firstVN);
			//now for the rest of the indexes
			for (var o=0;o<2;o++){
				//console.log(pointList[iterator+i]);
				//console.log("Poop: " + iterator + i);
				tmp = pointList[iterator+o].split("/"); //Split it again to seperate vertex Index and texture index
				t.push(parseInt(tmp[0],10)-1);
				if (textureData.length != 0)
					t.push(parseInt(tmp[1],10)-1);
				if (vertexNormalData.length != 0){
					t.push(parseInt(tmp[2],10)-1);
					//console.log(tmp[2]);
					}
			}
			//console.log(t);
			triangles.push(t);
			//break;
			//console.log(iterator);
			if (iterator == pointList.length-2){
				//console.log("KITTY CATZ MEOW FACE YAY!!!!");
				break;
			}
			iterator++;
		}
	}
}
/*
var tmp = pointList[where].split("/"); //Split it again to seperate vertex Index and texture index
t.push(parseInt(tmp[0],10)-1);
if (textureData.length != 0)
	t.push(parseInt(tmp[1],10)-1);
if (vertexNormalData.length != 0)
	t.push(parseInt(tmp[2],10)-1);*/

console.log("TEXLENGTH: " + textureData.length);
console.log("VERTEXLENGTH: " + vertexData.length);	
if (textureData.length === 0)
	console.log("!!!Warning!!! Texture Data Length is 0.  Creating default texture cords with default texture");
if (vertexNormalData.length === 0)
	console.log("!!!Warning!!! Vertex Normal Data Length is 0.  Creating vertex normal data based on the triangle's face's normal");
	
console.log("TRIANGLES BEFORE: " + triangles.length);	
	
var vmap = {};
var vNum = 0;
var vData = [];
var missingVertexNormalNum = 0;
for (var i=0;i<triangles.length;i++){
	var T = triangles[i];
	//console.log("T: " + T);
	var missingData = false;
	if (T.length != 9)
		missingData = true;
		
	var jumpMul = 3;//How many times thing will need to jump due to missing parts
	
	var missingNormalData = false;
	var missingTextureData = false;
	if (missingData == true){
//		if (vertexNormalData.length === vNum/3){
		if (vertexNormalData.length-missingVertexNormalNum === 0){//if there are no normals listed in the thing
			missingNormalData = true;
			var r = T.length/3;
			//console.log(vertexData[T[0*r]][0]);
			var a = [vertexData[T[0*r]][0],vertexData[T[0*r]][1],vertexData[T[0*r]][2]];//Time to start making our own normal based off the normal of the face
			var b = [vertexData[T[1*r]][0],vertexData[T[1*r]][1],vertexData[T[1*r]][2]];
			var c = [vertexData[T[2*r]][0],vertexData[T[2*r]][1],vertexData[T[2*r]][2]];
			var vn = VectorNormalize(VectorCross(VectorSub(b,a), VectorSub(c,a)));
			vertexNormalData.push(vn);
			jumpMul--; 
		}
		
		if (textureData.length === 1 || textureData.length === 0){//if there is only 0-2 texture points in the mesh then it isnt a mesh and would never get this far
			var missingTextureData = true;
			jumpMul--;
			if (textureData.length === 0){
				textureData.push([0,0]);
			}
		}
	}

	//-!!!!!WARNING!!!!:Very confusing programming logic trade off AHEAD!
	//Static: this will not change no matter the coming circumstances
	//HStatic: this will be static half the time and will only change on one given condition
	//QStatic: this will be static only on one given occasion
	for (var j=0;j<3;j++){//loop through the triangle's points
		//v Also jumpMul === 3... might use that instead for efficiency
		if (missingTextureData === true && missingNormalData === true){//Check to see if both are missing
			vertexIndex = T[j]; //only 'j' because there is only vertex information in the triangle info
			var textureIndex = 0;//Zero cuz it needs nothing other than zero
			var normalIndex = missingVertexNormalNum;
			//missingVertexNormalNum++;//increment the number of missing vertexes for next go-around
		}
		else{//if not both missing
			var jjmul = j*jumpMul//small optimization also a testimate to John Mullets father... i guess in some small way
/*Static*/	var vertexIndex = T[jjmul];//This is static and will not change and it is set so it already knows how many jumps to make
/*HStatic*/ var textureIndex = T[jjmul+1];//Will change if there is any missing textures, if NOT then it already knows how many jumps to make
/*QStatic*/	var normalIndex = T[jjmul+2];//Will not change if there is no element missing missing, if not then it will always change
			if (missingTextureData === true){
				textureIndex = 0;//Zero cuz it needs nothing other than zero
				normalIndex = T[jjmul+1];//Set normalIndex one less than described previously
			}
			else if (missingNormalData === true){//if it is not textureData then it could be the normal data
				normalIndex = missingVertexNormalNum;
				//missingVertexNormalNum++;//increment the number of missing vertexes for next go-around
			}
			//If not either of those conditions then nothing is missing and everything is set as it is spose to be
		}
		var key = vertexIndex + "," + textureIndex + "," + normalIndex;//To see if there is any new key that needs to be generated
		if (vmap[key] === undefined){ //So if there is not already the same key in place make a new key/item
			vmap[key] = vNum;	
			vData.push(vertexData[vertexIndex][0],vertexData[vertexIndex][1],vertexData[vertexIndex][2], //3d for draw coordinates
			textureData[textureIndex][0],textureData[textureIndex][1],
			vertexNormalData[normalIndex][0],vertexNormalData[normalIndex][1],vertexNormalData[normalIndex][2],
			0.0,0.0,0.0); //2d for texture coordinates
			vNum++;
		}
		faceData.push(vmap[key]);	
	}
	if (missingNormalData === true)
		missingVertexNormalNum++;
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
		
console.log("TRIANGLES AFTER: " + vNum/3);			

var fname = '';
for (var i=0;i<infile.length-4;i++)
	fname = fname + infile[i];
var ofp = new Writer(fname+".mesh");
ofp.write("mesh_5\n");
ofp.write("vertices "+vData.length+"\n");
ofp.write("indices "+faceData.length+"\n");

//console.log(currmtl);
console.log(currmtl);
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



