text = "HUATAI SECURITIES CO., LTD."
sitename = text.lower().replace(' ', '-').replace('"', '').replace('(', '').replace(')', '').replace(',', '').replace('.', '-').replace('--', '-').rstrip('-')

print(sitename)