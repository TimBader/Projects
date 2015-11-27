"use strict";

function GamepadHandler(opts){
	this.axisDeadZone = (opts.axisDeadZone !== undefined) ? opts.axisDeadZone : 0.2;

	this.aPressed = false;
	this.bPressed = false;
	this.yPressed = false;	
	this.xPressed = false;	
	
	this.ltsVec = [0,0];
	this.rtsVec = [0,0];
	
	this.lbPressed = false;
	this.rbPressed = false;
	
	this.rtsPressed = false;
	this.ltsPressed = false;
	
	this.rtPressed = false;
	this.ltPressed = false;
	
	this.selectPressed = false;
	this.startPressed = false;
	
	this.gamepad = undefined;
	
	//var selectAlreadyPressed = false;
	//var rTriggerPressed = false;
}

GamepadHandler.prototype.update = function(){
	var gamepads = navigator.getGamepads();
	this.gamepad = undefined;
	if (gamepads)
		for (var i=0;i<gamepads.length;i++){
			if (gamepads[i]){
				this.gamepad = gamepads[i];
				break;
			}
		}
	if (this.gamepad != undefined){
		this.ltsVec = getSomething(this.gamepad.axes[0],this.gamepad.axes[1]);
		this.rtsVec = getSomething(this.gamepad.axes[2],this.gamepad.axes[3]);
	
		if (this.gamepad.buttons.length != 0){
			//console.log("Meow");
			this.aPressed = this.gamepad.buttons[0].pressed;
			this.bPressed = this.gamepad.buttons[1].pressed;
			this.xPressed = this.gamepad.buttons[2].pressed;
			this.yPressed = this.gamepad.buttons[3].pressed;
			
			this.lbPressed = this.gamepad.buttons[4].pressed;
			this.rbPressed = this.gamepad.buttons[5].pressed;
			
			this.ltPressed = this.gamepad.buttons[6].pressed;			
			this.rtPressed = this.gamepad.buttons[7].pressed;			
			
			this.selectPressed = this.gamepad.buttons[8].pressed;
			this.startPressed = false;
			
			this.ltsPressed = this.gamepad.buttons[10].pressed;
			this.rtsPressed = this.gamepad.buttons[11].pressed;
		}
	}
}