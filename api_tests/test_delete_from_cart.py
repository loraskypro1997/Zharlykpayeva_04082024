
import requests

def test_delete_from_cart():
    url = "https://altaivita.ru/engine/cart/delete_products_from_cart_preview.php"
    payload = {
        "product_id": 4131,
        "this_listId": "product_cart",
        "parent_product": "4131",
        "LANG_key": "ru",
        "S_wh": "1",
        "S_CID": "b041a8a7c43d580fcba64f9023cfa3a1",
        "S_cur_code": "usd",
        "S_koef": "0.01441",
        "quantity": "1",
        "S_hint_code": "",
        "S_customerID": ""
    }
    response = requests.post(url, data=payload)
    assert response.status_code == 200, "Status code is not 200"
