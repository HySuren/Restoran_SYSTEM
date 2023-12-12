$(document).ready(function(){
    var previousValues = []; // массив для хранения предыдущих значений
    var totalAmount = 0; // общая сумма
    var resultDiv = $('#result');

    $('.btn').click(function(){
        var value = $(this).val();
        var price = parseFloat($(this).data("price")); // получаем цену из атрибута data-price
        previousValues.push({name: value, price: price}); // добавляем новое значение в массив предыдущих значений
        totalAmount += price; // добавляем цену к общей сумме
        updateResult(); // обновляем отображаемые значения
    });

    $('#clearValues').click(function(){
        previousValues = []; // очищаем массив предыдущих значений
        totalAmount = 0; // обнуляем общую сумму
        updateResult(); // обновляем отображаемые значения
    });

    // Вешаем обработчик удаления на все созданные элементы
    resultDiv.on("click", ".delete-item", function(){
        var index = $(this).data("index");
        var price = previousValues[index].price;
        previousValues.splice(index, 1);
        totalAmount -= price; // вычитаем цену товара из общей суммы
        updateResult(); // обновляем отображаемые значения
    });

    $('#submitValues').click(function(){
        var dataToSend = {
            values: previousValues,
            totalAmount: totalAmount
        }; // данные для отправки

        $.ajax({
            type: "POST",
            url: "create_order", // Замените на свой URL
            data: JSON.stringify(dataToSend), // отправляем данные в формате JSON
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                if (data.status === 'success') {
                    console.log("Данные успешно отправлены:", data);

                    // Отображаем "Заказ создан!" в центре экрана на 1 секунду
                    var orderCreatedDiv = $('<div id="orderCreated">Заказ создан!</div>');
                    $('body').append(orderCreatedDiv);
                    orderCreatedDiv.fadeIn('fast');
                    setTimeout(function () {
                        orderCreatedDiv.fadeOut('fast', function() {
                            orderCreatedDiv.remove();
                        });
                    }, 1000);

                    // Очищаем предыдущие выбранные товары
                    previousValues = [];
                    totalAmount = 0;

                    // Обновляем отображение
                    updateResult();

                    // Перенаправляем пользователя
                    window.location.href = data.redirect;  // Или используйте другой метод перенаправления
                } else {
                    console.error("Ошибка отправки данных:", data);
                }
            },
            error: function(xhr, status, error){
                console.error("Ошибка отправки данных:", error);

                // Если произошла ошибка, также выполните очистку и обновление отображения
                previousValues = [];
                totalAmount = 0;
                updateResult();
            }
        });
    });

     function updateResult(){
        resultDiv.html(''); // очищаем содержимое
        previousValues.forEach((item, index) => {
            resultDiv.append(`<div>${item.name} - Цена: ${item.price.toFixed(2)} руб <button class="delete-item" data-index="${index}">Удалить</button></div>`); // добавляем каждый элемент списка со ссылкой для удаления
        });
        $('#totalAmount').text("Общая сумма: " + totalAmount.toFixed(2) + " руб"); // выводим общую сумму
    }
});