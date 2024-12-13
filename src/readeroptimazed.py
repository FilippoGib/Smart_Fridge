import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["QT_QPA_PLATFORM"] = "xcb" #non so se serve
import cv2
import easyocr
import re
from datetime import datetime

ip_address = "https://172.20.10.6:4343/video" #cambiare secondo necessità, devi essere sullo stesso wi-fi del telefono, no eduroam


class ExpirationDateReader:
    def __init__(self, use_gpu=False):
        # Inizializza il lettore OCR per leggere solo numeri e simboli (evita lettere)
        self.reader = easyocr.Reader(['en', 'it'], gpu=use_gpu)  # lingua settata solo per numeri e simboli

    def last_day_of_month(self, month, year):
        """Restituisce l'ultimo giorno del mese per il mese e anno specificati."""
        if month in [4, 6, 9, 11]:  # Mesi con 30 giorni
            return 30
        elif month in [1, 3, 5, 7, 8, 10, 12]:  # Mesi con 31 giorni
            return 31
        elif month == 2:  # Febbraio, con controllo anno bisestile
            return 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
        return 30  # Valore di sicurezza

    def convert_two_digit_year_to_four(self, two_digit_year):
        """Converte un anno a due cifre in un anno a quattro cifre."""
        two_digit_year = int(two_digit_year)
        return f"20{two_digit_year:02}"

    def is_valid_day(self, day):
        """Verifica che il giorno sia valido (compreso tra 1 e 31)."""
        return 1 <= day <= 31

    def find_expiration_date(self, text):
        """Rileva e formatta la data di scadenza nel testo usando espressioni regolari."""
        date_patterns = [
            r"\b\d{2}/\d{2}/\d{4}\b",   # DD/MM/AAAA ok
            r"\b\d{2}-\d{2}-\d{4}\b",   # DD-MM-AAAA ok
            r"\b\d{2} \d{2} \d{4}\b",   # DD MM AAAA ok
            r"\b\d{2} \d{2} \d{2}\b",   # DD MM AA manca anno completo
            r"\b\d{2}\.\d{2}\.\d{2}\b",   # DD MM AA manca anno completo
            r"\b\d{2}/\d{2}/\d{2}\b",   # DD/MM/AA manca anno completo
            r"\b\d{2}/\d{2}\b",         # DD/MM manca anno 
            r"\b\d{2}\.\d{2}\b",        # DD.MM manca anno 
            r"\b\d{2}-\d{2}-\d{2}\b",   # DD-MM-AA manca anno completo
            r"\b\d{2}\.\d{2}\.\d{4}\b", # DD.MM.AAAA ok
            r"\b\d{2}\.\d{4}\b",        # MM.AAAA manca giorno
            r"\b\d{2}/\d{4}\b",         # MM/AAAA manca giorno
            r"\b\d{2}/\d{2}\b",         # MM/AA manca giorno e anno
            r"\b\d{2}\.\d{2}\b"         # MM.AA manca giorno e anno completo
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                detected_date = match.group()
                 # Se la data è nel formato DD/MM o DD.MM, aggiungi l'anno corrente , controllando che mese sia < 12 se no siamo nel caso MM/AA
                if re.match(r"^\d{2}/\d{2}$", detected_date) or re.match(r"^\d{2}\.\d{2}$", detected_date):
                    day, month = re.split(r"[./]", detected_date)
                    month = int(month)
                    if 1 <= month <= 12:
                        current_year = datetime.now().year if datetime.now().month <= month else datetime.now().year + 1
                        detected_date = f"{day:02}/{month:02}/{current_year}"
                    else:
                        month, year = day, month
                        year = self.convert_two_digit_year_to_four(str(year))
                        day = self.last_day_of_month(month, int(year))
                        detected_date = f"{day:02}/{month:02}/{year}"
                
                # Se la data è nel formato DD/MM/AA, converti AA in AAAA
                elif re.match(r"^\d{2}/\d{2}/\d{2}$", detected_date):
                    day, month, year = detected_date.split("/")
                    year = self.convert_two_digit_year_to_four(year)
                    detected_date = f"{day}/{month}/{year}"
                
                # Se la data è nel formato DD-MM-AA, converti AA in AAAA
                elif re.match(r"^\d{2}-\d{2}-\d{2}$", detected_date):
                    day, month, year = detected_date.split("-")
                    year = self.convert_two_digit_year_to_four(year)
                    detected_date = f"{day}/{month}/{year}"
                
                # Se la data è nel formato DD.MM.AA, converti AA in AAAA
                elif re.match(r"^\d{2}.\d{2}.\d{2}$", detected_date):
                    day, month, year = detected_date.split(".")
                    year = self.convert_two_digit_year_to_four(year)
                    detected_date = f"{day}/{month}/{year}"

                # Se la data è nel formato DD MM AA, converti AA in AAAA
                elif re.match(r"^\d{2} \d{2} \d{2}$", detected_date):
                    day, month, year = detected_date.split(" ")
                    year = self.convert_two_digit_year_to_four(year)
                    detected_date = f"{day}/{month}/{year}"

                # Se la data è nel formato MM/AAAA o MM.AAAA, aggiungi l'ultimo giorno del mese    
                elif re.match(r"^\d{2}/\d{4}$", detected_date) or re.match(r"^\d{2}\.\d{4}$", detected_date):
                    month, year = re.split(r"[./]", detected_date)
                    day = self.last_day_of_month(int(month), int(year))
                    detected_date = f"{day:02}/{int(month):02}/{year}"
                
                # Se la data è nel formato MM/AA o MM.AA, aggiungi l'ultimo giorno del mese e espandi AA a AAAA
                elif re.match(r"^\d{2}/\d{2}$", detected_date) or re.match(r"^\d{2}\.\d{2}$", detected_date):
                    month, year = re.split(r"[./]", detected_date)
                    month = int(month)
                    year = self.convert_two_digit_year_to_four(year)
                    day = self.last_day_of_month(month, int(year))
                    detected_date = f"{day:02}/{month:02}/{year}"


                # Controllo che il giorno sia valido
                day, month, year = detected_date.split("/")
                day = int(day)
                if not self.is_valid_day(day):
                    print(f"Errore: il giorno {day} non è valido.")
                    return None

                return detected_date
        return None

    def read_date_from_camera(self):
        """Apre la fotocamera, applica OCR, e cerca una data di scadenza."""
        # cap = cv2.VideoCapture(ip_address)
        cap = cv2.VideoCapture('/dev/video4')
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        print("Rilevamento automatico della data di scadenza. Premi 'q' per uscire.")
        
        frame_skip = 10
        frame_count = 0
        expiration_date_found = False

        while not expiration_date_found:
            ret, frame = cap.read()
            crop_height = 50 #pixels
            frame = frame[crop_height:, :]
            if not ret:
                print("Errore nell'aprire la fotocamera.")
                break

            cv2.imshow("Rilevamento data di scadenza", frame)

            if frame_count % frame_skip == 0:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, binary_frame = cv2.threshold(gray_frame, 120, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for cnt in contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    if w > 50 and h > 15:
                        roi = frame[y:y+h, x:x+w]
                        results = self.reader.readtext(roi)
                        detected_text = " ".join([res[1] for res in results])
                        print("Testo rilevato: ", detected_text)

                        expiration_date = self.find_expiration_date(detected_text)
                        if expiration_date:
                            print("Data di scadenza rilevata: ", expiration_date)
                            return expiration_date

            frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

