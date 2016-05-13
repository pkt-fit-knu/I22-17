HOR_UP = 117;
HOR_DOWN = 388;
VER_LEFT = 55;
VER_RIGHT = 623;

HOLE = [{x:60, y:118}, {x:337, y:114}, {x:623, y:116},
	{x:625, y:389}, {x:337, y:390}, {x:54, y: 386}]
REVERSE_HOLE = [{x:620, y:385}, {x:337, y:385}, {x:65, y:380},
	{x:65, y:125}, {x:337, y:120}, {x:615, y: 155}]

function normalize_vec(vec){
	len_vec = get_vec_len(vec);
	return {x: vec.x/len_vec, y: vec.y/len_vec};
}
function change_vec(vec, new_len){
	vec = normalize_vec(vec);
	return {x: vec.x*new_len, y:vec.y*new_len};
}
function point_distance(p1, p2){
	return Math.sqrt((p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y));
}
function get_vec_len(vec){
	return Math.sqrt(vec.x*vec.x + vec.y*vec.y);
}
function is_going(){
	flag = false;
	for (var k=0; k<Balls.length; k++){
		if (Balls[0].vec.x != 0 || Balls[0].vec.y != 0){
			flag = true;
		}
	}
	return flag;
}
function copy_balls(){
	arr = [];
	for (var i=0; i<Balls.length; i++){
		ob = {point: {x: Balls[i].point.x, y: Balls[i].point.y},
			vec: {x: Balls[i].vec.x, y:Balls[i].vec.y}, id: Balls[i].id};
		arr.push(ob);
	}
	return arr;
}
function going(){
	for (var i=0; i<Balls.length; i++){
		for (var k=0; k<i; k++){
			if (point_distance(Balls[i].point, Balls[k].point) < 25){
				kick_vec = {x: Balls[i].point.x - Balls[k].point.x, y: Balls[i].point.y - Balls[k].point.y};
				// Balls[i].vec.x *= -1; Balls[i].vec.y *= -1;
				// Balls[k].vec.x *= -1; Balls[k].vec.y *= -1;
				Balls[i].vec.x += kick_vec.x/10; Balls[i].vec.y += kick_vec.y/10;
				Balls[k].vec.x -= kick_vec.x/10; Balls[k].vec.y -= kick_vec.y/10;
			}
		}
	}
	for (var i=0; i<Balls.length; i++){
		if (Balls[i].point.x != -666){
			ball_obj = document.getElementById('ball-'+Balls[i].id);
			Balls[i].point.x += Math.round(Balls[i].vec.x);
			Balls[i].point.y += Math.round(Balls[i].vec.y);
			for (var j=0; j<HOLE.length; j++){
				if (point_distance(Balls[i].point, HOLE[j]) < 9){
					if (Balls[i].id == 1){
						was_vx = Balls[i].vec.x;
						was_vy = Balls[i].vec.y;
						new_x = REVERSE_HOLE[j].x;
						new_y = REVERSE_HOLE[j].y;
						console.log('new:',new_x,' ',new_y);
						document.getElementById('time-travel').style.display = 'block';
						audio_travel.innerHTML = '<audio autoplay><source src="travel.mp3" type="audio/mpeg"><//audio>';
						clearInterval(timer_go);
						setTimeout(function(){
							audio_travel.innerHTML = '';
							document.getElementById('time-travel').style.display = 'none';
							Balls = Time[0];
							new_ball = {point: {x: Balls[0].point.x, y: Balls[0].point.y}, 
								vec: {x: Balls[0].vec.x, y: Balls[0].vec.y}, id: 99};
							Balls.push(new_ball);
							Balls[0] = {point: {x: new_x, y:new_y}, 
								vec: {x:was_vx, y:was_vy}, id: 1};
							timer_go = setInterval(going, 40);
						}, 2000);
					}
					else {
						// alert('OH MY GOD');
						Balls[i].point.x = -666; Balls[i].point.y = -666;
						Balls[i].vec.x = 0; Balls[i].vec.y = 0;
						ball_obj.style.left = '-666px';
					}
				}
			}
		}
		if (Balls[i].point.x != -666){
			if (Balls[i].point.y < HOR_UP){
				Balls[i].point.y = HOR_UP;
				Balls[i].vec.y *= -1;
			}
			if (Balls[i].point.y > HOR_DOWN){
				Balls[i].point.y = HOR_DOWN;
				Balls[i].vec.y *= -1;
			}
			if (Balls[i].point.x < VER_LEFT){
				Balls[i].point.x = VER_LEFT;
				Balls[i].vec.x *= -1;
			}
			if (Balls[i].point.x > VER_RIGHT){
				Balls[i].point.x = VER_RIGHT;
				Balls[i].vec.x *= -1;
			}
			ball_obj.style.left = Balls[i].point.x - 10 + 'px';
			ball_obj.style.top = Balls[i].point.y - 10 + 'px';
			power = get_vec_len(Balls[i].vec);
			power -= 0.1;
			if (power < 0.3){
				Balls[i].vec = {x:0, y:0};
			}
			else {
				Balls[i].vec = change_vec(Balls[i].vec, power);
			}
		}
	}
	if (is_going() == false){
		Time = [];
	}
	else {
		Time.push(copy_balls());
	}
}

function Kick(toX, toY, power){
	vector = change_vec({x: toX-Balls[0].point.x, y: toY-Balls[0].point.y}, power);
	//console.log('new vector:'+vector.x+' '+vector.y);
	Balls[0].vec = vector;
}

click_pool = function(e){
	if (!is_going()){
		e_x = e.pageX - game_obj.getBoundingClientRect().left;
		e_y = e.pageY - game_obj.getBoundingClientRect().top;
		console.log('u clicked at:'+e_x+' '+e_y);
		Kick(e_x, e_y, 10);
	}
};
audio_travel = document.getElementById('audio');
game_obj = document.getElementById('game');
game_obj.onclick = click_pool;
your_ball = document.getElementById('ball-1');
Balls = [{point: {x:550, y:250}, vec: {x:0, y:0}, id:1}, 
	{point: {x:350, y:250}, vec: {x:0, y:0}, id:2},
	{point: {x:325, y:225}, vec: {x:0, y:0}, id:3},
	{point: {x:325, y:275}, vec: {x:0, y:0}, id:4}];
timer_go = setInterval(going, 40);
Time = [ copy_balls() ];
