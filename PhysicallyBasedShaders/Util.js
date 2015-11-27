function getSomething(xAxis, yAxis){
	var xC = xAxis;var yC = yAxis;
	if (xAxis < 0) xAxis*=-1;
	if (yAxis < 0) yAxis*=-1;
	if (yAxis != 0) var xRatio = xAxis/yAxis;
	else var xRatio = 1;
	if (xAxis != 0) var yRatio = yAxis/xAxis;
	else var yRatio = 1;
	var vec = tdl.normalize([xRatio,yRatio]);
	return [clampAndRatio(xC, 0.2*(vec[0]/xAxis)),clampAndRatio(yC, 0.2*(vec[1]/yAxis))];
	}

function boundIndices(list,r){
	for (var i=0;i<list.length;i++){
		console.log("s: "+list[i]);
		console.log("r: "+r);
		if (list[i] !== 0)
			if (list[i] > 0)
				if (list[i] - r < 0)
					list[i] = 0;
				else
					list[i] -= r;
			else
				if (list[i] + r > 0)
					list[i] = 0;
				else
					list[i] += r;
		console.log("e: "+list[i])
		}
	return list;
}

function clampAndRatio(axis, min){
	var antiMin = 1-min;
	if (axis < -min)
		axis = (axis+min)/antiMin;
	else if (axis > min)
		axis = (axis-min)/antiMin;
	else
		axis = 0;
	return axis;
}

function clamp(num, low, high){
	if (num < low)
		return low;
	if (num > high)
		return high ;
	return num;
}