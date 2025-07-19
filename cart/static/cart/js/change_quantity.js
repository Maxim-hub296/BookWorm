document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-update').forEach(button => {
        button.addEventListener('click', function () {
            const bookId = this.getAttribute('data-book-id');
            const action = this.getAttribute('data-action');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;


            fetch('/cart/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `book_id=${bookId}&action=${action}`
            })
                .then(response => response.json())
                .then(data => {
                    const quantityInput = document.querySelector(`.item-quantity[data-book-id="${bookId}"]`);
                    quantityInput.value = data.new_quantity

                    const itemTotal = document.querySelector(`.item-total[data-book-id="${bookId}"]`);
                    itemTotal.textContent = data.item_total + ' руб.';

                    const itemCount = document.querySelector('.item-count');
                    itemCount.textContent = `Товары (${data.items_total} шт.):`;



                    document.querySelectorAll('.cart-total').forEach(el => {
                        el.textContent = data.cart_total + ' руб.'
                    });


                }).catch(error => {
                console.error('Ошибка:', error);
                alert(`Произошла ошибка: ${error}`);
            });
        });
    });
});