	
//Dateiweite Definitionen
var chartWidth = 600;
var chartHeight = 400;
var radius = 20;
var countOverlays = 0;
var mapOverlay = false;
var cannonOverlay = false;
var projektilOverlay = false;
var map = false;

//Overlay ist Singleton
// --> Wird 1 einziges mal beim laden der Seite gerufen (onLoad-Event)
function createOverlay() {
	if(countOverlays == 1) return;	
	countOverlays++;	

	var overlay1;
	var overlay2;
	var overlay3;
	
	require(["dojox/gfx","dojo/domReady!"], function(gfx){
		overlay1 = gfx.createSurface("mapOverlay", chartWidth, chartHeight);
		overlay2 = gfx.createSurface("cannonOverlay",chartWidth,chartHeight);
		overlay3 = gfx.createSurface("projektilOverlay",chartWidth,chartHeight);
		mapOverlay = overlay1;
		cannonOverlay = overlay2;
		projektilOverlay = overlay3;
	});
	
	setupColors();	
	addLogLine("Hey there! To play TankCommander simply press 'Start Game' and have fun ;-)",green.Full,"logList");
}

function transformHeights(JSONObject){
	var r = [];
	var o = {};
	//Startpunkt (0,0)
	o.x=0;o.y=0;
	r.push(o);
	
	for(var i = 0; i < JSONObject.length; i++){
		o = JSONObject[i];
		j = {};
		j.x = o.x;
		j.y = chartHeight-o.y;
		r.push(j);
	}
	
	//Endpunkt (600,0)
	o.x=chartWidth;o.y=0;
	r.push(o);
	return r;
}

function getPoints(heights,interpolatedPoint){
	var ax = new Array(0,chartWidth);
	for(var i = 0; i < heights.length; i++){
		if(heights[i].x <= interpolatedPoint)
			ax[0] = i;
		if(heights[i].x >= interpolatedPoint){
			ax[1] = i;
			break;
		}
	}	
	return ax;
}

function drawClouds(heights,count){

	
	var polyPointsWolke = 20;
	for(var i = 0; i < count ; i++){
		var dyWolke = Math.floor(Math.random() * 20) + 5;
		var cx = Math.floor(Math.random() * chartWidth) + 0;
		var ax = getPoints(heights,cx);
		//Die höhere Position der beiden Stützpunkte ist maßgebend
		var maxy = Math.min(heights[ax[0]].y,heights[ax[1]].y) - 2*dyWolke;
		var cy = Math.floor(Math.random() * maxy) + 0;		
		//So, nun die Polygonpunkte im Kreis berechnen;
		var points = [];
		var d = 0;
		for(var j = 0; j < polyPointsWolke; j++){
			var o = {};
			var r = deg2rad(d);
			var v = Math.floor(Math.random() * dyWolke) + dyWolke*0.95;
			var cos = Math.cos(r);
			var sin = Math.sin(r);
			o.x = cos * 1.5*v + cx;
			o.y = sin * 0.5*v + cy;
			points.push(o);
			d += 360/polyPointsWolke;
		}
		drawCloud(points);	
	}
}

function drawCloud(points){
	mapOverlay.createPolyline(points).setFill(white.Trans);
}

function drawGameField(JSONObject){

	map = transformHeights(JSONObject);	
	//Erstmal Himmel weiß machen (rest-Textur weg)
	mapOverlay.createPolyline(map).setFill(white.Full);
	//Dann blau machen
	mapOverlay.createPolyline(map).setFill(blue.Trans);
	//Dann Wolken zeichnen
	var cloudCount = Math.floor(Math.random() * 20) + 5;
	drawClouds(map,cloudCount);
	
	for(i = 0; i < players.length; i++)
		drawTank(players[i]);
}


function drawTank(playerObject){
	var durchmesser = 2*radius;
	var posX = parseInt(playerObject.Position.x,10) - radius;
	var posY = chartHeight - parseInt(playerObject.Position.y,10) - radius;
	mapOverlay.createRect({ x: posX, y: posY, width: durchmesser, height: durchmesser}).setFill(playerObject.Color.Full).setStroke(blue.Full);
	mapOverlay.createImage({  x: posX, y: posY, width:durchmesser,height:durchmesser,src:'img/tank.png'});
	drawCannon(playerObject);
}

function drawFlugbahn(JSONObject){
	for(var i = 0; i < JSONObject.TimePoints.length; i++){
		o = JSONObject.TimePoints[i];
		window.setTimeout("drawProjektil("+o.x+","+o.y+",1)", o.t*1000);		
	}
}

function drawProjektil(x,y,rad){
	projektilOverlay.clear();
	projektilOverlay.createCircle({ cx: x, cy: chartHeight-y, r: rad}).setFill(blue.Full).setStroke(blue.Full);
}

function deg2rad(deg){
	return deg/180*Math.PI;
}

function setCannonAngle(degree){
	for(i = 0; i < players.length; i++)
		if(players[i].ID == myID)
			players[i].Angle = deg2rad(degree);
	adjustCannons();
}

function adjustCannons(){
	cannonOverlay.clear();
	for(i = 0; i < players.length; i++)
		drawCannon(players[i],true);
}

function drawCannon(playerObject){
	
	//Winkel (nur 1 mal berechnen --> sonst teuer!)
	var radians = playerObject.Angle;
	var cos = Math.cos(radians);
	var sin = Math.sin(radians);
	
	//Position (Mittelpunkt)
	var px1 = parseInt(playerObject.Position.x,10) + 1;
	var py1 = chartHeight - parseInt(playerObject.Position.y,10) + 1;
	
	//Fundament
	var halfRadius = radius / 2;
	cannonOverlay.createCircle({ cx: px1, cy: py1, r: halfRadius}).setStroke(black.Full);
	var pxF1 = sin*halfRadius+px1;
	var pxF2 = -sin*halfRadius+px1;
	var pyF1 = cos*halfRadius+py1;
	var pyF2 = -cos*halfRadius+py1;
	cannonOverlay.createLine({ x1: pxF1, y1: pyF1, x2: pxF2, y2: pyF2 }).setStroke({color:black.Full,width:1});
	
	//Cannon
	var cannonLength = 1.5*radius;
	var px2 = cos*cannonLength+px1;
	var py2 = -sin*cannonLength+py1;
	cannonOverlay.createLine({ x1: px1, y1: py1, x2: px2, y2: py2 }).setStroke({color:blue.Full,width:2});
}
