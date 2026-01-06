from fastapi import FastAPI
from api.routers.tasks import router as tasks_router
from api.routers.user import router as user_router
from api.routers.client import router as client_router
from api.routers.company import router as company_router
from api.routers.sales import router as sales_router
from api.routers.contact import router as contact_router
from api.routers.department import router as department_router
from api.routers.purchase_details import router as purchase_detail_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://custmanage-frontend.onrender.com"],  # ← フロントのURL
    allow_credentials=True,
    allow_methods=["*"],  # ← OPTIONS, POST, GET などを許可
    allow_headers=["*"],
)

app.include_router(tasks_router,tags=["tasks"])
app.include_router(user_router,tags=["users"])
app.include_router(client_router,tags=["clients"])
app.include_router(company_router,tags=["companies"])
app.include_router(sales_router,tags=["sales"])
app.include_router(contact_router,tags=["contacts"])
app.include_router(department_router,tags=["departments"])
app.include_router(purchase_detail_router,tags=["purchase_details"])





