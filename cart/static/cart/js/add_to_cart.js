const form = document.getElementById('cart-form');

form.addEventListener('submit', function (e) {
    e.preventDefault();

    const bookId = document.getElementById('book-id').value;
    const quantity = document.getElementById('quantity').value
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `book_id=${bookId}&quantity=${quantity}`
    })

    alert("Товар добавлен в корзину")
});