import requests

# L'URL de cerca de Open Food Facts
# 'search_terms' és l'equivalent al 'q' o 'ingr' d'Edamam
query = "pizza"
url = f"https://es.openfoodfacts.org/cgi/search.pl?search_terms={query}&action=process&json=1"
headers = {
    'User-Agent': 'project - Python - Version 1.0'
}
response = requests.get(url,headers=headers)
response.raise_for_status()

data = response.json()
productes = data.get('products', [])

print(f"S'han trobat {len(productes)} productes per a '{query}':\n")

for p in productes:  # Mostrem els 5 primers
    
    nom = p.get('product_name', 'Nom no disponible')
    marca = p.get('brands', 'Marca desconeguda')
    nutriscore = p.get('nutriscore_grade', 'N/A').upper()
    nutrients=p.get('nutriments','No info')
    
    print(f" {nom} ({marca})")
    print(f"   Nutriscore: {nutriscore}")
    print(nutrients)
    print("-" * 30)