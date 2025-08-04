document.addEventListener('DOMContentLoaded', function () {
    // 0) Если контейнера для тостов нет в DOM — добавляем его
    if (!document.getElementById('toast-container')) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        // стили контейнера можно положить в CSS или прописать здесь
        container.style.position = 'fixed';
        container.style.bottom = '30px';
        container.style.left = '50%';
        container.style.transform = 'translateX(-50%)';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
    }

    // 1) Функция показа тоста
    function showToast(message, type = 'success', duration = 3000) {
        const toastContainer = document.getElementById('toast-container');

        const toast = document.createElement('div');
        toast.className = 'toast-message';
        // яркие bootstrap-классы через стили в CSS
        if (type === 'error') {
            toast.classList.add('error');
        }
        toast.innerText = message;

        toastContainer.appendChild(toast);

        // Плавное появление
        setTimeout(() => toast.classList.add('show'), 10);

        // Скрываем через duration
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    // 2) Обработчики «−» / «+» с уведомлениями на границах
    document.getElementById('minus').addEventListener('click', function () {
        const quantityInput = document.getElementById('quantity');
        let value = parseInt(quantityInput.value, 10);
        if (value > 1) {
            quantityInput.value = value - 1;
        } else {
            showToast('Мин. количество — 1', 'error');
        }
    });

    document.getElementById('plus').addEventListener('click', function () {
        const quantityInput = document.getElementById('quantity');
        let value = parseInt(quantityInput.value, 10);
        if (value < 99) {
            quantityInput.value = value + 1;
        } else {
            showToast('Максимум — 99 шт.', 'error');
        }
    });

    // 3) Отправка формы «Добавить в корзину»
    const form = document.getElementById('cart-form');
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const bookId = document.getElementById('book-id').value;
        const quantity = document.getElementById('quantity').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `book_id=${bookId}&quantity=${quantity}`
        })
        .then(response => {
            if (response.ok) {
                showToast("Товар добавлен в корзину", 'success');
            } else {
                showToast("Ошибка при добавлении товара", 'error');
            }
        })
        .catch(error => {
            console.error("Ошибка: ", error);
            showToast("Не удалось добавить в корзину", 'error');
        });
    });
});
