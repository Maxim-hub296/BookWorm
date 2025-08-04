document.addEventListener('DOMContentLoaded', function () {
    // 1) Функция пересчёта суммы в строке
    function recalcRow(bookId, newQty) {
        const priceEl = document.querySelector(`.cart-item[data-book-id="${bookId}"] .fw-medium`);
        // вытаскиваем число из "123.45 руб."
        const price = parseFloat(priceEl.textContent.replace(/[^\d.]/g, '')) || 0;
        const totalEl = document.querySelector(`.item-total[data-book-id="${bookId}"]`);
        totalEl.textContent = (price * newQty).toFixed(2) + ' руб.';
    }

    // 2) Функция пересчёта общего количества и суммы корзины
    function recalcCart() {
        let itemsTotal = 0, cartSum = 0;
        document.querySelectorAll('.cart-item').forEach(row => {
            const id = row.dataset.bookId;
            const qty = +row.querySelector(`.item-quantity[data-book-id="${id}"]`).value;
            const total = parseFloat(
                row.querySelector(`.item-total[data-book-id="${id}"]`)
                    .textContent.replace(/[^\d.]/g, '')
            ) || 0;
            itemsTotal += qty;
            cartSum += total;
        });
        // Обновляем DOM
        document.querySelector('.item-count').textContent = `Товары (${itemsTotal} шт.):`;
        document.querySelectorAll('.cart-total').forEach(el => {
            el.textContent = cartSum.toFixed(2) + ' руб.';
        });
    }

    // 3) Объект для хранения таймаутов по каждой книге
    const pendingUpdates = {}; // { [bookId]: timeoutID }

    // 4) Отправка одного запроса к серверу
    function sendUpdate(bookId, action) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch('/cart/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `book_id=${bookId}&action=${action}`
        })
            .then(resp => resp.json())
            .catch(err => {
                console.error('Ошибка при обновлении на сервере:', err);
            });
    }

    // 5) Планируем дебаунс-запрос: отправляем через 1 секунду после последнего клика
    function scheduleUpdate(bookId, action) {
        if (pendingUpdates[bookId]) {
            clearTimeout(pendingUpdates[bookId]);
        }
        pendingUpdates[bookId] = setTimeout(() => {
            sendUpdate(bookId, action);
            delete pendingUpdates[bookId];
        }, 1000);
    }

    // 6) Обработчик клика по кнопкам увеличения/уменьшения
    document.querySelectorAll('.btn-update').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const bookId = this.dataset.bookId;
            const action = this.dataset.action;

            // Оптимистично меняем количество в input
            const qtyInput = document.querySelector(`.item-quantity[data-book-id="${bookId}"]`);
            let qty = +qtyInput.value;
            if (action === 'increase') {
                qty++;
            } else if (action === 'decrease') {
                qty = Math.max(1, qty - 1);
            }
            qtyInput.value = qty;

            // Пересчитываем строку и корзину
            recalcRow(bookId, qty);
            recalcCart();

            // Планируем запрос на сервер
            scheduleUpdate(bookId, action);
        });
    });
});
