(function() {
    var testSocket = io.connect('/test');

    // Обработка метода set (передаёт JSON данные с вопросами теста), msg - данные
    testSocket.on('set', function(msg) {
        console.log(msg);
        alert(msg)
    });

    // Обработка метода update question_num - порядковый номер вопроса (нумерация начинается с 0), result - true или false
    testSocket.on('update', function(question_num, result) {
        console.log(question_num, result);
        alert(question_num + " " + result);
    });

    // Обработка метода finish msg - true или false
    testSocket.on('finish', function(result) {
        console.log(result);
        alert(result)
    });

    // Обработка метода error, msg - сообщение об ошибке
    testSocket.on('error', function(error) {
        console.log(error);
        alert(error)
    });

    // Отправляешь get запрос без параметров
    testSocket.emit('GET', [1]);

    // Отправлешь update запрос с параметром
    testSocket.emit('UPDATE', 0, 2);

})();
