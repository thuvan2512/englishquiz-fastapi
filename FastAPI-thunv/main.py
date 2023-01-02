from fastapi import FastAPI, Request, Body
import database
import model
import utils
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Demo FastAPI",
        version="1.0",
        description="This is a simple project to demo fast api - thunv2512",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI()
app.openapi = custom_openapi

@app.get("/")
def index():
    return {
        "message": "go to http://localhost:8000/docs or http://127.0.0.1:8000/docs"
    }

@app.get("/category/get-by-id/{category_id}",tags=["category"])
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
@app.get("/category/get-all-categories",tags=["category"])
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

@app.post("/category/insert-category",tags=["category"])
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
@app.put("/category/update-category",tags=["category"])
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

@app.delete("/category/delete-by-id/{category_id}",tags=["category"])
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

@app.get("/question/get-by-id/{question_id}",tags=["question"])
def get_question_by_id(question_id):
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        question_obj = session.query(model.QuestionORM).filter(
            model.QuestionORM.id.__eq__(str(question_id))
        ).first()
        if question_obj:
            msg = "Lấy chi tiết câu hỏi thành công!!!"
            status = 1
            data = {
                "question": question_obj
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
@app.get("/question/get-all-questions",tags=["question"])
def get_all_questions():
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        list_question_obj = session.query(model.QuestionORM).all()
        if list_question_obj:
            msg = "Lấy tất cả câu hỏi thành công!!!"
            status = 1
            data = {
                "list_question": list_question_obj
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

@app.post("/question/insert-question",tags=["question"])
def insert_question( payload: dict = Body(...)):
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        id = utils.generate_uuid()
        content = payload.get("content")
        category_id = payload.get("category_id")
        if session.query(model.CategoriesORM).filter(model.CategoriesORM.id.__eq__(int(category_id))).first() is not None:
            obj = model.QuestionORM(id = id,content = content,category_id = int(category_id))
            session.add(obj)
            session.commit()
            msg = "Thêm mới câu hỏi thành công!!!"
            status = 1
            data = {
                "question": {
                    "id": obj.id,
                    "content": obj.content,
                    "category_id": obj.category_id
                }
            }
        else:
            msg = "Danh mục không tồn tại!!!"
    except Exception as ex:
        msg = str(ex)
    finally:
        session.close()
    return {
        "status": status,
        "message": msg,
        "data": data
    }
@app.put("/question/update-question",tags=["question"])
def update_category(payload: dict = Body(...)):
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        id = payload.get("id")
        content = payload.get("content")
        category_id = payload.get("category_id")
        obj = session.query(model.QuestionORM).filter(model.QuestionORM.id.__eq__(id)).first()
        if obj:
            if category_id:
                if session.query(model.CategoriesORM).filter(model.CategoriesORM.id.__eq__(int(category_id))).first() is not None:
                    obj.category_id = int(category_id)
                else:
                    raise Exception("Danh mục không tồn tại!!!")
            if content:
                obj.content = content
            session.commit()
            msg = "Cập nhật thành công!!!"
            status = 1
            data = {
                "question": {
                    "id": obj.id,
                    "content": obj.content,
                    "category_id": obj.category_id
                }
            }
        else:
            msg = "Câu hỏi không tồn tại!!!"
    except Exception as ex:
        msg = str(ex)
    finally:
        session.close()
    return {"status": status,"message": msg,"data": data}

@app.delete("/question/delete-by-id/{question_id}",tags=["question"])
def delete_question_by_id(question_id):
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        question_obj = session.query(model.QuestionORM).filter(
            model.QuestionORM.id.__eq__(question_id)
        ).first()
        if question_obj:
            session.delete(question_obj)
            session.commit()
            msg = "Xóa câu hỏi thành công!!!"
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

@app.post("/choice/insert-choice",tags=["choice"])
def insert_choice( payload: dict = Body(...)):
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        id = utils.generate_uuid()
        content = payload.get("content")
        question_id = payload.get("question_id")
        is_correct = payload.get("is_correct")
        if session.query(model.QuestionORM).filter(model.QuestionORM.id.__eq__(question_id)).first() is not None:
            obj = model.ChoiceORM(id = id,content = content,question_id = question_id, is_correct = is_correct)
            session.add(obj)
            session.commit()
            msg = "Thêm mới câu trả lời thành công!!!"
            status = 1
            data = {
                "choice": {
                    "id": obj.id,
                    "content": obj.content,
                    "is_correct": obj.is_correct,
                    "question_id": obj.question_id
                }
            }
        else:
            msg = "Câu hỏi không tồn tại!!!"
    except Exception as ex:
        msg = str(ex)
    finally:
        session.close()
    return {
        "status": status,
        "message": msg,
        "data": data
    }

@app.delete("/choice/delete-by-id/{choice_id}",tags=["choice"])
def delete_choice_by_id(choice_id):
    status, msg, data = 0, None, None
    session = database.get_database_session()
    try:
        choice_obj = session.query(model.ChoiceORM).filter(
            model.ChoiceORM.id.__eq__(choice_id)
        ).first()
        if choice_obj:
            session.delete(choice_obj)
            session.commit()
            msg = "Xóa câu trả lời thành công!!"
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