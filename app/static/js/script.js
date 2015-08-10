var numberOfQuestions = 0
var final =[] //Array storing answers to questions
var submitted = false;
var errors = "";


$(document).ready( function() {
	numberOfQuestions = $('#num').text();
	for (var i = 0; i < numberOfQuestions; i++) {
		final.push(0)
	};
	updateWords();
	adjustBoxHeights();
});

function former(num, choice) {//updates final array with current values
	final[num-1] = (choice);
	updateWords();
}

function updateWords(){//updates words at bottom of screen
	errors = "";
	for( var i = 0; i < final.length; i++){
			if (final[i]===0)
			{
				if (errors === ""){
					errors=errors+" "+(i+1);
				}
				else
				{
					errors = errors+", "+(i+1);
				}

			}
		}
	errors = addAnd(errors);
	if (errors === "")
	{
		$('#errors').html("");
	}
	else
	{
		if (errors.length < 3)
		{
			$('#errors').html('You forgot question'+errors);
		}
		else
		{
			$('#errors').html('You forgot questions'+errors);
		}
	}
}

function addAnd(words) {// adds the and to the string of words
	if(words.length > 2)
	{
		words = words.substring(0,words.length-3)+" & "+words.substring(words.length-1,words.length);
	}
	return words
}

function adjustBoxHeights(){ //adjusts the box heights to match up in each row of the table
	for (var i = 0; i < numberOfQuestions; i++)
	{
		var selector1 = "#box1" + String(i+1)
		var selector2 = "#box2" + String(i+1)
		height1 = $(selector1).css('height')
		height2 = $(selector2).css('height')
		numheight1 = parseInt(height1.substring(0,height1.length-2))
		numheight2 = parseInt(height2.substring(0,height2.length-2))
		if (numheight1<numheight2){
			$(selector1).css("height",String(height2))
		} else {
			$(selector2).css("height",String(height1))
		}
	}
}

$(function() {
	$('#submission').click( function() {
		var firsterror = -1;
		allAnswered = true;
		for( var i = 0; i < final.length; i++){
			if (final[i] === 0)
			{
				allAnswered = false;
				if (firsterror === -1){
					firsterror = i;
				}
			}
		}
		if (allAnswered){
			$('#errors').html('');
			if (!submitted){
				message = JSON.stringify(final)
				console.log(message)
				$.ajax({
					type: 'POST',
					url: '/_savedata',
					data: message,
					success: function(){
						$('#submission').css("background-color","blue");
						$('#submission').css("color","red");
						$('#submission').html("Thanks!");
						submitted = true;
					},
					dataType: 'json',
					contentType: 'application/json'

				});
			}
		}
		else{/*scrolls up to first missed question*/	
			myWindow = window;
			var desiredHeight = 24+parseInt($('.top').height());
			for (var i = 0; i < firsterror; i++){
				desiredHeight += parseInt($('#tr'+String(i+1)).height());
			}
			myWindow.scrollTo(0,desiredHeight);
			myWindow.focus();
		}

	});
});
//make sure they answer everything
//notifocation maybe move screen up to what wasn't selected