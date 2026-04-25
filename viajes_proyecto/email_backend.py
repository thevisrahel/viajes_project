from django.core.mail.backends.console import EmailBackend                 # Hereda del backend de consola
from email.mime.text import MIMEText                                       # Para crear emails en texto plano puro
import sys

class PlainConsoleEmailBackend(EmailBackend):                              # Backend personalizado sin quoted-printable
    def write_message(self, message):
        msg_data = message.message()
        for part in msg_data.walk():                                       # Recorre todas las partes del email
            if part.get_content_type() == 'text/plain':
                payload = part.get_payload(decode=True)                   # Decodifica el contenido
                if payload:
                    text = payload.decode('utf-8')                        # Convierte a string
                    self.stream.write(text)                               # Escribe en la consola sin encoding
                    self.stream.write('\n' + '-' * 79 + '\n')
                    self.stream.flush()
                    return
        super().write_message(message)                                     # Fallback al comportamiento normal