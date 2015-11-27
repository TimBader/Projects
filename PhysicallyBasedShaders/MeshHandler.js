function MeshHandler(meshDict){
	this.meshDict = meshDict;
}

MeshHandler.prototype.addMesh = function(meshName, path){
	//adds the path name of the mesh to be loaded later at anouther date
	this.meshDict[MeshName] = path;
}

MeshHandler.prototype.removeMesh = function(meshName){
	//Removes mesh from the dictionary
	delete this.meshDict[meshName];
}

MeshHandler.prototype.loadMeshes = function(loader){
	//loads all meshes if they haven't been converted from path into Mesh Object
		for (var i in this.meshDict){
			if (typeof this.meshDict[i] == "string"){
				this.meshDict[i] = new Mesh(loader, this.meshDict[i]);
			}
		}
}

MeshHandler.prototype.getMesh = function(meshName){
	//returns given mesh name if it is loaded aka. not a string path still
	if (typeof this.meshDict[meshName] != "string")
		return this.meshDict[meshName];
	throw new Error("The attempted loading of the mesh named: " + meshName + " has not been converted to a mesh yet");	
}

MeshHandler.prototype.loadMesh = function(meshName, loader){
	//Loads given the given mesh assuming that the mesh hasn't loaded yet
	if (typeof this.meshDict[meshName] == "string")
		this.meshDict[meshName] = new Mesh(loader, this.meshDict[meshName]);
	else
		throw new Error("Attempting to load a mesh without a proper string path");

}