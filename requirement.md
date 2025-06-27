# requirements pour Smart Saha Marketplace
Copier le code
## Core
Django>=4.2,<5.0
djangorestframework>=3.14
psycopg2-binary>=2.9

## Auth JWT (Supabase-compatible)
djangorestframework-simplejwt>=5.3

## CORS headers (frontend ↔ backend)
django-cors-headers>=4.3

## Documentation API (Swagger/Redoc)
drf-spectacular>=0.27

## Tests & outils
pytest>=7.4
pytest-django>=4.5
black>=24.3
isort>=5.13

## Environnement (.env)
python-dotenv>=1.0

## (optionnel pour image ou fichiers dans les annonces)
Pillow>=10.0
📌 Bonus : installation rapide
bash
Copier le code
pip install -r requirements.txt
