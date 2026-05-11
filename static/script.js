let cart = [];
let total = 0;

// Fetch menu items from the Python backend
document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/menu')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('menu-container');
            data.forEach(item => {
                const card = document.createElement('div');
                card.className = 'menu-card';
                card.innerHTML = `
                    <h3>${item.name}</h3>
                    <span class="category-badge">${item.category}</span>
                    <span class="price">₹${item.price.toFixed(2)}</span>
                    <button onclick="addToCart(${item.id}, '${item.name}', ${item.price})">Add to Order</button>
                `;
                container.appendChild(card);
            });
        });
});

function addToCart(id, name, price) {
    cart.push({ id, name, price });
    total += price;
    updateCartUI();
}

function updateCartUI() {
    const cartList = document.getElementById('cart-items');
    cartList.innerHTML = '';
    
    cart.forEach((item, index) => {
        const li = document.createElement('li');
        li.innerHTML = `<span>${item.name}</span> <span>₹${item.price.toFixed(2)}</span>`;
        cartList.appendChild(li);
    });
    
    document.getElementById('total-price').innerText = total.toFixed(2);
}

function checkout() {
    if (cart.length === 0) {
        alert("Your order list is empty!");
        return;
    }
    alert(`Order placed successfully! Total amount: ₹${total.toFixed(2)}. Your food is being prepared.`);
    cart = [];
    total = 0;
    updateCartUI();
}