import sys
import getpass


def error(msg, code=1, exit=True):
    print(f"\n/!\\ {msg}")

    if exit:
        sys.exit(code)


def user_input(prompt, default=None, choices=[]):
    prompt = f"[?] {prompt}" + (f" [{default}]: " if default else ": ")
    while True:
        if value := input(prompt).strip():
            if choices and value not in choices:
                print(f"[!] Invalid choice: {value}")
                continue

            return value
        elif default:
            return default


def get_new_password():
    password = ""
    while not password:
        password = getpass.getpass("[?] Password: ")
        confirmation = getpass.getpass("[?] Confirm: ")

        if password != confirmation:
            print("Passwords do not match ...")
            password = ""

    return password
