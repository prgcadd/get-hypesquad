import requests
import sys
import json
import os

def print_help():
    script_name = os.path.basename(sys.argv[0])
    print(f"Usage: {script_name} /t <discord_token> /hs <1|2|3|0>")
    print("  /t: Discord token")
    print("  /hs: HypeSquad house choice (1: Bravery, 2: Brilliance, 3: Balance, 0: Exit current house)")
    print(f"Example: {script_name} /t \"your_token_here\" /hs 1")

def get_username(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return f"{data['username']}#{data['discriminator']}"
    return None

def set_hypesquad(token, house_id):
    house_names = {1: 'Bravery', 2: 'Brilliance', 3: 'Balance', 0: 'None'}
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    if house_id == 0:
        response = requests.delete('https://discord.com/api/v9/hypesquad/online', headers=headers)
    else:
        payload = {'house_id': house_id}
        response = requests.post('https://discord.com/api/v9/hypesquad/online', json=payload, headers=headers)
    
    return response.status_code == 204

def main():
    print("get-hypesquad by prgcadd")
    print("Version 1.0")
    print()
    
    if len(sys.argv) != 5 or sys.argv[1] != '/t' or sys.argv[3] != '/hs':
        print_help()
        return
    
    token = sys.argv[2]
    try:
        house_choice = int(sys.argv[4])
        if house_choice not in [0, 1, 2, 3]:
            print("Error: HypeSquad choice must be 0, 1, 2, or 3")
            return
    except ValueError:
        print("Error: HypeSquad choice must be a number")
        return
    
    username = get_username(token)
    if username is None:
        print("Error: Invalid token or unable to fetch user information")
        return
    
    print(f"Logged in as: {username}")
    
    if set_hypesquad(token, house_choice):
        if house_choice == 0:
            print("Successfully removed from HypeSquad house")
        else:
            house_names = {1: 'Bravery', 2: 'Brilliance', 3: 'Balance'}
            print(f"Successfully set HypeSquad house to: {house_names[house_choice]}")
    else:
        print("Error: Failed to set HypeSquad house")

if __name__ == "__main__":
    main()
