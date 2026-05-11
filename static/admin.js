// Fetch orders immediately, then every 3 seconds
fetchOrders();
setInterval(fetchOrders, 3000);

function fetchOrders() {
    fetch('/api/all_orders')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('orders-table-body');
            tbody.innerHTML = ''; // Clear table
            
            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No active orders right now!</td></tr>';
                return;
            }

            data.forEach(order => {
                // Format the items list nicely
                let itemsList = order.items.map(i => i.name).join(', ');
                
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>#${order.id}</strong></td>
                    <td>${itemsList}</td>
                    <td>₹${order.total.toFixed(2)}</td>
                    <td><strong>${order.status}</strong></td>
                    <td>
                        <button class="btn-ready" onclick="updateStatus(${order.id}, 'Ready for Pickup 🛎️')">Mark Ready</button>
                        <button class="btn-done" onclick="updateStatus(${order.id}, 'Completed ✅')">Done</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        });
}

function updateStatus(orderId, newStatus) {
    fetch('/api/update_order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_id: orderId, status: newStatus })
    }).then(() => {
        fetchOrders(); // Refresh table immediately
    });
}