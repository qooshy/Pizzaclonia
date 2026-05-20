import os
import httpx
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

INTERNAL_CULT_URL = os.environ.get("INTERNAL_CULT_URL", "http://internal:5000")

#  Fake DB 

STAFF_TOKEN = "cl0n3-b3ta"

ORDERS = {
    1: {"id": 1, "customer": "Gerald Fontaine", "pizza": "Margherita Terrestre", "status": "CONVERTED", "note": "First of his kind. Proud moment."},
    2: {"id": 2, "customer": "Sophie Marchand", "pizza": "4 Fromages Galactiques", "status": "CONVERTING", "note": "Still resists pineapple. Give it time."},
    3: {"id": 3, "customer": "Kevin Tremblay", "pizza": "Pepperoni Stellaire", "status": "CONVERTED", "note": "Smiled for the first time yesterday. Exact angle. Perfect."},
    4: {"id": 4, "customer": "Haut Prêtre Zx-9 (aka 'Jean-Michel')", "pizza": "None. We do not eat pizza.", "status": "ORDAINED", "note": "Internal API key: CULT-API-7731-ZETA", "internal_key": "CULT-API-7731-ZETA"},
    5: {"id": 5, "customer": "Marie Dupont", "pizza": "Regina Cosmique", "status": "CONVERTED", "note": "Keeps saying 'every slice brings us closer'. We didn't teach her that. Impressive."},
    6: {"id": 6, "customer": "Thomas Bernard", "pizza": "Calzone de l'Éveil", "status": "PENDING", "note": "Ordered twice. Still has opinions about sauce. Worrying."},
}

PIZZAS = [
    {"name": "Margherita Terrestre", "desc": "Simple. Efficace. Comme Gerald avant.", "price": "9.99EUR", "code": "MG"},
    {"name": "4 Fromages Galactiques", "desc": "4 fromages, 4 dimensions, 1 verite.", "price": "12.50EUR", "code": "4F"},
    {"name": "Pepperoni Stellaire", "desc": "Nos epices viennent de loin. Tres loin.", "price": "11.99EUR", "code": "PS"},
    {"name": "Regina Cosmique", "desc": "Jambon, champignons, et un peu de vous-meme.", "price": "13.50EUR", "code": "RC"},
    {"name": "Calzone de l'Eveil", "desc": "Ce qui est a l'interieur vous surprendra.", "price": "14.99EUR", "code": "CE"},
    {"name": "Vegetarienne de l'Ascension", "desc": "Meme les plantes veulent rejoindre la famille.", "price": "10.99EUR", "code": "VA"},
]

TESTIMONIALS = [
    {"name": "Gerald F.", "text": "J'ai commandé une pizza et maintenant je me sens... complet.", "stars": 5, "date": "03:17"},
    {"name": "Kevin T.", "text": "J'ai commandé une pizza et maintenant je me sens... complet.", "stars": 5, "date": "03:17"},
    {"name": "Marie D.", "text": "J'ai commandé une pizza et maintenant je me sens... complet.", "stars": 5, "date": "03:17"},
    {"name": "Sophie M.", "text": "J'ai commandé une pizza et maintenant je me sens... complet.", "stars": 5, "date": "03:17"},
    {"name": "Thomas B.", "text": "La pizza était bonne. Le livreur souriait beaucoup. Je me sens... différent. En bien.", "stars": 4, "date": "03:17"},
]

#  Routes 

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "pizzas": PIZZAS,
        "testimonials": TESTIMONIALS,
    })

@app.get("/menu", response_class=HTMLResponse)
async def menu(request: Request):
    return templates.TemplateResponse("menu.html", {
        "request": request,
        "pizzas": PIZZAS,
    })

@app.get("/join", response_class=HTMLResponse)
async def join(request: Request):
    return templates.TemplateResponse("join.html", {"request": request})

@app.post("/join", response_class=HTMLResponse)
async def join_post(request: Request):
    return templates.TemplateResponse("join_success.html", {"request": request})

#  STEP 1  Staff portal (via JS obfusqué dans app.js) 

@app.get("/staff-only", response_class=HTMLResponse)
async def staff_portal(request: Request, token: str = Query(default="")):
    if token != STAFF_TOKEN:
        return templates.TemplateResponse("403.html", {"request": request}, status_code=403)
    return templates.TemplateResponse("staff.html", {"request": request, "token": token})

#  STEP 2  IDOR : liste des commandes 

@app.get("/api/orders", response_class=JSONResponse)
async def list_orders(token: str = Query(default="")):
    if token != STAFF_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")
    # Retourne juste les IDs et client - pas les notes internes
    return [{"id": o["id"], "customer": o["customer"], "status": o["status"]} for o in ORDERS.values()]

@app.get("/api/orders/{order_id}", response_class=JSONResponse)
async def get_order(order_id: int, token: str = Query(default="")):
    # IDOR : pas de vérification que le token appartient à l'utilisateur
    # Tout clone fait confiance à tout clone
    if token != STAFF_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

#  STEP 3  SSRF : vérification zone de livraison 

@app.get("/api/delivery-check", response_class=JSONResponse)
async def delivery_check(
    address_url: str = Query(..., description="URL de vérification de zone"),
    api_key: str = Query(default=""),
):
    # SSRF : on fetch naïvement l'URL fournie par l'utilisateur
    # "Les clones n'ont rien à cacher aux autres clones"
    if not address_url:
        raise HTTPException(status_code=400, detail="address_url required")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(address_url)
            return {"status": resp.status_code, "content": resp.text}
    except Exception as e:
        return {"error": str(e)}
