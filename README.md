# Projecte Web - Aplicació Django

## 1. Informació general

Assignatura: Projecte Web  
Curs: 2025/2026  
Professors: Roberto Garcia i David Sarrat  

Repositori del projecte:  
https://github.com/DiogoPires2003/projecteWeb.git  

Aquest projecte consisteix en el desenvolupament d’una aplicació web utilitzant el framework Django, seguint els requisits definits a l’enunciat de la pràctica.

---

## 2. Model de dades

La base de dades utilitzada és la mateixa que es va definir a la primera entrega del projecte. Aquesta decisió s’ha pres amb l’objectiu de mantenir la coherència entre fases i aprofitar un model que ja havia estat validat prèviament.

El model està format per diverses entitats relacionades entre si, complint amb el requisit d’incloure com a mínim tres entitats amb relacions significatives. A més, s’ha mantingut una estructura relacional coherent i normalitzada per garantir la integritat de les dades.

---

## 3. Sistema d’autenticació

Per a la gestió d’usuaris, s’ha utilitzat el sistema d’autenticació integrat de Django (`django.contrib.auth`). Aquest sistema permet gestionar de manera segura el registre i l’inici de sessió dels usuaris.

S’han implementat les funcionalitats següents:
- Registre d’usuaris
- Inici i tancament de sessió
- Restricció d’accés a determinades funcionalitats segons autenticació

Aquesta decisió s’ha pres per garantir un nivell adequat de seguretat, evitar implementar mecanismes propis innecessaris i facilitar la integració amb la resta del framework.

---

## 4. Interfície d’usuari

Pel que fa a la interfície, s’ha optat per un disseny senzill, clar i funcional. L’objectiu principal ha estat garantir una bona experiència d’usuari i facilitar la navegació per l’aplicació.

S’han utilitzat colors neutres combinats amb un color principal per destacar accions importants. Aquesta elecció respon a criteris de llegibilitat, coherència visual i accessibilitat.

---

## 5. Navegació i visualització de dades

S’han desenvolupat diferents pàgines que permeten interactuar amb les dades de l’aplicació, com ara:
- Pàgines de llistat d’elements
- Pàgines de detall
- Pàgina principal

Aquestes funcionalitats permeten explorar la informació sense necessitat d’accedir al panell d’administració, millorant així la usabilitat general del sistema.

---

## 6. Panell d’administració

S’ha activat el panell d’administració de Django per permetre la gestió de les dades de manera eficient. A través d’aquest panell es poden crear, modificar i eliminar instàncies de les diferents entitats del sistema.

Aquesta funcionalitat és especialment útil durant el desenvolupament i les proves, així com per complir amb els requisits de la pràctica.

---

## 7. Desplegament amb Docker

El projecte inclou una configuració basada en Docker i docker-compose que permet executar l’aplicació de manera senzilla i reproduïble.

Aquesta decisió facilita el desplegament en diferents entorns i assegura que l’aplicació funcioni de manera consistent independentment del sistema on s’executi.

---

## 8. Bones pràctiques (12-factor)

En la mesura del possible, el desenvolupament ha seguit les recomanacions del model 12-factor, especialment en aspectes com:
- Separació entre configuració i codi
- Ús de variables d’entorn
- Facilitat de desplegament

Aquest enfocament millora la mantenibilitat i escalabilitat de l’aplicació.

---

## 9. Instruccions d’execució

Requisits previs:
- Docker
- Docker Compose

Per executar l’aplicació, cal executar la següent comanda:

```bash
docker-compose up --build