var Swarm = Swarm || {};

(function(Swarm) {

	var boids = [],
		TURN_SPEED = 0.05,
		MIN_DIST = 6,
		MAX_DIST = 30,
		MOUSE_DIST = 300,
		targetX,
		targetY;

	function Boid(width, height, speed) {
		this.x = 0;
		this.y = 0;
		this.vx = 0;
		this.vy = 0;
		this.angle = 0;
		this.size = 8;
		this.speed = speed;
		this.closestBoid = null;
    width = 3; height = 3;
		this.div = document.createElement('div');
		this.div.style.width = width + 'px';
		this.div.style.height = height + 'px';
		this.div.classList.add('boid');
	}

	Boid.prototype.update = function() {
		this.closestBoid = this.getClosest();
		if (!this.closestBoid) {
			return;
		}

		var hx,
			hy;

		if (targetX && targetY) {
			hx = targetX - this.x;
			hy = targetY - this.y;
		} else {
			hx = this.closestBoid.x - this.x;
			hy = this.closestBoid.y - this.y;
		}

		var distHeading = Math.sqrt(hx * hx + hy * hy),
			vxHeading,
			vyHeading;

		if (distHeading > MOUSE_DIST) {
			vxHeading = Math.random() - 0.5;
			vyHeading = Math.random() - 0.5;
		} else {
			vxHeading = hx / distHeading;
			vyHeading = hy / distHeading;
		}

		var dxClosest = this.closestBoid.x - this.x;
		var dyClosest = this.closestBoid.y - this.y;

		var normClosest = Math.sqrt(dxClosest * dxClosest + dyClosest * dyClosest);
		var distClosest = Math.sqrt(dxClosest * dxClosest + dyClosest * dyClosest) - this.closestBoid.size;

		var vxClosest = dxClosest / normClosest;
		var vyClosest = dyClosest / normClosest;
		
		var vxAverage,
			vyAverage;

		if (distClosest > MAX_DIST) {
			vxAverage = vxHeading + vxClosest;
			vyAverage = vyHeading + vyClosest;
		} else if (distClosest < MIN_DIST) {
			vxAverage = -vxClosest;
			vyAverage = -vyClosest;
		} else {
			vxAverage = vxHeading;
			vyAverage = vyHeading;
		}

		var normAverage = Math.sqrt(vxAverage * vxAverage + vyAverage * vyAverage);
		vxAverage = vxAverage / normAverage;
		vyAverage = vyAverage / normAverage;
		
		var crossProduct = this.vx * vyAverage - this.vy * vxAverage,
			angleDifference;

		if (this.vx * vxAverage + this.vy * vyAverage > 0) {
			angleDifference = Math.asin(crossProduct);	
		} else {
			angleDifference = Math.PI - Math.asin(crossProduct);
		}

		angleDifference = Math.abs(angleDifference);

		if (crossProduct > 0) {
			this.angle += angleDifference * TURN_SPEED; // Turn right
		} else {
			this.angle -= angleDifference * TURN_SPEED; // Turn left
		}

		this.vx = Math.cos(this.angle);
		this.vy = Math.sin(this.angle);
		
		this.move();
	};

	Boid.prototype.move = function() {
		this.x += this.vx * this.speed;
		this.y += this.vy * this.speed;

		if (this.x < -this.size * 2) {
			this.x = window.innerWidth;
		} else if (this.x > window.innerWidth + this.size) {
			this.x = -this.size
		}
		if (this.y < -this.size * 2) {
			this.y = window.innerHeight;
		} else if (this.y > window.innerHeight + this.size) {
			this.y = -this.size;
		}

		this.div.style.transform = this.div.style.webkitTransform = this.getTransform();
	};

	Boid.prototype.getTransform = function() {
		return 'translate3d(' + this.x + 'px' + ',' + this.y + 'px,0) rotateZ(' + (this.angle * 180 / Math.PI - 90) + 'deg)';
	};

	Boid.prototype.getClosest = function() {
		var dist = Infinity;
		var ret = null;

		for (var i = boids.length; i--; ) {
			var b = boids[i];
			if (this !== b) {
				var dx = b.x - this.x;
				var dy = b.y - this.y;
				var d = dx * dx + dy * dy - b.size * b.size;
				if (d < dist) {
					dist = d;
					ret = b;
				}
			}
		}

		return ret;
	};

	function addBoid(b) {
		document.body.appendChild(b.div);
		boids.push(b);
	}

	function createBoids(total, width, height, speed) {
		for (var i = total; i--; ) {
			var b = new Boid(width, height, speed);
			b.x = Math.random() * window.innerWidth;
			b.y = Math.random() * window.innerHeight;
			b.angle = Math.random() * 360;
			addBoid(b);
		}
	}
	
	function update() {
		updateID = requestAnimationFrame(update);

		for (var i = boids.length; i--; ) {
			var b = boids[i];
			b.update();
		}
	}
	
	window.addEventListener('mousemove', function(event) {
		targetX = event.pageX;
		targetY = event.pageY;
	});

	document.addEventListener('mouseout', function(event) {
		targetX = targetY = 0;
	});

	document.addEventListener('touchstart', function(event) {
  	targetX = event.targetTouches[0].pageX;
  	targetY = event.targetTouches[0].pageY;
  });

  document.addEventListener('touchmove', function(event) {
  	event.preventDefault();
  	targetX = event.targetTouches[0].pageX;
  	targetY = event.targetTouches[0].pageY;
  });

	document.addEventListener('touchend', function(event) {
  	targetX = targetY = 0;
  });

  window.onload = function() {
	 	setTimeout(function() {
			if (window.innerWidth < 500) {
				createBoids(3, 5, 25, 3);
			} else {
				createBoids(9, 6, 30, 4);
			}
			update();
		}, 100);
  }

}(Swarm));

// requestAnimationFrame shim
var i = 0,
    lastTime = 0,
    vendors = ['ms', 'moz', 'webkit', 'o'];

while (i < vendors.length && !window.requestAnimationFrame) {
  window.requestAnimationFrame = window[vendors[i] + 'RequestAnimationFrame'];
  window.cancelAnimationFrame = window[vendors[i] + 'CancelAnimationFrame'] || window[vendors[i] + 'CancelRequestAnimationFrame'];
  i++;
}

if (!window.requestAnimationFrame) {
  window.requestAnimationFrame = function(callback, element) {
    var currTime = new Date().getTime(),
        timeToCall = Math.max(0, 1000 / 60 - currTime + lastTime),
        id = setTimeout(function() { callback(currTime + timeToCall); }, timeToCall);
    
    lastTime = currTime + timeToCall;
    return id;
  };
}

if (!window.cancelAnimationFrame) {
  window.cancelAnimationFrame = function(id) {
    clearTimeout(id);
  };
}