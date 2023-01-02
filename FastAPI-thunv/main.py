from fastapi import FastAPI, Request, Body
import database
import model

app = FastAPI()

@app.get("/category/get-by-id/{category_id}")
def get_category_by_id(category_id):
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        category_obj = session.query(model.CategoriesORM).filter(
            model.CategoriesORM.id.__eq__(int(category_id))
        ).first()
        if category_obj:
            msg = "Lấy chi tiết danh mục thành công!!!"
            status = 1
            data = {
                "category": category_obj
            }
        else:
            msg = "Không tìm thấy !!!"
    except Exception as ex:
        msg = str(ex)
    finally:
        session.close()
    return {
        "status": status,
        "message": msg,
        "data": data
    }
@app.get("/category/get-all-categories")
def get_all_categories():
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        list_category_obj = session.query(model.CategoriesORM).all()
        if list_category_obj:
            msg = "Lấy tất cả danh mục thành công!!!"
            status = 1
            data = {
                "list_categories": list_category_obj
            }
        else:
            msg = "Không tìm thấy !!!"
    except Exception as ex:
        msg = str(ex)
    finally:
        session.close()
    return {
        "status": status,
        "message": msg,
        "data": data
    }

@app.post("/category/insert-category")
def insert_category( payload: dict = Body(...)):
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        category_name = payload.get("name")
        obj = model.CategoriesORM(name = category_name)
        session.add(obj)
        session.commit()
        msg = "Thêm mới danh mục thành công!!!"
        status = 1
        data = {
            "category": {
                "id": obj.id,
                "name": obj.name
            }
        }
    except Exception as ex:
        msg = str(ex)
    finally:
        session.close()
    return {
        "status": status,
        "message": msg,
        "data": data
    }
@app.put("/category/update-category")
def update_category(payload: dict = Body(...)):
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        category_name = payload.get("name")
        category_id = payload.get("id")
        category_obj = session.query(model.CategoriesORM).filter(
            model.CategoriesORM.id.__eq__(int(category_id))
        ).first()
        if category_obj:
            category_obj.name = category_name
            session.commit()
            msg ,status = "Cập nhật danh mục thành công!!!", 1
            data = {
                "category": {
                    "id": category_obj.id,
                    "name": category_obj.name
                }
            }
        else:
            msg = "Không tìm thấy !!!"
    except Exception as ex:
        msg = str(ex)
    finally:
        session.close()
    return {"status": status,"message": msg,"data": data}

@app.delete("/category/delete-by-id/{category_id}")
def delete_category_by_id(category_id):
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        category_obj = session.query(model.CategoriesORM).filter(
            model.CategoriesORM.id.__eq__(int(category_id))
        ).first()
        if category_obj:
            session.delete(category_obj)
            session.commit()
            msg = "Xóa danh mục thành công!!!"
            status = 1
        else:
            msg = "Không tìm thấy !!!"
    except Exception as ex:
        msg = str(ex)
    finally:
        session.close()
    return {
        "status": status,
        "message": msg,
        "data": data
    }
