import { useEffect, useState } from "react"

function App() {

    const [inventory, setInventory] = useState([])

    const [formData, setFormData] = useState({
        product_name: "",
        barcode: "",
        brand: "",
        quantity: "",
        price: ""
    })

    async function fetchInventory() {

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/inventory"
            )

            const data = await response.json()

            setInventory(data)

        } catch (error) {

            console.log(
                "Error fetching inventory:",
                error
            )
        }
    }

    useEffect(() => {

        fetchInventory()

    }, [])

    function handleChange(event) {

        setFormData({

            ...formData,

            [event.target.name]:
                event.target.value
        })
    }

    async function addItem(event) {

        event.preventDefault()

        try {

            const response = await fetch(

                "http://127.0.0.1:5000/inventory",

                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        ...formData,

                        quantity:
                            Number(formData.quantity),

                        price:
                            Number(formData.price)
                    })
                }
            )

            if (response.ok) {

                fetchInventory()

                setFormData({

                    product_name: "",
                    barcode: "",
                    brand: "",
                    quantity: "",
                    price: ""
                })
            }

        } catch (error) {

            console.log(
                "Error adding item:",
                error
            )
        }
    }

    async function deleteItem(id) {

        try {

            await fetch(

                `http://127.0.0.1:5000/inventory/${id}`,

                {
                    method: "DELETE"
                }
            )

            fetchInventory()

        } catch (error) {

            console.log(
                "Error deleting item:",
                error
            )
        }
    }

    return (

        <div style={{ padding: "20px" }}>

            <h1>
                Inventory Management System
            </h1>

            <form onSubmit={addItem}>

                <input
                    type="text"
                    name="product_name"
                    placeholder="Product Name"
                    value={formData.product_name}
                    onChange={handleChange}
                />

                <br /><br />

                <input
                    type="text"
                    name="barcode"
                    placeholder="Barcode"
                    value={formData.barcode}
                    onChange={handleChange}
                />

                <br /><br />

                <input
                    type="text"
                    name="brand"
                    placeholder="Brand"
                    value={formData.brand}
                    onChange={handleChange}
                />

                <br /><br />

                <input
                    type="number"
                    name="quantity"
                    placeholder="Quantity"
                    value={formData.quantity}
                    onChange={handleChange}
                />

                <br /><br />

                <input
                    type="number"
                    step="0.01"
                    name="price"
                    placeholder="Price"
                    value={formData.price}
                    onChange={handleChange}
                />

                <br /><br />

                <button type="submit">
                    Add Item
                </button>

            </form>

            <hr />

            <h2>Inventory</h2>

            {inventory.length === 0 ? (

                <p>No inventory items found.</p>

            ) : (

                inventory.map((item) => (

                    <div
                        key={item.id}
                        style={{
                            border: "1px solid black",
                            padding: "10px",
                            marginBottom: "10px"
                        }}
                    >

                        <h3>
                            {item.product_name}
                        </h3>

                        <p>
                            Brand: {item.brand}
                        </p>

                        <p>
                            Quantity: {item.quantity}
                        </p>

                        <p>
                            Price: ${item.price}
                        </p>

                        <button
                            onClick={() =>
                                deleteItem(item.id)
                            }
                        >
                            Delete
                        </button>

                    </div>
                ))
            )}

        </div>
    )
}

export default App