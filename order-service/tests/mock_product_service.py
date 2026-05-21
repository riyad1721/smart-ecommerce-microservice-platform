from fastapi import FastAPI, HTTPException

app = FastAPI(title="mock-product-service")

PRODUCTS = {
    "product-1": {
        "id": "product-1",
        "name": "Mechanical Keyboard",
        "price": "2500.00",
        "is_active": True,
        "stock_quantity": 20,
    },
    "product-2": {
        "id": "product-2",
        "name": "Wireless Mouse",
        "price": "900.00",
        "is_active": True,
        "stock_quantity": 50,
    },
}


@app.get("/api/v1/products/{product_id}")
def get_product(product_id: str):
    product = PRODUCTS.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
