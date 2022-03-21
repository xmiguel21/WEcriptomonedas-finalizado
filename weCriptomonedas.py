from bs4 import BeautifulSoup
import requests

# paguina web principal
url = 'https://coinmarketcap.com/es/'
page = requests.get(url)
cont = page.text
soup = BeautifulSoup(cont, 'lxml')
box = soup.find('html', lang='es')

listaMonedas = []
lista_img = []

# enlaces de las monedas de la pagina web
lista_paginas = []
con = 0
for x in box.find('tbody'):
    links = x.find('div', attrs={'display': 'flex', 'class': 'sc-16r8icm-0 escjiH'})
    links = links.find('a').__getitem__('href')
    lista_paginas.append('https://coinmarketcap.com' + links)
    con = con + 1
    if con == 10:
        break

# guardando los datos de las monedas en la lista de monedas
for x in range(len(lista_paginas)):

    # extracion del codigo html de la paguina web entregada
    url = lista_paginas[x]

    page1 = requests.get(url)
    cont1 = page1.text

    soup2 = BeautifulSoup(cont1, 'lxml')

    # extracion de las imagenes de las monedas
    imagenes = soup2.find('div', class_='sc-16r8icm-0 gpRPnR nameHeader')
    imagenes = imagenes.find('img').__getitem__('src')
    lista_img.append(imagenes)

    # siglas de la moneda
    v = soup2.find('div', class_='sc-16r8icm-0 kjciSH priceSection')
    moneda = soup2.find('small', class_='nameSymbol').get_text()

    # obtencion del valor de la moneda
    optencion_valor = v.find('div', class_='sc-16r8icm-0 kjciSH priceTitle')
    valor = optencion_valor.find('div', class_='priceValue').get_text()


    # precio minimo
    minimo = v.find('span', class_='n78udj-5 dBJPYV').get_text()

    # precio maximo
    x = soup2.find('div', class_='sc-16r8icm-0 SjVBR')
    maximo = x.find('span', class_='n78udj-5 dBJPYV').get_text()

    # obtencion del volumen capital de la moneda
    con = 0
    a = soup2.find('div', class_='sc-16r8icm-0 fggtJu statsSection')
    for volu in a.findAll('div', class_='statsBlock'):
        if con == 2:
            for q in volu:
                if con == 3:
                    volumen = q.find('div', class_='statsValue').get_text()
                con = con + 1
        con = con + 1

    # optencion de nombre de la moneda
    tex2 = soup2.find('h2', class_='sc-1q9q90x-0 jCInrl h1')
    titulo2 = tex2.get_text()

    # extracion de dominio capital y el nivel de mercado
    con = 0
    dominio = ''
    nivel = ''
    for x in soup2.find('tbody'):
        if con == 5:
            do = x.find('span', class_=True)
            for i in do:
                dominio = dominio + i
        if con == 6:
            n = x.find('td')
            for i in n:
                nivel = nivel + i
        con = con + 1

    # extracion de la capitalizacion del mercado precio actual por suministro circulante
    con = 0
    for x in soup2.find('div', class_='sc-16r8icm-0 nds9rn-0 dAxhCK'):
        if con == 2:
            c = x.find('span')
            for i in c:
                capital = i
        con = con + 1

    # agregando los datos de la moneda extraida
    listaMonedas.append(titulo2)
    listaMonedas.append(valor)
    listaMonedas.append(minimo)
    listaMonedas.append(maximo)
    listaMonedas.append(volumen)
    listaMonedas.append(moneda)
    listaMonedas.append(dominio)
    listaMonedas.append(nivel)
    listaMonedas.append(capital)


#funcion encargada de recibir un numero tipo texto y lo tranforma a un numero con decimal
def numero(monto):
    b=[]
    a = ''
    for q in monto:
        if ord(q)>47 and ord(q)<58 or q=='.':
            a=a+q
            str(a)
    b.append(a)
    for x in b:
        c=float(x)
    return c

#se encarga de sacar el promedio entre el valor minimo y maximo entregados
def media(numero1,numero2):
    resultado=(numero1+numero2)/2
    return resultado

#devuelve un Si si el valor es mayor al promedio que tiene la moneda durante el dia
#devuelve un No si el valor es menor al promedio que tiene la moneda durante el dia
#devuelve un - si el valor es igual al promedio que tiene la moneda durante el dia
def invercion(numero1,numero2,monto):
    a = numero(monto)
    b = numero(numero1)
    c = numero(numero2)
    d=''
    if media(c,b)>a:
        d ='No'
    elif media(c,b)<a:
        d = 'Si'
    else:
        d = '-'
    return d

