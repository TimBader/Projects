"use strict";
var canvasWidth = 700;
var canvasHeight = 600;
var camera = new Camera({canvasWidth:canvasWidth, canvasHeight:canvasHeight, fov:80*3.14/180, eye:[0,10,20,1], coi:[0,0,13,1], hither:0.1, yon:1000});
camera.set([0,0,0,1],[0,0,-1,1],[0,1,0,0]);
var gl;
//var prog;
//var prog2;
var progPhase1;
var progPhase2;
var progPhaseTransparent;

var cvs;

var Mesh_Handler = new MeshHandler({"Sphere":"Sphere.mesh","WheelT":"WheelT.mesh","Test":"Test.mesh","xxxT":"xxxT.mesh","CarBody":"Car.mesh","Sword":"sword.mesh","Badge":"Badge.mesh","W":"GTRWheel.mesh","C":"GTR.mesh"});

//Will handle all the objects
var Object_Handler = new Object3dHandler();

//Will handle all the lights
var Light_Handler = new LightHandler();

var last;

var screenUnitSquare;

var emptyTexture;

var Gamepad_Input = new GamepadHandler({});
var Keyboard_Input = new KeyboardHandler();
var tmp = document.getElementsByTagName("body");
var body = tmp[0];

var FrameBuffer;

var bbprog;
var bbquad;
//var sparktex;
var treetex;
var treelocs = [];

var skyprog;
var skytex;
var skybox;

var skyIMG;
var skyIMGB;


var envImgs = [];
var envMapBlurBuffer;
var envMapBlurProg;
var secondBlurBuffer;
var copyProg;

var envUrls = ["art/xp.png","art/xn.png","art/yp.png","art/yn.png","art/zp.png","art/zn.png"];
//var envUrls = ["art/px.png","art/nx.png","art/py.png","art/ny.png","art/pz.png","art/nz.png"];

var shadowProg;
var shadowBuffer;
var shadowCamera = new Camera({canvasWidth:512, canvasHeight:512, fov:20*3.14/180, eye:[0,100,0,1], coi:[0,0,0,1], hither:0.1, yon:1000});
shadowCamera.set(tdl.mul([0.85,0.4,0.9,1.0],20),[0,0,0,1],[0,0,-1,0]);
var bEnvMap = new EnviromentMap({urls:envUrls});	

var shadowBufferSize = 512;
var shadowBufferSizeI = 1/shadowBufferSize;

var shadowBlurBuffer;
var shadowBlurProg;

var shadowOrtho = tdl.orthographic(-40,40,-40,40,shadowCamera.hither,shadowCamera.yon);

var heightMap;
		
var progHeightMap;
var progHeightMapShadow;		
		
var dummyCube;

var meow = true;

var particles = [];

var G,P;

function main(){
    cvs = document.getElementById("cvs");
	
    gl = tdl.setupWebGL(cvs,{alpha:false,stencil:true,preserveDrawingBuffer:true});   
	var tmp = gl.getExtension("WEBGL_draw_buffers");
	if(!tmp)
		throw new Error("Your browser does not support multiple frame buffer render targets");
	else
		console.log("YOU DO SUPPORT Super FBO's");
	gl.getExtension("EXT_frag_depth");
	gl.disable(gl.BLEND);
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    gl.clearColor(0,0,0,0);
	
    var progLoader = new tdl.Loader(loadingSetup);

	progPhase1 = new tdl.Program(progLoader, "vsPhase1.txt", "fsPhase1.txt");
	progPhase2 = new tdl.Program(progLoader, "vsPhase2.txt", "fsPhase2.txt");
	progPhaseTransparent = new tdl.Program(progLoader, "vsPhaseTransparent.txt", "fsPhaseTransparent.txt");
    bbprog = new tdl.Program(progLoader, "bbvs.txt", "bbfs.txt");
    skyprog = new tdl.Program(progLoader, "skyvs.txt", "skyfs.txt");
	//
	envMapBlurProg = new tdl.Program(progLoader, "vsEnvMapBlur.txt", "fsEnvMapBlur.txt");	
	//copyProg = new tdl.Program(progLoader, "mehVs.txt", "mehShader.txt");	
	shadowProg = new tdl.Program(progLoader, "shadowvs.txt", "shadowfs.txt");
	shadowBlurProg = new tdl.Program(progLoader, "vsEnvMapBlur.txt", "fsGaussBlur3.txt");
	progHeightMap = new tdl.Program(progLoader, "hmapvs.txt", "fsPhase1.txt");
	progHeightMapShadow = new tdl.Program(progLoader, "hmapvsShadow.txt", "shadowfs.txt");
	
	progLoader.finish();
	
    bbquad = new tdl.primitives.Mesh(
        tdl.primitives.createPlane( 0,0, 1,1 ),
        {
            position: {name:"a_position", number: 3},
            texCoord: {name:"a_texcoord", number: 2}
        }
    );	

	shadowBuffer = new tdl.Framebuffer(shadowBufferSize,shadowBufferSize, {format:[ [gl.RGBA,gl.FLOAT] ]});

	shadowBlurBuffer = new tdl.Framebuffer(shadowBufferSize,shadowBufferSize,{format:[ [gl.RGBA,gl.FLOAT] ]});
	
	FrameBuffer = new tdl.Framebuffer(canvasWidth, canvasHeight, { format: [ [gl.RGBA, gl.FLOAT], [gl.RGBA, gl.FLOAT], [gl.RGBA, gl.FLOAT], [gl.RGBA, gl.FLOAT]], depthtexture:true});
	
	emptyTexture = new tdl.SolidTexture([0,0,0,0.1]);
	screenUnitSquare = new UnitSquare();	
	
	
	
	last=Date.now();
} 

function loadingSetup(){
	var loader = new tdl.Loader(preprocessing);//calls that funciton when loader is done loading!
	Mesh_Handler.loadMeshes(loader);
    //treetex = new tdl.Texture2D(loader,"art/pinktree.png");
    treetex = new tdl.Texture2D(loader,"art/pinetree.png");		

	//heightMap = new Heightmap( loader, "t1.png", 200, 100, 200, new Material({albetoMap: new tdl.SolidTexture([240,240,240,255]), reflectanceMap: new tdl.SolidTexture([49,49,49,255]), roughnessMap: new tdl.SolidTexture([230,230,230,255])} ));		
    
	var mat = new Material({
	albetoMap: new tdl.ColorTexture({width:1,height:1,pixels:[240,240,240]},tdl.gl.RGB), 
	reflectanceMap: new tdl.ColorTexture({width:1,height:1,pixels:[29,29,29]},tdl.gl.RGB), 
	roughnessMap: new tdl.ColorTexture({width:1,height:1,pixels:[10]},tdl.gl.LUMINANCE)
	});
	heightMap = new Heightmap( loader, "t1d.png", 200, 20, 200, mat);	
	heightMap.load(loader);
	
	bEnvMap.loadImages(loader);
	
	Particles.load(loader);
	for(var i=0; i<200; ++i){
		particles.push( new Particles(100) );
	}	
	
	loader.finish();
}


function keydown_callback(ev){
	var found = 0;
	for (var i=0;i<Keyboard_Input.evList.length;i++)
		if (ev.keyCode === Keyboard_Input.evList[i].keyCode)
			found = 1;
	if (found === 0)
		Keyboard_Input.evList.push(ev)
}
function keyup_callback(ev){
	for (var i=0;i<Keyboard_Input.evList.length;i++)
		if (ev.keyCode === Keyboard_Input.evList[i].keyCode){
			Keyboard_Input.evList.splice(i,1);
			i--;
		}
}

function preprocessing(){	
	bEnvMap.createBuffers();
	
	bEnvMap.makeBlur(envMapBlurProg, copyProg, screenUnitSquare);
	
	skybox = new tdl.primitives.Mesh(
		tdl.primitives.createCube(30),
		{ position: "vec3 a_position", normal: "vec3 a_normal", texCoord: "vec2 a_texcoord" },
		tdl.identity(),
		{}
	);		
	
	gameInitialize();
}

function gameInitialize(){
	//This is where we can initialize some objects or things before the game starts
	Light_Handler.lights.push(new Light({pos:[0.38,1,0.12,0],color:[1,1,0.8,-2],shineDirection:[0,0,0,0],ambientDiffuseMaxPower:0.5}));
	//Light_Handler.lights.push(new Light({pos:[0.85,0.4,0.9,0],color:[1,0.6,0.4,-2],shineDirection:[0,0,0,0],ambientDiffuseMaxPower:0.34}));	
	//Light_Handler.lights.push(new Light({pos:[-10,20,1,1],color:[1,1,0.9,0]}));
	
	//Adds the list called "objects" to the dictionary
	Object_Handler.addObjectCategory("OBJECTS");
	Object_Handler.addObjectCategory("CARS");

	Object_Handler.addObject("OBJECTS", "Light0", new Object3d({pos:[20,22,0,1],size:.25,mesh:Mesh_Handler.getMesh("Sword")}));
	
	//objHandler is a handling object that contains a dictionary of lists that contain objects
	//to add a new object to one of the list, you do ObjHanderl.push Meathod
	//

	//var mat = new Material({albetoMap:new tdl.SolidTexture([240,240,240,255]),roughnessMap:new tdl.SolidTexture([255,255,255,255]),reflectanceMap:new tdl.SolidTexture([49,49,49,255])});	

	Object_Handler.addObject("CARS", "PlayerCar0", new Car({pos:[0,0,-14,1],bodyMesh:Mesh_Handler.getMesh("CarBody"),wheelMesh:Mesh_Handler.getMesh("W"),size:1,wheelSize:0.50}));
	//Object_Handler.getObject("CARS", "PlayerCar0")[0].bodyMaterial.albetoMap = new tdl.SolidTexture([209, 22, 7, 255]);
	//Object_Handler.getObject("CARS", "PlayerCar0")[0].bodyMaterial.roughnessMap = new tdl.SolidTexture([0.90*255, 0, 0, 255]);
	//Object_Handler.getObject("CARS", "PlayerCar0")[0].bodyMaterial.reflectanceMap = new tdl.SolidTexture([0.40*255, 0.40*255, 0.40*255, 255]);	
	Object_Handler.addObject("OBJECTS", "Marker0", new Object3d({pos:[30,10,30,1],mesh:Mesh_Handler.getMesh("Sphere")}));
	Object_Handler.addObject("OBJECTS", "Marker1", new Object3d({pos:[-30,19,30,1],mesh:Mesh_Handler.getMesh("Sphere")}));
	Object_Handler.addObject("OBJECTS", "Marker2", new Object3d({pos:[-100,40,-30,1],size:10,mesh:Mesh_Handler.getMesh("Sphere")}));
	Object_Handler.addObject("OBJECTS", "Marker3", new Object3d({pos:[30,23,-30,1],mesh:Mesh_Handler.getMesh("CarBody")}));
	Object_Handler.addObject("OBJECTS", "Test", new Object3d({pos:[0,25,0,1],size:20,rotAxis:[1,0,0,0],rotVel:-0.002,mesh:Mesh_Handler.getMesh("Badge")}));
	Object_Handler.addObject("OBJECTS", "Test", new Object3d({pos:[30,25,40,1],size:10,rotAxis:[0,0,1,0],rotVel:-0.12,mesh:Mesh_Handler.getMesh("W")}));

	Object_Handler.addObject("OBJECTS", "Test", new Object3d({pos:[0,20,12,1],size:5,rotAxis:[0,0,1,0],rotVel:0.002,mesh:Mesh_Handler.getMesh("Test")}));
	
	
	var mat = new Material({
	albetoMap: new tdl.ColorTexture({width:1,height:1,pixels:[240,240,240]},tdl.gl.RGB), 
	reflectanceMap: new tdl.ColorTexture({width:1,height:1,pixels:[29,29,29]},tdl.gl.RGB), 
	roughnessMap: new tdl.ColorTexture({width:1,height:1,pixels:[200]},tdl.gl.LUMINANCE)
	});
	Object_Handler.addObject("OBJECTS", "Test", new Object3d({pos:[0,-1,0,1],size:60,mesh:Mesh_Handler.getMesh("Test"),material:mat}));
	
	
	
	Object_Handler.addObject("OBJECTS", "SkySphere", new Object3d({pos:[30,30,0,1],size:5,mesh:Mesh_Handler.getMesh("Sword")}));
	//Object_Handler.addObject("OBJECTS", "SkySphere", new Object3d({pos:[30,30,0,1],size:5,mesh:Mesh_Handler.getMesh("Sword")}));
	
	//Object_Handler.addObject("OBJECTS", "SphereTest", new Object3d({pos:[10,0,0,1],size:3,mesh:Mesh_Handler.getMesh("Sphere")}));
	//Object_Handler.addObject("OBJECTS", "SphereTest", new Object3d({pos:[20,25,0,1],size:3,mesh:Mesh_Handler.getMesh("Sphere"),rotAxis:[0,1,0,0],rotVel:0.1}));	

    treelocs.push([80,10,-20],[-20,10,0]);	
	
	make_noise();
	
	update();
}

function randrange(a, b){
    var r = Math.random();
    return a + r * (b-a);
}

var next_spawn = 0;
function update(){
	//Calculating elapsed time
	var now = Date.now();
	var dtime = (now-last)/1000;
	last = Date.now();

	//Updating keyboard & GAMEPAD events
	//Keyboard_Input.update();
	body.addEventListener("keydown",keydown_callback);
	body.addEventListener("keyup",keyup_callback);	
	Gamepad_Input.update();	

	//Vectors for movement controls
	var strafeVector = [0,0,0];
	var rotateVector = [0,0,0];

	//Car Mode Controls
	/*if (Keyboard_Input.checkForKey(65) === 1)// A
		rotateVector[1] += 1;		
	if (Keyboard_Input.checkForKey(68) === 1)// D
		rotateVector[1] += -1;
	
	if (Keyboard_Input.checkForKey(87) === 1)// W
		strafeVector[2] -= 4;
	if (Keyboard_Input.checkForKey(83) === 1)// S
		strafeVector[2] += 4;	*/
	//Camera Mode Controls
	//Keyboard Strafing
	
	Object_Handler.getObject("CARS","PlayerCar0")[0].wheelRotationSpeed = 0;
	if (Keyboard_Input.checkForKey(65) === 1)// A
		strafeVector[0] += -1;		
	if (Keyboard_Input.checkForKey(68) === 1)// D
		strafeVector[0] += 1;
	if (Keyboard_Input.checkForKey(85) === 1 || Gamepad_Input.yPressed === true)// U
		strafeVector[1] += 1;	
	if (Keyboard_Input.checkForKey(79) === 1 || Gamepad_Input.bPressed === true)// O
		strafeVector[1] += -1;		
	if (Keyboard_Input.checkForKey(87) === 1){// W
		strafeVector[2] += -1;
		Object_Handler.getObject("CARS","PlayerCar0")[0].wheelRotationSpeed = -6.28;		
		}
	if (Keyboard_Input.checkForKey(83) === 1){// S
		strafeVector[2] += 1;		
		Object_Handler.getObject("CARS","PlayerCar0")[0].wheelRotationSpeed = 6.28;		
		}
	
	//Keyboard Rotation
	if (Keyboard_Input.checkForKey(74) === 1)// J
		rotateVector[1] += 1;
	if (Keyboard_Input.checkForKey(76) === 1)// L
		rotateVector[1] += -1;
	if (Keyboard_Input.checkForKey(73) === 1)// I
		rotateVector[0] += 1;
	if (Keyboard_Input.checkForKey(75) === 1)// K
		rotateVector[0] += -1;	
	if (Keyboard_Input.checkForKey(81) === 1 || Gamepad_Input.lbPressed === true)// Q
		rotateVector[2] += 1;
	if (Keyboard_Input.checkForKey(69) === 1 || Gamepad_Input.rbPressed === true)// E
		rotateVector[2] += -1;	

	
	rotateVector[1] = clamp(rotateVector[1]-1*Gamepad_Input.rtsVec[0],-1,1);
	rotateVector[0] = clamp(rotateVector[0]-1*Gamepad_Input.rtsVec[1],-1,1);

	var rOC;
	if (strafeVector[0] != 0 || strafeVector[1] != 0 || strafeVector[2] != 0){
		strafeVector[0] = clamp(strafeVector[0]+Gamepad_Input.ltsVec[0],-1,1);
		strafeVector[2] = clamp(strafeVector[2]+Gamepad_Input.ltsVec[1],-1,1);
		
		//Good strafing
		var strafeVecMag = tdl.length(strafeVector);
		if (strafeVecMag > 1.0)
			strafeVector = tdl.mul(strafeVector, 1/strafeVecMag);
		
		rOC = 8.5*dtime;
		Object_Handler.getObject("CARS", "PlayerCar0")[0].strafe(rOC*strafeVector[0],rOC*strafeVector[1],rOC*strafeVector[2]);
	}

	if (rotateVector[0] != 0 || rotateVector[1] != 0 || rotateVector[2] != 0){	
		var rotateVecMag = tdl.length(rotateVector);
		if (rotateVecMag > 1.0)
			rotateVector = tdl.mul(rotateVector, 1/rotateVecMag);
	
		rOC = (1.57)*dtime;
		Object_Handler.getObject("CARS", "PlayerCar0")[0].turn(rOC*rotateVector[1]);
		
		//Extra Camera Car rotation
		Object_Handler.getObject("CARS", "PlayerCar0")[0].tilt(rOC*rotateVector[0]);Object_Handler.getObject("CARS", "PlayerCar0")[0].roll(rOC*rotateVector[2]);
	}
	
	if (rOC != 0){
		//Getting third person camera
		camera.coi = tdl.add(Object_Handler.getObject("CARS", "PlayerCar0")[0].pos,tdl.mul(20,Object_Handler.getObject("CARS", "PlayerCar0")[0].antilook));
		camera.eye = tdl.add(Object_Handler.getObject("CARS", "PlayerCar0")[0].pos,tdl.add(tdl.mul(10,Object_Handler.getObject("CARS", "PlayerCar0")[0].look),tdl.mul(2.5,Object_Handler.getObject("CARS", "PlayerCar0")[0].up)));
		camera.up = Object_Handler.getObject("CARS", "PlayerCar0")[0].up;
		camera.computeVM();
	}
	
	//this will update all the objects at once
	Object_Handler.updateAll(dtime);
	// this will update only the objects listed under "objects" list
	//I will implement the above just in-case it is needed.  It will come soon.
	
	//var antiDir = tdl.mul(1, [0.0,1.0,0.0,0.0]);
	var carPos = Object_Handler.getObject("CARS", "PlayerCar0")[0].pos;
	var dist = 10;
	//var newCamPos = tdl.add(tdl.mul([0.85,0.4,0.9,0.0], dist),carPos);
	var newCamPos = tdl.add(tdl.mul([0.38,1,0.12,0], dist), carPos);
	
	shadowCamera.set(newCamPos, carPos, [0,0,-1,0]);
	
	next_spawn -= dtime*1000;
	
	if( next_spawn <= 0 ){
		next_spawn = 100;//randrange(500,4000);
		newParticle();
	}

    Particles.updateprog.use();
    Particles.usq.drawS0(Particles.updateprog);
    Particles.updateprog.setUniform("g",[0,-0.000005,0]);
    Particles.updateprog.setUniform("elapsed",dtime*1000);	
	for(var i=0; i<particles.length; ++i){
		particles[i].update(dtime*1000);
	}

	draw(dtime);
	//let tdl update the recall the updating
	tdl.requestAnimationFrame(update);
}

function newParticle(){
    for(var i=0; i<particles.length; ++i){
        if( particles[i].lifeleft <= 0 ){
			var p = Object_Handler.getObject("CARS", "PlayerCar0")[0].pos;
            particles[i].init( 
                [randrange(camera.coi[0]-15, camera.coi[0]+15), camera.coi[1]+25, randrange(camera.coi[2]-20,camera.coi[2]+20)], //position
                [0.9, 0.9, 0.9, 1.0] //color
                );
            break;
        }
    }
}

function draw(dtime){
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT );
	//FPS drawing
	//msg0.innerHTML = "FPS: " + parseInt(1/dtime);

	drawShadows();
	blurShadowBuffer();

	drawFirstPhase();
	drawSecondPhase();
	
	drawTransparent();

	drawBillboards();

    //gl.blendFunc(gl.SRC_ALPHA,gl.ONE);
    Particles.drawprog.use();
    camera.draw(Particles.drawprog);
    Particles.drawprog.setUniform("color", [0.9,0.9,0.9,1.0]);
    for(var i=0; i<particles.length; ++i){
        particles[i].draw(/*camera*/);
    }
    //make sure we can update the pos and vel textures on the next go-round
    Particles.drawprog.setUniform("postex", Particles.dummytex);
    Particles.drawprog.setUniform("veltex", Particles.dummytex);	
	gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);	
	
	drawSkybox();
}


function drawShadows(){
	shadowProg.use();
	shadowCamera.drawShadow(shadowProg);
	shadowProg.setUniform("projMatrix", shadowOrtho);
	shadowBuffer.bind();
	gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT );
	Object_Handler.drawShadowAll(shadowProg, false);
	progHeightMapShadow.use();
	shadowCamera.drawShadow(progHeightMapShadow);
	progHeightMapShadow.setUniform("projMatrix", shadowOrtho);
	heightMap.drawShadow(progHeightMapShadow);
	shadowBuffer.texture.setParameter(gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
	shadowBuffer.texture.setParameter(gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);	
	shadowBuffer.unbind();
}

function blurShadowBuffer(){
	shadowBlurProg.use();
	shadowBlurProg.setUniform("ISize",shadowBufferSizeI);
	shadowBlurProg.setUniform("deltas", [1,0]);
	shadowBlurProg.setUniform("image", shadowBuffer.texture);
	shadowBlurBuffer.bind();
	gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT );
	screenUnitSquare.draw(shadowBlurProg);
	shadowBlurBuffer.unbind();
	shadowBlurProg.setUniform("deltas", [0,1]);
	shadowBlurProg.setUniform("image", shadowBlurBuffer.texture);
	shadowBuffer.bind();
	gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT );
	screenUnitSquare.draw(shadowBlurProg);
	shadowBuffer.unbind();
}

function drawFirstPhase(){
	progPhase1.use();
	camera.draw(progPhase1);
	progPhase1.setUniform("noise",[0.5,0.01]);
	progPhase1.setUniform("enviromentMap",bEnvMap.nonBlurredBuffer);
	progPhase1.setUniform("enviromentMapB",bEnvMap.blurredBuffer.texture);
	progPhase1.setUniform("G",G);
	progPhase1.setUniform("P",P);
	FrameBuffer.bind();
	gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT );
	Object_Handler.drawAll(progPhase1, false);
	
	progHeightMap.use();
	camera.draw(progHeightMap);
	progHeightMap.setUniform("noise",[2.0,0.025]);	
	progHeightMap.setUniform("enviromentMap",bEnvMap.nonBlurredBuffer);
	progHeightMap.setUniform("enviromentMapB",bEnvMap.blurredBuffer.texture);
	progHeightMap.setUniform("G",G);
	progHeightMap.setUniform("P",P);
	heightMap.draw(progHeightMap);
	
	FrameBuffer.unbind();
}

function drawSecondPhase(){
	//Second render phase:	
	progPhase2.use();
	camera.drawPhase2(progPhase2);	
    gl.blendFunc(gl.ONE,gl.ONE);
    gl.enable(gl.BLEND);
	progPhase2.setUniform("posTexture", FrameBuffer.textures[0]);
	progPhase2.setUniform("normalTexture", FrameBuffer.textures[1]);
	progPhase2.setUniform("albetoTexture", FrameBuffer.textures[2]);
	progPhase2.setUniform("reflectanceTexture", FrameBuffer.textures[3]);
	progPhase2.setUniform("depth_texture", FrameBuffer.depthtexture);
	//progPhase2.setUniform("lightNum", Light_Handler.lights.length);
	//progPhase2.setUniform("light_projMatrix", shadowCamera.projectionMatrix);
	progPhase2.setUniform("light_projMatrix", shadowOrtho);	
	progPhase2.setUniform("light_viewMatrix", shadowCamera.viewMatrix);
	progPhase2.setUniform("light_hitheryon",[shadowCamera.hither, shadowCamera.yon-shadowCamera.hither]);
	progPhase2.setUniform("shadowBuffer", shadowBuffer.texture);
	//Drawing once for every light and blending the result together for final image
	Light_Handler.drawLightsPhase2(progPhase2, screenUnitSquare);
	//progPhase2.setUniform("ambientColor", [0.3,0.3,0.3]);
	//emptying all other FBOs textures
    gl.disable(gl.BLEND);
	progPhase2.setUniform("posTexture", emptyTexture);
	progPhase2.setUniform("normalTexture", emptyTexture);
	progPhase2.setUniform("albetoTexture", emptyTexture);
	progPhase2.setUniform("reflectanceTexture", emptyTexture);
	progPhase2.setUniform("depth_texture", emptyTexture);
	progPhase2.setUniform("shadowBuffer", emptyTexture);
 }
 
function drawTransparent(){
	//Third render phase for transparent objects:
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);
    progPhaseTransparent.use();
	Light_Handler.lights[0].draw(progPhaseTransparent);
	camera.draw(progPhaseTransparent);
	progPhaseTransparent.setUniform("enviromentMap",bEnvMap.blurredBuffer.texture);
	gl.colorMask(0,0,0,0);
	Object_Handler.drawAll(progPhaseTransparent, true);
	//heightMap.draw();
	gl.colorMask(true,true,true,true);
	Object_Handler.drawAll(progPhaseTransparent, true);
	gl.disable(gl.BLEND);
}
 
function drawSkybox(){
    skyprog.use();
    camera.draw(skyprog);
	skyprog.setUniform("basetexture", bEnvMap.nonBlurredBuffer);
    skyprog.setUniform("worldMatrix", tdl.scaling(20,20,20));
    skybox.draw(skyprog);
}

function drawBillboards(){
	//Billboards
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);
    bbprog.use();
    camera.draw(bbprog);
	gl.colorMask(0,0,0,0);
    bbprog.setUniform("texture",treetex);
    for(var i=0;i<treelocs.length;++i){
        bbprog.setUniform("translation",treelocs[i]);
        bbquad.draw(bbprog);
    }
	gl.colorMask(true,true,true,true);
    for(var i=0;i<treelocs.length;++i){
        bbprog.setUniform("translation",treelocs[i]);
        bbquad.draw(bbprog);
    }
	gl.disable(gl.BLEND);
 }
 
 function make_noise(){
    //var G,P;
    var gg = new Uint8Array(256*4);
    var g = [];
    
    var ctr=0;
    for(var i=0;i<256;++i){
        var v = [Math.random()-0.5,Math.random()-0.5,Math.random()-0.5,0.0];
        var len = Math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]);
        if( len === 0.0 ){
            --i;
            continue;
        }
        v[0] /= len;
        v[1] /= len;
        v[2] /= len;
        g.push( v[0],v[1],v[2] );
        gg[ctr++] = Math.floor((v[0]+1.0)*255);
        gg[ctr++] = Math.floor((v[1]+1.0)*255);
        gg[ctr++] = Math.floor((v[2]+1.0)*255);
        gg[ctr++] = 128;
    }
        
    G = new tdl.ColorTexture({width:256,height:1,pixels:gg});

    var pp = new Uint8Array(256);
    for(var i=0;i<256;++i){
        pp[i]=i;
    }
	pp = shuffle(pp)
    
    P = new tdl.ColorTexture({width:256,height:1,pixels:pp,format:gl.LUMINANCE});
}
function shuffle(array){
	var m = array.length, t,i;
	while(m){
		i = Math.floor(Math.random()* m--);
		t = array[m];
		array[m] = array[i];
		array[i] = t;
	}
return array;
}
