import qrcode

# url = "https://lecoh.pythonanywhere.com/"
url = "https://netorgft5520718-my.sharepoint.com/:f:/g/personal/david_pauta_nakama_com_pe/ErpYQU7bvaFIgA-oCsGL9R4BXpcYIVJwHOl1DuPAH2nQfQ?e=WAvha9"
img = qrcode.make(url)
img.save("qr_asistencia.png")

