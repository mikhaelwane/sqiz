import os
import sys
import asyncio
from telethon import TelegramClient, errors

ASCII = [
    "██████   █████   ██▓▒███████▒",
    "▒██    ▒ ▒██▓  ██▒▓██▒▒ ▒ ▒ ▄▀░",
    "░ ▓██▄   ▒██▒  ██░▒██▒░ ▒ ▄▀▒░ ",
    "  ▒   ██▒░██  █▀ ░░██░  ▄▀▒   ░",
    "▒██████▒▒░▒███▒█▄ ░██░▒███████▒",
    "▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░▓  ░▒▒ ▓░▒░▒",
    "░ ░▒  ░ ░ ░ ▒░  ░  ▒ ░░░▒ ▒ ░ ▒",
    "░  ░  ░     ░   ░  ▒ ░░ ░ ░ ░ ░",
    "      ░      ░     ░    ░ ░    ",
    "                      ░        "
]

for line in ASCII:
    print(line)

print("by mikhaelwane")

API_ID = '123456'
API_HASH = '123456'

async def nuke(session_path: str):
    if not os.path.isfile(session_path):
        print(f"File {session_path} not found.")
        return

    client = TelegramClient(session_path, API_ID, API_HASH)
    await client.start()

    me = await client.get_me()
    print(f"Logged in as {me.first_name} (@{me.username})")

    print("WARNING: This will permanently delete ALL dialogues (chats, groups, channels) for this account.")
    confirm = input("Are you sure? (y/N): ")
    if confirm.lower() != 'y':
        print("Aborted.")
        await client.disconnect()
        return

    dialogs = await client.get_dialogs()
    total = len(dialogs)
    print(f"Found {total} dialogues. Deleting...")

    for i, dialog in enumerate(dialogs, 1):
        try:
            await client.delete_dialog(dialog.id)
            print(f"  [{i}/{total}] Deleted {dialog.name or 'unnamed'}")
            await asyncio.sleep(0.5)
        except errors.FloodWaitError as e:
            print(f"Waiting {e.seconds} seconds due to flood...")
            await asyncio.sleep(e.seconds)
            await client.delete_dialog(dialog.id)
        except Exception as e:
            print(f"  Failed to delete {dialog.name}: {e}")

    try:
        await client.log_out()
        print("Session terminated on server.")
    except Exception as e:
        print(f"Logout error: {e}")

    await client.disconnect()

    if os.path.isfile(session_path):
        os.remove(session_path)
        print(f"Local session file {session_path} removed.")

    print("Done.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sqiz.py /patch/to/account.session")
        sys.exit(1)
    asyncio.run(nuke(sys.argv[1]))
