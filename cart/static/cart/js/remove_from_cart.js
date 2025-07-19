document.addEventListener('DOMContentLoaded', function() {
    // Находим все кнопки удаления
    const deleteButtons = document.querySelectorAll('.del-btn');
    
    // Для каждой кнопки добавляем обработчик
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Находим родительскую строку товара
            const row = this.closest('.cart-item');
            // Получаем ID книги из data-атрибута
            const bookId = row.getAttribute('data-book-id');
            
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch('/cart/delete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `book_id=${bookId}`
            })
            .then(response => {
                if (response.ok) {
                    // Удаляем строку из таблицы
                    row.remove();
                    // Обновляем страницу после небольшой задержки
                    setTimeout(() => {
                        location.reload();
                    }, 300);
                } else {
                    alert("Ошибка при удалении товара");
                }
            })
            .catch(error => {
                console.error("Ошибка: ", error);
                alert("Произошла ошибка");
            });
        });
    });
});