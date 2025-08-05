document.addEventListener('DOMContentLoaded', function () {
    // 0) Если контейнера для тостов нет — создаём его
    if (!document.getElementById('toast-container')) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        Object.assign(container.style, {
            position: 'fixed',
            bottom: '30px',            // отступ от низа
            left: '50%',               // центр по горизонтали
            transform: 'translateX(-50%)', // учёт ширины контейнера
            zIndex: '1055',
            pointerEvents: 'none'      // чтобы клики проходили сквозь
        });
        document.body.appendChild(container);
    }

    // Функция показа тоста
    function showToast(message, type = 'success', duration = 3000) {
        const toastContainer = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = 'toast-message';
        if (type === 'error') toast.classList.add('error');
        toast.innerText = message;
        toastContainer.appendChild(toast);
        // плавное появление
        setTimeout(() => toast.classList.add('show'), 10);
        // скрытие
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    // Обработчики «−» / «+» с тостами на границах
    document.getElementById('minus').addEventListener('click', function () {
        const input = document.getElementById('quantity');
        let v = parseInt(input.value, 10) || 1;
        if (v > 1) {
            input.value = v - 1;
        } else {
            showToast('Мин. количество — 1', 'error');
        }
    });
    document.getElementById('plus').addEventListener('click', function () {
        const input = document.getElementById('quantity');
        let v = parseInt(input.value, 10) || 1;
        if (v < 99) {
            input.value = v + 1;
        } else {
            showToast('Максимум — 99 шт.', 'error');
        }
    });

    // Отправка формы «В корзину» с тостами вместо alert
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
                showToast('Товар добавлен в корзину', 'success');
            } else {
                showToast('Ошибка при добавлении товара', 'error');
            }
        })
        .catch(err => {
            console.error('Ошибка:', err);
            showToast('Не удалось добавить в корзину', 'error');
        });
    });
});