// Assigns a html element to a variable for convenience
const app = document.getElementById('root');

// Creates a new html element "logo"
const logo = document.createElement('img');
// Sets the source image for "logo" to an image file in the same directory
logo.src = 'ghibli_logo.png';

// Creates a new html element, a div
const container = document.createElement('div');
container.setAttribute('class', 'container');

// Add our created elements to an element of the page
app.appendChild(logo);
app.appendChild(container);

// Create a request variable and assign a new XMLHttpRequest Object to it.
var request = new XMLHttpRequest();

// Open a new connection, using the GET request on the URL endpoint
request.open('GET', 'https://ghibliapi.herokuapp.com/films', true);

request.onload = function () {
	// Begin accessing JSON data here
	var data = JSON.parse(this.response);
	
	// Check response code!
	if (request.status >= 200 && request.status < 400) {
		
		// Iterate through the objects in the returned JSON file
		data.forEach(movie => {
	
			// Log each movie's title
			console.log(movie.title);
			console.log(movie.description);
			
			// Create a div with a card class
			const card = document.createElement('div');
			card.setAttribute('class', 'card');
			
			// Create a title (an h1, in JS speak), and set the text content to the film's title
			const h1 = document.createElement('h1');
			h1.textContent = movie.title;
			
			// Create a paragraph (a p, in JS speak) and set the text content to the film's description
			const p = document.createElement('p');
			movie.description = movie.description.substring(0, 300);  // Limit the description to 300 characters
			p.textContent = `${movie.description}...`;  // End with an ellipses - REF I DON'T KNOW WHAT THAT MEANS
			
			// Append the card to the container element
			container.appendChild(card);
			
			// Append the title and description (h1 and p) to the card
			card.appendChild(h1);
			card.appendChild(p);
			
		});
		
	// If it's the wrong error code, report it
	} else {
		console.log('error');
	}
};

// Send request
request.send();




