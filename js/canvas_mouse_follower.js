/*
	Canvas mouse follower -> simple 2d animation using html5 canvas.

	Inspired by -> https://medium.com/@matswainson/getting-started-with-canvas-in-html5-ef1917cc496

	// example
	# html
	<canvas id="myCanvas"></canvas>
	
	# js
	let foo = canvasMouseFollower('#myCanvas');
	foo.config({
		size: 25,
		color: 'dodgerblue',
		particles: 30,
		colors: true
	});
	foo.start();
*/


function getRandomInt(min, max){
	/*
		Generates random integer b/w the specified values.
	*/
	return Math.floor(Math.random() * (max - min + 1)) + min;
}
function getRandomColor(){
	/*
		Generates the random hex color codes.
	*/
	return '#' +  Math.random().toString(16).substring(2).padStart(6, '0').substring(0, 6);
}

function miniParticles(color, colors, pointer){
	/*
		Mini particles object
	*/
	this.size = getRandomInt(2, 10);
	this.color = (colors)?getRandomColor(): color;
	this.x = pointer.x + getRandomInt(-10, 10);
	this.y = pointer.y + getRandomInt(-10, 10);
	this.dir = [-1, 1][(Math.floor(Math.random() * 2))];
	this.speedX = getRandomInt(-5, 5);
	this.speedY = getRandomInt(-5, 5);
}


function canvasMouseFollower(selector){
	const self = {
		/*
			Variables
		*/
		canvas: document.querySelector(selector),
		ctx: undefined,
		options: {
			size: 20,	//size of the main circle particle
			color: "#ffffff",	//color of the main circle particles
			particles: 25,	//no of mini particles
			colors: false,	//color of the mini particles (true -> assign random colors to particles, false -> same color as that of main circle particle)
			shadow: true,	//specify the shadow to be used are not
			shadowColor: 'rgba(0,0,0,0)', 	//shadow color,
			fps: 18		//frames per second, amount of times to update the canvas per second
		},
		pointer: {	
			//object contains the x & y coordinates of the cursor and updated through event listener
			x: 0,
			y: 0
		},
		particlesArray: [],	// array consists of mini particles
		animationFrame: 0,
		running: false,
		/*
			Functions
		*/
		config: (userOptions) => {
			// config user options to the particles
			self.options.size = userOptions.size || self.options.size;
			self.options.color = userOptions.color || self.options.color;
			self.options.particles = userOptions.particles || self.options.particles;
			self.options.colors = userOptions.colors || self.options.colors;
			self.options.shadow = userOptions.shadow || self.options.shadow;
			self.options.shadowColor = userOptions.shadowColor || self.options.shadowColor;
			self.options.fps = userOptions.fps || self.options.fps;
		},
		setPointer: (e) => {
			// helper function to assign cursor position to the pointer
			self.pointer.x = e.changedTouches ? e.changedTouches[0].pageX : e.offsetX;
			self.pointer.y = e.changedTouches ? e.changedTouches[0].pageY : e.offsetY;
		},
		setCanvas: (e) => {
			// adjust canvas width & height when window is resized.
			self.canvas.width = document.documentElement.clientWidth;
			self.canvas.height = document.documentElement.clientHeight;
		},
		requestFrame: () => {
			window.requestAnimationFrame(self.drawCircle);
		},
		drawCircle: () => {
			// function to draw particles
			self.ctx.clearRect(0,0, self.canvas.width, self.canvas.height);
			if(self.options.shadow){
				self.ctx.shadowColor = self.options.shadowColor;
			}
			self.ctx.shadowBlur = 2;
			let temp;
			for (let i = 0; i < self.particlesArray.length; i++){
				temp = self.particlesArray[i];
				self.ctx.fillStyle = temp.color;
				self.ctx.beginPath();
				self.ctx.arc( temp.x , temp.y ,temp.size, 0 , 2*Math.PI, false);
				self.ctx.fill();
				self._moveParticles(temp);
			}
			self.ctx.fillStyle = self.options.color;
			self.ctx.shadowBlur = 10;
			self.ctx.beginPath();
			self.ctx.arc(self.pointer.x, self.pointer.y, self.options.size, 0 , 2*Math.PI, false);
			self.ctx.fill();
			self.animationFrame = setTimeout(self.requestFrame, 1000/self.options.fps);
		},
		_moveParticles: (i) => {
			/* 
				Move the mini/sub particles in random direction and decrease the size of the mini particles to provide a good look.
				Also assign the new size, when size is lesser than 1.
			*/
			if(i.size < 1){
				i.size = getRandomInt(3, 8);
				i.y = self.pointer.y;
				i.x = self.pointer.x;
			}
			i.y += i.speedY;
			i.x += i.speedX;
			i.size *= 0.85;
		},
		_createParticles: (color, colors, pointer) => {
			// creates the mini/sub particles
			for(let i=0; i<self.options.particles; i++){
				self.particlesArray.push(new miniParticles(color, colors, pointer));
			}
		},
		setParticlesColor: (colors) => {
			/*
				@param colors: array of background colors for mini particles

				This function indirectly assign colors to the mini particles, so it is recommended to call this function only after the start function is called.

				Random color from the array will be assigned to the mini particles.
			*/
			for(let i=0; i<self.particlesArray.length; ++i){
				self.particlesArray[i].color = colors[Math.floor(Math.random() * colors.length)];
			}
		},
		init: () => {
			//action to be taken place before animation yet to be started.
			self.ctx = self.canvas.getContext('2d');
			self.canvas.addEventListener('touchstart', self.setPointer);
			self.canvas.addEventListener('touchmove', self.setPointer);
			self.canvas.addEventListener('mousemove', self.setPointer);
			window.addEventListener('orientationchange', self.setCanvas);
			window.addEventListener('resize', self.setCanvas);
			self._createParticles(self.options.color, self.options.colors, self.pointer);
			self.setCanvas(self.canvas);
		},
		start: () => {
			// starts the animation
			if(!self.running && !self.animationFrame)
				self.init();
			self.running = true;
			self.requestFrame();
		},
		stop: () => {
			// stops the animation
			self.running = false;
			clearTimeout(self.animationFrame);
		}
	}
	return self;
}