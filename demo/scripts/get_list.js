document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#form').onsubmit = () => {
        const request = new XMLHttpRequest();
        const id = document.querySelector('#id').value;
        request.open('POST', '/get-order');
        request.onload = () => {

            const data = JSON.parse(request.responseText);
            document.querySelector('#r_id').innerHTML = 'ID: ';
            document.querySelector('#order_name').innerHTML = 'Name: ';
            document.querySelector('#status').innerHTML = 'Completed: ';
            document.querySelector('#date').innerHTML = "Date created: ";
            document.querySelector('#date_comp').innerHTML = "Date completed: ";
            document.querySelector("#item_list").innerHTML = ''
            document.querySelector('#confirm').disabled = true;
            document.querySelector('#check').disabled = true;
            document.querySelector('#delete').disabled = true;
            document.querySelector('#addItem').disabled = true;
            document.querySelector('#removeItem').disabled = true;
            document.querySelector('#updateQuantity').disabled = true;
            if (data.success) {
                if (data.found) {
                    if (data.status == false) {
                        document.querySelector('#confirm').disabled = false;
                        document.querySelector('#check').disabled = false;
                        document.querySelector('#delete').disabled = false;
                        document.querySelector('#addItem').disabled = false;
                        document.querySelector('#removeItem').disabled = false;
                        document.querySelector('#updateQuantity').disabled = false;
                    }
                    const r_id = data.id;
                    const name = data.name
                    const item = data.item;
                    const quantity = data.quantity;
                    const status = data.status;
                    const date = data.date;
                    const comp = data.comp
                    document.querySelector('#r_id').innerHTML = `ID: ${r_id}`;
                    document.querySelector('#order_name').innerHTML = `Name: ${name}`;
                    document.querySelector('#status').innerHTML = `Completed: ${status}`
                    document.querySelector('#date').innerHTML = `Date created: ${date}`;
                    document.querySelector('#date_comp').innerHTML = `Date completed: ${comp}`;
                    var i
                    for (i = 0; i < item.length; i++) {
                        var l = `Item: ${item[i]} ------------------------ Quantity: ${quantity[i]}`
                        document.querySelector("#item_list").innerHTML += ('<li>' + l + '</li>')
                    }
                 }
                 else {
                    alert(data.msg);
                 }
            }
            else {
                alert("There was an error!")
            }
        }
        const data = new FormData();
        data.append('id', id);
        request.send(data);
        return false;
    };

    document.querySelector('#check').onclick = () => {
        const request = new XMLHttpRequest();
        const id = document.querySelector('#id').value;
        request.open('POST', '/check-order');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.success) {
                   var ul = document.getElementById("cpu_list")
            }
            else {
                alert("There was an error please try again!")
            }
        }
        const data = new FormData();
        data.append('id', id);
        request.send(data);
        return false;
    }

    document.querySelector('#confirm').onclick = () => {
        const request = new XMLHttpRequest();
        const id = document.querySelector('#id').value;
        request.open('POST', '/confirm-order');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.success) {
                if (data.done) {
                    document.querySelector('#confirm').disabled = true;
                    document.querySelector('#check').disabled = true;
                    document.querySelector('#delete').disabled = true;
                    document.querySelector('#addItem').disabled = true;
                    document.querySelector('#removeItem').disabled = true;
                    document.querySelector('#updateQuantity').disabled = true;
                    document.querySelector('#status').innerHTML = 'Completed: true';
                    document.querySelector('#date_comp').innerHTML = `Date completed: ${data.comp}`;
                    alert(data.msg)
                }
                else {
                    alert(data.msg)
                }
            }
            else {
                alert("There was an error please try again!")
            }
        }
        const data = new FormData();
        data.append('id', id);
        request.send(data);
        return false;
    }

    document.querySelector('#delete').onclick = () => {
        const request = new XMLHttpRequest();
        const id = document.querySelector('#id').value;
        request.open('POST', '/delete-order');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.success) {
                if (data.done) {
                    document.querySelector('#confirm').disabled = true;
                    document.querySelector('#check').disabled = true;
                    document.querySelector('#delete').disabled = true;
                    document.querySelector('#addItem').disabled = true;
                    document.querySelector('#removeItem').disabled = true;
                    document.querySelector('#updateQuantity').disabled = true;
                    document.querySelector('#r_id').innerHTML = 'ID: ';
                    document.querySelector('#order_name').innerHTML = 'Name: ';
                    document.querySelector('#status').innerHTML = 'Completed: ';
                    document.querySelector("#item_list").innerHTML = ''
                    document.querySelector('#date').innerHTML = "Date created: ";
                    document.querySelector('#date_comp').innerHTML = "Date completed: ";

                    alert(data.msg)
                }
                else {
                    alert(data.msg)
                }
            }
            else {
                alert("There was an error please try again!")
            }
        }
        const data = new FormData();
        data.append('id', id);
        request.send(data);
        return false;
    }


});