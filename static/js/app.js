var CODES = {
	GET_QUESTION: 'get_question',
	GET_RESULTS: 'get_results',
	GET_START: 'get_start',
	SEND_START: 'on_start',
	SEND_QUESTION: 'on_question'
};


var initTest = {
	code: 'get_start',
	success: true
};

var test = [
    {
    	code: 'get_question',
        success: true,
        number: 1,
        question: "What is your name?",
        variants: {
            1: "Alex",
            2: "Eugen",
            3: "Max",
            4: "Nikita",
            5: "Sergey"
        },
        answers: {
        	1: 2,
        	2: 2,
        	3: 2
        }
    },
    {
    	code: 'get_question',
        success: true,
        number: 2,
        question: "What is your age?",
        variants: {
            1: "< 10",
            2: "10-20",
            3: "20-30",
            4: "30-40",
            5: "40-50",
            6: "> 50"
        },
        answers: {
        	1: 1,
        	2: 2,
        	3: 2
        }
    },
    {
    	code: 'get_question',
        success: true,
        number: 3,
        question: "What is your sex?",
        variants: {
            1: "Male",
            2: "Female"
        },
        answers: {
        	1: 1,
        	2: 0,
        	3: 2
        }
    },
];

var results = {
	code: 'get_results',
	success: true,
	completed: true,
	answers: {
		1: 1,
		2: 0,
		3: 1
	}
};

var ResponseManager = {
	process: function (response) {
		if (!response.success) {
			throw("Server error!");
			alert("Server error!");
		} else if (response.code === CODES.GET_START) {
			App.startTest(response);
		} else if (response.code === CODES.GET_QUESTION) {
			App.updateQuiz(response);
		} else if (response.code === CODES.GET_RESULTS) {
			App.finishTest(response);
		}
	}
};

var SocketHelper = {

	// TODO: remove, just for emulation
	questionNumber: 0,

	init: function (request) {
		var me = this;
		// send to server init message

		// TODO: remove - server emulation
		setTimeout (function () {
			me.get(initTest);
		}, 200);
	},

	send: function (request) {
		var  me = this;
		// send request

		// TODO: remove - server emulation
		setTimeout (function () {
			if (me.questionNumber != test.length) {
				me.get(test[me.questionNumber]);
				++me.questionNumber;
			} else {
				me.get(results);
			}
		}, 200);
	},

	get: function (response) {
		ResponseManager.process(response);
	}
};

var RequestBuilder = {

	buildInitRequest: function (testType) {
		return {
			code: CODES.SEND_START,
			testType: testType
		};
	},

	buildQuestionSubmitRequest: function (questionId, answerId) {
		return {
			code: CODES.SEND_QUESTION,
			questionId: questionId,
			answerId: answerId
		};
	},

	buildFirstQuestionRequest: function () {
		return {
			code: CODES.SEND_QUESTION
		}
	}

};

var App = {

    startTest: function () {
        var me = this;
        $(".start").fadeOut(500);

        SocketHelper.send(RequestBuilder.buildFirstQuestionRequest());
    },


    updateQuiz: function (response) {
        var me = this,
        	quiz = $('.quiz');
        quiz.fadeOut(500);
        setTimeout(function () {
        	me.updateQuestion(quiz, response.question, response.number);
        	me.updateVariants(quiz, response.variants, response.number);
            me.updateAnswers(quiz, response.answers, response.number);
        }, 500);
        quiz.fadeIn(500);
    },

    updateQuestion: function (quiz, question, questionId) {
        quiz.find('.question').html('<h3><span class="label label-warning questionId">' + questionId + '</span> ' + question + '</h3>');	
    },	

    updateVariants: function (quiz, variants, questionId) {
    	var variantsDiv = quiz.find('.variants');
            variantsDiv.html("");
        for (var key in variants) {
            variantsDiv
                .append($('<label class="btn btn-lg btn-primary btn-block element-animation"></label>')
                    .append($('<span class="btn-label"><i class="glyphicon glyphicon-chevron-right"></i></span>'))
                    .append($('<input type="radio" name="answer">').val(key))
                    .append(variants[key])
                    .on('click', function () {
                        var answer = $(this).find('input:hidden').val();
                        var request = RequestBuilder.buildQuestionSubmitRequest(answer, questionId);
                        SocketHelper.send(request);
                    })
            );
        }
    },

    updateAnswers: function (quiz, answers, questionId) {
    	var me = this,
    		answersDiv = quiz.find('.answers');
            answersDiv.html("");
        for (var key in answers) {
        	var answer = answers[key],
        		answerClass = me.getAnswerButtonClass(parseInt(key), answer, questionId);
        	answersDiv.append($('<label class="btn-sm ' +  answerClass + '">' + key + '</label>'));
        }
    },

    getAnswerButtonClass: function (questionNumber, answer, currentQuestionNumber) {
    	return questionNumber === currentQuestionNumber ? 'btn-warning' : 
    			answer === 0 ? 'btn-danger' : 
    			answer === 1 ? 'btn-success' : 'btn-default';
    },

    finishTest: function (response) {
    	var me = this;
        $('.quiz').fadeOut(1000);
        setTimeout(function () {
        	var finalDiv = $('.final');
        	me.updateAnswers(finalDiv, response.answers, -1);
        	finalDiv.fadeIn(500);
        }, 1000);
    }
};


$(function () {

    $("#start").on('click', function () {
    	SocketHelper.init(RequestBuilder.buildInitRequest());
    });

});

