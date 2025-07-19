document.getElementById('minus').addEventListener('click', function () {
    const quantityInput = document.getElementById('quantity');
    let value = parseInt(quantityInput.value);
    if (value > 1) {
        quantityInput.value = value - 1;
    }
});

document.getElementById('plus').addEventListener('click', function () {
    const quantityInput = document.getElementById('quantity');
    let value = parseInt(quantityInput.value);
    if (value < 99) {
        quantityInput.value = value + 1;
    }
})


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
    }).then(response => {
        if (response.ok) {
            alert("Товар добавлен в корзину");
        } else {
            alert("Ошибка при добавлении товара");
        }
    }).catch(error => {
        console.error("Ошибка: ", error)
        alert("Произошла ошибка");
    });


});