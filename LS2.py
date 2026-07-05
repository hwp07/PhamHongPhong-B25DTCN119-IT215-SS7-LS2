"""test case
1. 
    - kết quả hiện tại: 
            {
                "statusCode": 200,
                "message": "Cập nhật thành công",
                "data": null
            }
    - Kết quả mong muốn: 404 Not Found
    - Lỗi phát hiện: 
        + print không làm dừng chương trình
        + không có raise HTTPException(404) mà vẫn trả về được 200 OK



2.
    - kết quả hiện tại: 
        HTTP 200 OK
        {"error": "Trạng thái không hợp lệ"}
    - Kết quả mong muốn: 
        HTTP 400 Bad Request
        {"detail":"Trạng thái không hợp lệ"}
    - Lỗi phảt hiện: trả về return {"error":...} thay vì raise HTTPException(400)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]

# loại bỏ magic string
VALID_STATUS = {"PENDING", "SHIPPING", "DELIVERED"}

class StatusUpdate(BaseModel):
    status: str

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # kiểm tra trạng thái
    if data.status not in VALID_STATUS:
        raise HTTPException(
            status_code=400,
            detail="Trạng thái không hợp lệ"
        )

    # cập nhật trạng thái
    order["status"] = data.status

    return {
        "statusCode": 200,
        "message": "Cập nhật thành công",
        "data": order
    }