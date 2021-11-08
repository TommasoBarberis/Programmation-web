import requests

URLS = [
  'https://perso.liris.cnrs.fr/pierre-antoine.champin/2018/progweb-python/_static/td1/page1.html',
  'https://perso.liris.cnrs.fr/pierre-antoine.champin/2018/progweb-python/_static/td1/no_such_page.html',
  'https://perso.liris.cnrs.fr/pierre-antoine.champin/2018/progweb-python/_static/td1/style.css',
  'https://perso.liris.cnrs.fr/pierre-antoine.champin/2018/progweb-python/_static/td1/sand.png',
  'https://www.uniprot.org/',
  'https://www.uniprot.org/uniparc/UPI000000001F',
  'https://www.uniprot.org/uniparc/UPI000000001F.tab',
  'https://www.uniprot.org/uniparc/UPI000000001F.truc',
  'https://www.uniprot.org/images/logos/uniprot-rgb-optimized.svg',
]

for url in URLS:
    print("URL: " + url)
    r = requests.get(url)
    print("STATUS: " + str(r.status_code))
    try:
        print("Content-Type: " + r.headers['Content-Type'])
    except:
        pass
    print(r.content[:20])
    print("\n")
