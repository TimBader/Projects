"use strict";

function Object3dHandler(){
	this.objectDictionary = {};	
}

Object3dHandler.prototype.addObjectCategory = function(objectCategoryName){
	this.objectDictionary[objectCategoryName] = {};
}
Object3dHandler.prototype.addObject = function(objectCategoryName,objectName,object){
	if (this.objectDictionary[objectCategoryName] == undefined)
		this.addObjectCategory(objectCategoryName);
	if (this.objectDictionary[objectCategoryName][objectName] == undefined)
		this.objectDictionary[objectCategoryName][objectName] = [];
	this.objectDictionary[objectCategoryName][objectName].push(object);
}

Object3dHandler.prototype.getObject = function(objectCategoryName,objectName){
	return this.objectDictionary[objectCategoryName][objectName];
}

//Draw
Object3dHandler.prototype.drawObject = function(objectCategoryName,objectName,prog,drawTransparent){
	for (var i = 0;i<this.objectDictionary[objectCategoryName][objectName].length;i++)
		if (drawTransparent == this.objectDictionary[objectCategoryName][objectName][i].transparent)
			this.objectDictionary[objectCategoryName][objectName][i].draw(prog);
}

Object3dHandler.prototype.drawCategory = function(objectCategoryName,prog,drawTransparent){
	for (var key in this.objectDictionary[objectCategoryName]){
		if (this.objectDictionary[objectCategoryName].hasOwnProperty(key)){
			this.drawObject(objectCategoryName,key,prog,drawTransparent);
		}
	}
}

Object3dHandler.prototype.drawAll = function(prog,drawTransparent){
	for (var key in this.objectDictionary){
		if (this.objectDictionary.hasOwnProperty(key)){
			this.drawCategory(key,prog,drawTransparent);
		}
	}
}

//Updating
Object3dHandler.prototype.updateObject = function(objectCategoryName, objectName, elapsed){
	for (var i = 0;i<this.objectDictionary[objectCategoryName][objectName].length;i++){
		this.objectDictionary[objectCategoryName][objectName][i].update(elapsed);
		if (this.objectDictionary[objectCategoryName][objectName][i].deleteMe === true){
			this.objectDictionary[objectCategoryName][objectName].splice(i,1);
			i--;	
		}
	}
}

Object3dHandler.prototype.updateCategory = function(objectCategoryName, elapsed){
	for (var key in this.objectDictionary[objectCategoryName]){
		if (this.objectDictionary[objectCategoryName].hasOwnProperty(key)){
			this.updateObject(objectCategoryName,key, elapsed);
		}
	}
}

Object3dHandler.prototype.updateAll = function(elapsed){
	for (var key in this.objectDictionary){
		if (this.objectDictionary.hasOwnProperty(key)){
			this.updateCategory(key, elapsed);
		}
	}
}

//Shadow Drawing
Object3dHandler.prototype.drawShadowObject = function(objectCategoryName,objectName,prog,drawTransparent){
	for (var i = 0;i<this.objectDictionary[objectCategoryName][objectName].length;i++)
		if (drawTransparent == this.objectDictionary[objectCategoryName][objectName][i].transparent)
			this.objectDictionary[objectCategoryName][objectName][i].drawShadow(prog);
}

Object3dHandler.prototype.drawShadowCategory = function(objectCategoryName,prog,drawTransparent){
	for (var key in this.objectDictionary[objectCategoryName]){
		if (this.objectDictionary[objectCategoryName].hasOwnProperty(key)){
			this.drawShadowObject(objectCategoryName,key,prog,drawTransparent);
		}
	}
}

Object3dHandler.prototype.drawShadowAll = function(prog,drawTransparent){
	for (var key in this.objectDictionary){
		if (this.objectDictionary.hasOwnProperty(key)){
			this.drawShadowCategory(key,prog,drawTransparent);
		}
	}
}

/*
object3dHandler.prototype.push = function(listName, thing){
	for (var i=0;i<this.listNames.length;i++){
		if (this.listNames[i] == listName){
			this.lists[i].push(thing);
			break;
		}
	}
	if (this.dicts[listName][thingName] == undefined){
		this.dicts[listName][thingName] = [thing];
	else
		this.dicts[listName][thingName].push(thing);
	}
}
object3dHandler.prototype.draw = function(prog, transparent){
//transparent = -1:noTransperent, 1:onlyTransparent, else:both
	for (var i=0;i<this.lists.length;i++){
		for (var j=0;j<this.lists[i].length;j++){
			if (transparent === -1){
				if (this.lists[i][j].transparent === false)
					this.lists[i][j].draw(prog);}
			else if (transparent === 1){
				if (this.lists[i][j].transparent === true)
					this.lists[i][j].draw(prog);}
			else
				this.lists[i][j].draw(prog);
		}
	}
}

object3dHandler.prototype.drawAllWithTransparency = function(prog){
	this.draw(prog, -1);//Draw all non-transparent
	
	gl.blendFuncSeparate(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA, gl.ONE, gl.ONE);
	gl.colorMask(false,false,false,false);
	gl.disable(gl.BLEND);
	this.draw(prog, 1);//Draw all transparent
	gl.colorMask(true,true,true,true);
	gl.enable(gl.BLEND);

	this.draw(prog, 1);//""Yep again for some reason but we need it
}

object3dHandler.prototype.updateAll = function(elapsed, checkForDelete){
	for (var i=0;i<this.lists.length;i++){
		for (var j=0;j<this.lists[i].length;j++){
			this.lists[i][j].update(elapsed);
			if (checkForDelete === true)
				if (this.lists[i][j].deleteMe === true){
					this.lists[i].splice(j,1);
					j--;
				}
		}
	}
}
*/