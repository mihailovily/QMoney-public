def generate_license(filename):
    # генерируем лицензию
    my_file = open(filename, "w+")
    alphabet = list('qwertyuiopasdfghjklzxcvbnm')
    unusual = list('!@#$%^&*()?":>}{][')
    licensekey = []
    licensekey.append('0')
    licensekey.append(str(random.randint(0, 9)))
    for i in range(3):
        licensekey.append(random.choice(alphabet))
    for i in range(3):
        licensekey.append(random.choice(unusual))
    licensekey.append(str(random.randint(0, 9)))
    licensekey.append('0')
    licensekey = ''.join(licensekey)
    my_file.write(licensekey)
    my_file.close()

generate_license(license.txt) #генерируем лифензию, пишем в выбранный файл