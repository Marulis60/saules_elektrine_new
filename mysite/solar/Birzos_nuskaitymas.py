import requests
from bs4 import BeautifulSoup
import csv
import datetime


# sukuria stulpelį, kuriame parodomas indeksas, kelinta pagal didį kaina
def rusiuoti(elektros_kainos):
    global indeksas
    indeksas = []
    for x in range(24):
        indeksas.append(0)
    for i in range(24):
        maziausia = 10000.
        for j in range(24):
            if elektros_kainos[j] == '-': elektros_kainos[j] = 0.0
            if maziausia > float(elektros_kainos[j]) and indeksas[j] == 0:
                laikina = j
                maziausia = elektros_kainos[j]
        indeksas[laikina] = i + 1
    return indeksas


# sukuria stulpelį, penkios mažiausios reikšmės paleidžia akumuliatoriaus įkrovimą "start"
def ijungti_ikrovima(indeksas):
    global start_in
    start_in = []
    for x in range(24):
        start_in.append('null')
    for x in range(24):
        if indeksas[x] <= 5:
            start_in[x] = 'start'
    return start_in


# sukuria stulpelį, penkis didžiausios reikšmės paleidžia akumuliatoriaus iškrovimą "start"
def įjungti_iskrovima(indeksas):
    global start_out
    start_out = []
    for x in range(24):
        start_out.append('null')
    for x in range(24):
        if indeksas[x] >= 19:
            start_out[x] = 'start'
    return start_out


def surusiuoti(elektros_kainos):
    rusiuoti(elektros_kainos)
    ijungti_ikrovima(indeksas)
    įjungti_iskrovima(indeksas)
    return indeksas, start_in, start_out


# kas dieną nuskaitome NordPool duomenis iš internetinio psl (18 val. būna nauji duomenys)
bandom_nuskaityti = True
# while bandom_nuskaityti:
#     try:
x = datetime.datetime.now()
dabartinis_laikas = int(x.strftime(("%H")))

if dabartinis_laikas >= 10 and dabartinis_laikas < 24:
    # Nuskaitome biržos duomenis
    r = requests.get('https://elektra.p5.lt/?fbclid=IwAR3sGOEDLQ9QyUt3BODzcfoE5xuBc_1MPc0wP6eg1X8xC_RVRky94s7fVjQ')
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    main_lygis = soup.body.main
    sekcija = main_lygis.section.next_sibling.next_sibling
    lentele = sekcija.tbody
    stulpeliai = lentele.find_all('tr')

    #  stulpeliai turi :valandas, kainas ir surušiuotą indeksą
    laikas = []
    kaina = []
    rusiavimas = []
    for i in range(len(stulpeliai)):
        st = lentele.select('tr')[i]
        atskirtas = st.get_text()
        skaidymas = atskirtas.split()  # išskaidome į tris grupes
        laikas.append(i)
        if skaidymas[1] == '-':  # gali būti, kad kainos nesuvestos, todėl "-" pakeičiam į nulį
            kaina.append(0)
        else:
            kaina.append(float(skaidymas[1]))
        rusiavimas.append(skaidymas[2])
    rezultatas = (surusiuoti(kaina))
    # kainų įrašymas į csv failą
    with open("birza00.csv", 'w', encoding="UTF-8", newline='') as failas:
        csv_writer = csv.writer(failas)
        csv_writer.writerow(['VALANDOS', 'KAINA', 'RŪŠIAVIMAS', 'ĮKRAUTI', 'IŠKRAUTI'])
        for i in range(24):
            csv_writer.writerow([laikas[i], kaina[i], indeksas[i], start_in[i], start_out[i]])
    bandom_nuskaityti = False
    # else:
    #     print('biržos duomenys neatnaujinti bandom po valandos nuskaityti')
    #     time.sleep(60)

    # except:
    #     ...
