/*Wichtig für going live
startServer.py
	Adresse localhost weg und mit "" --> auf allen Interfaces lauschen
	SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.ThreadingTCPServer(("", 9999), GameSocketHandler)
*/


//Spielvariablen
var errorOrClosed = false;
var socket = false;
var playerNameEntered = null;
var players = [];
var playerColors = [];
var gameOver = true;

var myID = false;
var radius = 10;
var selfHasTurn = true;
var hitObject = false;

var green = {};
var orange = {};
var red = {};
var blue = {};
var violet = {};
var cyan = {};
var gray = {};
var black = {};
var white = {};

function startGame(){
		
	if(playerNameEntered == "" || playerNameEntered == null)
		playerNameEntered = prompt("Please enter your name:");
	if(playerNameEntered == "" || playerNameEntered == null){
		addLogLine("You have to enter a nickname before you can play!",orange.Full,"logList");
		return;
	}
	cleanup();
	gameOver = false;
	players = [];
	mapOverlay.clear();
	cannonOverlay.clear();
	projektilOverlay.clear();
	socketCommunication();
}

function cleanup(){		
	addLogLine("You can restart by clicking on Start Game",green.Full,"logList");
	setFieldState('startButton',false);
	setFieldState('chatButton',false);
}

function setupColors(){
	green = { Full:"rgba(0,255,0,1)", Trans:"rgba(0,255,0,0.5)" };
	orange = { Full:"rgba(255,165,0,1)", Trans:"rgba(255,165,0,0.5)" };
	red = { Full:"rgba(255,0,0,1)", Trans:"rgba(255,0,0,0.5)" };
	blue = { Full:"rgba(0,0,255,1)", Trans:"rgba(0,0,255,0.5)" };
	violet = { Full:"rgba(255,0,255,1)", Trans:"rgba(255,0,255,0.5)" };
	cyan = { Full:"rgba(0,255,255,1)", Trans:"rgba(0,255,255,0.5)" };
	white = { Full:"rgba(255,255,255,1)", Trans:"rgba(255,255,255,0.5)" };
	black = { Full:"rgba(0,0,0,1)", Trans:"rgba(0,0,0,0.5)" };
	playerColors = new Array(green,red,blue,orange,violet,cyan);
}

function socketCommunication(){
	errorOrClosed = false;
	require(['dojox/socket'], function (Socket) {
		addLogLine("Try to reach server...",orange.Full,"logList");
		//Create Socket
		socket = new Socket("ws://localhost:80");
		//socket = new Socket("ws://w3bs.de:9999");
		
		//Bei Fehler abbrechen			
		socket.on("error", function(event){
			addLogLine("Socket error",orange.Full,"logList");
			errorOrClosed = true;
			cleanup();
		});
		//Socket schließen
		socket.on("close", function(event){
			addLogLine("Socket closed!",orange.Full,"logList");
			errorOrClosed = true;
			cleanup();
		});
		
		//If Connection is open
		socket.on("open", function(event){
			setFieldState('startButton',true);
			addLogLine("Connection established!",green.Full,"logList");
			var logonString = JSON.stringify({name:playerNameEntered});
			var serverString = buildServerString("Logon",logonString);
			socket.send(serverString);
		});
				
		socket.on("message", function(event){
			var JSONObject;
			var data = event.data;			
			var identifier = getJSONIdentifier(data,":");
			var json = data.substr(identifier.length+1);
			addLogLine("Retrieving Data (Message-Identifier: "+identifier+")",orange.Full,"logList");
			//addLogLine(json,orange.Full,"logList");
			//Nur JSON parsen, wenn es tatsächlich json ist
			if(identifier != "WaitForPlayer" && identifier != "PlayerAvailable" && identifier != "WrongTurn"){
				//Always use secure parsing (second parameter)
				JSONObject = JSON.parse(json, true);
			}
			
			switch(identifier){			
				case "Player":
					myID = JSONObject.ID;
				break;
			
				case "WaitForPlayer":
					addLogLine("Currently there is no opponent. You'll get\
					informed if an opponent is ready...",orange.Full,"logList");
				break;
				
				case "PlayerAvailable":
					addLogLine("Yeah :-) There is an opponent!",green.Full,"logList");
				break;
				
				case "Player1":
					JSONObject.Color = playerColors[0];
					players.push(JSONObject);
				break;
				
				case "Player2":
					JSONObject.Color = playerColors[1];
					players.push(JSONObject);					
				break;
				
				case "PlayerBegins":
					//addLogLine(json,orange.Full,"logList");					
					
					if(JSONObject.ID == myID){
						selfHasTurn = true;
						addLogLine("You have the first turn!",blue.Full,"logList");
					}
					else
					{
						selfHasTurn = false;
						addLogLine("Your opponent has the first turn!",blue.Full,"logList");
					}
					
					setupPlayers(players);
					
				break;
				
				case "MapHorizon":			
					createGameField(JSONObject);
				break;
				
				case "Fired":
					//Kanonen justieren
					for(i = 0; i < players.length; i++)
						if(JSONObject.Origin.ID == players[i].ID)	
							players[i].Angle = JSONObject.Origin.Angle;
					adjustCannons();
					selfHasTurn = !selfHasTurn;
					drawFlugbahn(JSONObject);
					//Den Button erst nach der Zeit wieder umschwenken
					var maxTime = JSONObject.TimePoints[JSONObject.TimePoints.length-1].t;
					window.setTimeout("setFieldState('fireButton',"+!selfHasTurn+")",maxTime*1000);
					window.setTimeout("projektilOverlay.clear()",maxTime*1000);
					hitObject = JSONObject.Hits;
					window.setTimeout("checkHits()",maxTime*1000);
					window.setTimeout("checkGameOver()",maxTime*1000+2000);
				break;
				
				case "PlayerLostConnection":				
					if(gameOver == true)
						addLogLine("Player "+JSONObject.Name+" has left the game!",orange.Full,"logList");
					else{
						addLogLine("Player "+JSONObject.Name+" has lost connection or given up!",orange.Full,"logList");
						for(i = 0; i < players.length; i++)
							if(players[i].ID == JSONObject.ID)
								players[i].Lost = true;
						checkGameOver();					
					}
					//Test
					cleanup();
				break;
				
				case "Message":
					addLogLine(JSONObject.Message,blue.Full,"chatList");
				break;
				
			}
		});	
		
	});
}

function createGameField(JSONObject,radius){
	drawGameField(JSONObject);
	show("gamePanel");
}

function setupPlayers(players){
	//Spielernamen in Titelleiste angeben und Controls und Statistics einfärben
	var s = "";
	for(i = 0; i < players.length; i++){
		players[i].Angle = deg2rad(90);
		if(myID == players[i].ID)
			document.getElementById('controlPanel').style.background = players[i].Color.Trans;
		else 
			addLogLine("Your opponent is "+players[i].Name+"!",blue.Full,"logList");
		s += players[i].Name;
		if(i < players.length-1)
			s += " vs ";
	}
	document.getElementById("playerNames").innerHTML = s;
	document.getElementById("angle").value = 90;
	document.getElementById("power").value = 0;
	
	//Spielerstatistiken einbauen
	addStatisticTables(players);
	setFieldState('fireButton',!selfHasTurn);
	setFieldState('chatButton',false);
}

function fire(){
	//Button sofort sperren
	setFieldState('fireButton',true);
	var myAngle = document.getElementById('angle').value;
	//bei mehreren Spielern kann zwischen 0 und 180 Grad geschossen werden!
	myAngle = deg2rad(myAngle);
	var myPower = document.getElementById('power').value;
	if(errorOrClosed) return;
	var json = JSON.stringify({angle:myAngle,power:myPower});
	var serverString = buildServerString("Fire",json);
	socket.send(serverString);	
}


function checkHits(){
	if(hitObject.length == 0){
		addLogLine("No hit detected!!",blue.Full,"logList");
		return false;
	}
	//Wieso ist das Hit-Object so?! Ahhh, wegen mehreren Playern!!! Danke-Mike!!!
	for(j = 0; j < hitObject.length; j++){
		for(i = 0; i < players.length; i++){
			if(hitObject[j].Player.ID == players[i].ID){
				var damage = parseInt(hitObject[j].Player.Damage*100,10);
				players[i].Damage = damage;
				var id1 = "damageRatioMeter"+players[i].ID;
				var id2 = "damageRatioValue"+players[i].ID;
				document.getElementById(id1).value = damage;
				document.getElementById(id2).innerHTML = damage;
				var hitName = players[i].Name+" was";
				if(players[i].ID == myID)
					hitName = "You were";
				addLogLine(hitName + " hit ("+parseInt(hitObject[j].Percent*100,10)+" damage)!",blue.Full,"logList");
				if(players[i].Damage >= 100)
					players[i].Lost = true;
			}
		}
	}
	showImageForSeconds('img/explosion.gif',2);
	
}

function checkGameOver(){
	var playersDeath = 0;
	var lastPlayerAlive = false;
	for(i = 0; i < players.length; i++){
		if(players[i].Lost == true)
			playersDeath++;
		else
			lastPlayerAlive = players[i];
		//Spieler informieren, dass er verloren hat
		if(myID == players[i].ID && players[i].Lost == true){
			drawText("You lost!!!",red.Trans);
			
			gameOver = true;
			cleanup();
		}
		
	}
	//Wenn nur noch ein Spieler übrig ist,
	if(playersDeath == players.length-1 && lastPlayerAlive.ID == myID){
		drawText("You won!!!",green.Trans);
		gameOver = true;
		cleanup();
	}
}

function buildServerString(identifier,json){
	return identifier+":"+json;
}

function getJSONIdentifier(string,delim){
	var arr = string.split(delim);
	return arr[0];
}

function printDebug(obj){
	for(var propertyName in obj) {
	   console.log("Property: " + propertyName + " Value: " + obj[propertyName]);
	}
}

function addLogLine(text,color,where){
	require(["dojo/dom-construct"], function(domConstruct){
		var ul = document.getElementById(where);
		domConstruct.create("li", { innerHTML: text }, ul);
		var li = ul.getElementsByTagName('li');
		li[li.length-1].style.color = color;
		//Scroll to end
		var div = ul.parentNode;
		div.scrollTop = div.scrollHeight;
	});	
}



function show(id){
	document.getElementById(id).style.display = "block";
}

function hide(id){
	document.getElementById(id).style.display = "none";
}

function setFieldState(id,state){
	var b = document.getElementById(id);
	b.disabled = state;
}

function showValue(value,appendix,target){
	document.getElementById(target).innerHTML = value + appendix;
}

function prepareShot(){
	if(constraintsOk())
		fire();
}

function constraintsOk(){
	var iAngle = document.getElementById('angle');
	var iPower = document.getElementById('power');
	var av = parseInt(iAngle.value,10);
	var amin = parseInt(iAngle.min,10);
	var amax = parseInt(iAngle.max,10);
	var pv = parseInt(iPower.value,10);
	var pmin = parseInt(iPower.min,10);
	var pmax = parseInt(iPower.max,10);	
	
	//Nur Zahlen erlauben
	var regex = /[^,\d]/g;
	var ergAngle = regex.test(av);
	var ergPower  = regex.test(pv);
	
	var error = false;
	if(av < amin || av > amax || ergAngle == true){
		addLogLine("Wrong Angle Set! (" + av + ")",orange.Full,"logList");
		error = true;
	}
	if(pv < pmin || pv > pmax || ergPower == true){
		addLogLine("Wrong Power Set! (" + pv + ")",orange.Full,"logList");
		error = true;
	}
	
	return !error;
}

function addStatisticTables(players){
	var opponentStatistics = document.getElementById('opponentStatistics');
	var s = "";
	for(i = 0; i < players.length; i++)
		s += getStatisticHTML(players[i]);
	opponentStatistics.innerHTML = s;
}

function getStatisticHTML(playerObject){
	return "<fieldset id='stat"+playerObject.ID+"' style='background:"+playerObject.Color.Trans+"'>\
		<legend>"+playerObject.Name+"</legend>\
			<table>\
				<tr>\
					<th>Damage ratio: </th>\
					<th><span id='damageRatioValue"+playerObject.ID+"'>0</span>%</th>\
				</tr>\
				<tr>\
					<td colspan='2'><meter min='0' low='33' optimum='0' high='66' max='100' value='0' id='damageRatioMeter"+playerObject.ID+"'></td>\
				</tr>\
			</table>\
		</fieldset>";
}

function showImageForSeconds(imgUrl,seconds){

	document.getElementById("replaceableContent").style.display = "block";
	document.getElementById("replaceableContent").innerHTML = "<img src='"+imgUrl+"' class='overlay'/>";	
	document.getElementById("mapOverlay").style.display = "none";
	document.getElementById("cannonOverlay").style.display = "none";
	document.getElementById("projektilOverlay").style.display = "none";
	
	window.setTimeout("resetContent()",seconds*1000);
}

function resetContent(){
	document.getElementById("replaceableContent").style.display = "none";
	document.getElementById("mapOverlay").style.display = "block";
	document.getElementById("cannonOverlay").style.display = "block";
	document.getElementById("projektilOverlay").style.display = "block";
}

function drawText(aText,color){
	cannonOverlay.createText({ x:70, y:230, text:aText, align:"start"}).
					setFont({ family:"Arial", size:"72pt", weight:"bold" }). //set font
					setFill(color);
}

function showHighscoreList(){
	alert("ToDo");
}

function showAboutDialog(){
	alert("ToDo");
}

function sendChatMessage(){
	var v = document.getElementById("chatMessage").value;
	var s = JSON.stringify({Message:v});
	var ss = buildServerString("Message",s);
	socket.send(ss);	
	addLogLine(v,blue.Trans,"chatList");
}