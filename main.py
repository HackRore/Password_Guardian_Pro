import os
os.environ["PYSG_SKIP_INSTALLER"] = "1"
import FreeSimpleGUI as sg
import hashlib
import requests
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

APP_NAME = "Password Guardian Pro"
ICON_PATH = os.path.join("assets", "logo.png")

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123", "password1", "111111", "123123", "letmein", "admin"
}

def check_strength(password):
    import string
    reasons = []
    score = 0

    if len(password) < 8:
        reasons.append("Password must be at least 8 characters.")
    else:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    else:
        reasons.append("Add lowercase letters.")
    if any(c.isupper() for c in password):
        score += 1
    else:
        reasons.append("Add uppercase letters.")
    if any(c.isdigit() for c in password):
        score += 1
    else:
        reasons.append("Add digits.")
    if any(c in string.punctuation for c in password):
        score += 1
    else:
        reasons.append("Add symbols (e.g., !@#$%).")
    if password.lower() in COMMON_PASSWORDS:
        reasons.append("Password is too common.")
        score = 0

    if score >= 5:
        return "Strong", reasons
    elif score >= 3:
        return "Medium", reasons
    else:
        return "Weak", reasons

def check_pwned(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None, "API error"
        hashes = (line.split(':') for line in resp.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count), None
        return 0, None
    except Exception as e:
        return None, f"Connection error: {e}"

def export_pdf(password, strength, reasons, breach_count, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"{APP_NAME} - Password Audit Report")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30
    c.drawString(50, y, f"Password checked: {'*' * len(password)}")
    y -= 30
    c.drawString(50, y, f"Strength: {strength}")
    y -= 30
    c.drawString(50, y, "Analysis:")
    y -= 20
    for reason in reasons:
        c.drawString(70, y, f"- {reason}")
        y -= 20
    y -= 10
    if breach_count is not None:
        if breach_count > 0:
            c.setFillColorRGB(1, 0, 0)
            c.drawString(50, y, f"⚠️ Found in {breach_count} breaches!")
            c.setFillColorRGB(0, 0, 0)
        else:
            c.drawString(50, y, "✅ Not found in known breaches.")
    else:
        c.drawString(50, y, "Dark web check: Not performed or failed.")
    y -= 30
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, y, "Recommendations:")
    y -= 20
    c.drawString(70, y, "- Use a unique password for every site.")
    y -= 15
    c.drawString(70, y, "- Consider using a password manager.")
    y -= 15
    c.drawString(70, y, "- Change passwords found in breaches immediately.")
    c.save()

def main():
    sg.theme("DarkBlue3")
    layout = [
        [sg.Image(filename=ICON_PATH, size=(64, 64)), sg.Text(APP_NAME, font=("Any", 20, "bold"))],
        [sg.Text("Enter Password:"), sg.Input(password_char="*", key="-PWD-", size=(30,1)), sg.Button("Check")],
        [sg.Text("Email (optional):"), sg.Input(key="-EMAIL-", size=(30,1))],
        [sg.Multiline("", size=(60, 8), key="-RESULT-", disabled=True)],
        [sg.ProgressBar(100, orientation='h', size=(40, 10), key='-PROG-', visible=False)],
        [sg.Button("Export PDF"), sg.Button("Reset"), sg.Button("Exit")]
    ]

    window = sg.Window(APP_NAME, layout, icon=ICON_PATH)

    password = ""
    strength = ""
    reasons = []
    breach_count = None

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event == "Check":
            window["-RESULT-"].update("")
            window["-PROG-"].update(visible=True)
            window.refresh()
            password = values["-PWD-"]
            if not password:
                window["-RESULT-"].update("Please enter a password.")
                window["-PROG-"].update(visible=False)
                continue
            strength, reasons = check_strength(password)
            breach_count, err = check_pwned(password)
            result = f"Password Strength: {strength}\n"
            if reasons:
                result += "Suggestions:\n" + "\n".join(f"- {r}" for r in reasons) + "\n"
            if err:
                result += f"Dark web check failed: {err}\n"
            elif breach_count is not None:
                if breach_count > 0:
                    result += f"⚠️ This password was found in {breach_count} data breaches!\n"
                else:
                    result += "✅ This password was NOT found in known breaches.\n"
            window["-RESULT-"].update(result)
            window["-PROG-"].update(visible=False)
            sg.popup_no_titlebar("Check complete!", keep_on_top=True, auto_close=True, auto_close_duration=2)
        if event == "Export PDF":
            if not password:
                sg.popup_error("No password checked yet!")
                continue
            default_name = f"PasswordAudit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            save_path = sg.popup_get_file("Save PDF As", save_as=True, file_types=(("PDF Files", "*.pdf"),), default_extension=".pdf", default_path=default_name)
            if save_path:
                try:
                    export_pdf(password, strength, reasons, breach_count, save_path)
                    sg.popup_no_titlebar("PDF exported!", keep_on_top=True, auto_close=True, auto_close_duration=2)
                except Exception as e:
                    sg.popup_error(f"Failed to export PDF: {e}")
        if event == "Reset":
            window["-PWD-"].update("")
            window["-EMAIL-"].update("")
            window["-RESULT-"].update("")
            password = ""
            strength = ""
            reasons = []
            breach_count = None

    window.close()

if __name__ == "__main__":
    main()