"use strict";

function GamePad();
	this.ltsxAxis = 0;
	this.ltsyAxis = 0;
	this.rtsxAxis = 0;
	this.rtsyAxis = 0;
	this.lbPressed = false;
	this.rbPressed = false;
	this.aPressed = false;
	this.rtsPressed = false;
	this.selectPressed = false;
	this.selectAlreadyPressed = false;
	this.gamepad;
	
GamePad.prototype.getCurrentGamePad();
	var gamepads = navigator.getGamepads();
	this.gamepad;
	if (gamepads){
		for (var i=0;i<gamepads.length;i++){
			if (gamepads[i]){
				this.gamepad = gamepads[i];
				break;
			}
		}
	}