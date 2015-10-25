(function () {

    var testSocket = io.connect('http://192.168.1.4:12000/test');

    var App = {

        test: null,
        length: 0,
        questionId: 0,
        answers: {},

        /**
         *
         * @param test [ {
         *                 chapter_num: 1,
         *                 question: 'blabla',
         *                 variants: {
         *                      1: 'text1',
         *                      2: 'text',
         *                      3: 'text'
         *                 },
         *                 href: 'http:/blablabla.com/blabla'
         *             } ]
         */
        initTest: function (test) {
            var me = this,
                answers = me.answers;
            me.test = JSON.parse(test);
            me.length = me.test.length;
            me.questionId = 0;
            for (var i = 1; i <= me.length; ++i) {
                answers[i] = 2;
            }
        },

        startTest: function () {
            var me = this;
            $(".start").fadeOut();
            me.updateQuiz(me.getCurrentQuiz(me.test, me.questionId, me.answers));
        },

        getCurrentQuiz: function (test, index, answers) {
            var quiz = test[index];
            return {
                chapterNumber: quiz.chapter_num,
                number: index + 1,
                question: quiz.question,
                variants: quiz.variants,
                link: quiz.href,
                answers: answers
            }
        },

        nextQuestion: function (prevResult) {
            var me = this;
            me.answers[me.questionId + 1] = prevResult ? 1 : 0;
            ++me.questionId;
            me.updateQuiz(me.getCurrentQuiz(me.test, me.questionId, me.answers));
        },

        updateQuiz: function (quiz) {
            var me = this,
                quizDiv = $('.quiz');
            quizDiv.fadeOut(500);
            setTimeout(function () {
                me.updateQuestion(quizDiv, quiz.question, quiz.number);
                me.updateVariants(quizDiv, quiz.variants, quiz.number);
                me.updateAnswers(quizDiv, quiz.answers, quiz.number);
            }, 500);
            quizDiv.fadeIn(500);
        },

        updateQuestion: function (quiz, question, questionId) {
            quiz.find('.question').html('<h4><span class="label label-warning questionId">' + questionId + '</span> ' + question + '</h4>');
        },

        updateVariants: function (quiz, variants, questionId) {
            var variantsDiv = quiz.find('.variants');
            variantsDiv.html("");
            for (var key in variants) {
                variantsDiv
                    .append($('<label class="btn btn-primary btn-block element-animation"></label>')
                        .append($('<span class="btn-label"><i class="glyphicon glyphicon-chevron-right"></i></span>'))
                        .append($('<input type="hidden" name="answer">').val(key))
                        .append(variants[key])
                        .on('click', function () {
                            var answer = $(this).find('input:hidden').val();
                            testSocket.emit('UPDATE', questionId - 1, answer);
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
                answersDiv.append($('<label class="btn-sm ' + answerClass + '">' + key + '</label>'));
            }
        },

        getAnswerButtonClass: function (questionNumber, answer, currentQuestionNumber) {
            return questionNumber === currentQuestionNumber ? 'btn-warning' :
                    answer === 0 ? 'btn-danger' :
                    answer === 1 ? 'btn-success' : 'btn-default';
        },

        finishTest: function (result) {
            var me = this,
                answers = me.answers;
            if (!result) {
                answers[me.questionId + 1] = 0;
            }
            $('.quiz').fadeOut(1000);
            setTimeout(function () {
                var finalDiv = $('.final'),
                    congratulationsDiv = finalDiv.find('.congratulations');
                congratulationsDiv.html(result ? "<h2>Congratulations! <br/>You have passed the test!</h2>"
                                               : "<h2>Looser! <br/>You have failed the test!</h2>");
                me.updateAnswers(finalDiv, answers, -1);
                finalDiv.fadeIn(500);
            }, 1000);
        },

        error: function (msg) {
            $('.quiz').fadeOut();
            alert(msg);
        }
    };

    // Обработка метода set (передаёт JSON данные с вопросами теста), msg - данные
    testSocket.on('set', function (test) {
        App.initTest(test);
        App.startTest();
    });

    // Обработка метода update question_num - порядковый номер вопроса (нумерация начинается с 0), result - true или false
    testSocket.on('update', function (question_num, result) {
        App.nextQuestion(result);
    });

    // Обработка метода finish msg - true или false
    testSocket.on('finish', function (result) {
        App.finishTest(result);
    });

    // Обработка метода error, msg - сообщение об ошибке
    testSocket.on('error', function (error) {
        App.error(error);
    });

    $(function () {
        $("#start").on('click', function () {
            testSocket.emit('GET');
        });
    });
})();