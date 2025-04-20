import requests
import json

def send_mailtrap_message(to_email):
    print("Sending email with Mailtrap...")

    # ¡PELIGRO! Credenciales hardcodeadas (NO recomendado para producción)
    api_token = "6bf88bf3c945c740b7bf0d2cea4433c6"
    mailtrap_id = "3630156"
    from_email = "password@novashift.com"
    from_name = "Nova Shift"
    subject = "You are awesome!"
    body_text = "Congrats for sending test email with Mailtrap! NEW"
    category = "Integration Test"

    url = f"https://sandbox.api.mailtrap.io/api/send/{mailtrap_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",  # Mailtrap usa "Bearer"
        "Content-Type": "application/json"
    }
    payload = {
        "from": {"email": from_email, "name": from_name},
        "to": [{"email": to_email}],
        "subject": subject,
        "text": body_text,
        "category": category
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print("Correo enviado exitosamente a través de Mailtrap!")
        print(response.text)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar el correo con Mailtrap: {e}")
        return None

if __name__ == "__main__":
    email = "11michaelvzla.cl@gmail.com"  # Ejemplo de email
    result = send_mailtrap_message(email)
    # Puedes procesar el resultado si es necesario
    if result:
        print(f"Mailtrap Response Status Code: {result.status_code}")

# TOken: 
# Name: mailtrap01
# Created By:Michael González
# Access :Account Admin
# Token : 6bf88bf3c945c740b7bf0d2cea4433c6



