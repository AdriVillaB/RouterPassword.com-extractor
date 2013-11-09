__author__ = 'AdriVillaB'

import time
import os
import requests
from BeautifulSoup import BeautifulSoup
import pickle


class Router(object):

    def __init__(self, manufacturer=None, model=None, protocol=None, username=None, password=None):
        """

        :param manufacturer:
        :param model:
        :param protocol:
        :param username:
        :param password:
        :return:
        """
        self.manufacturer = manufacturer
        self.model = model
        self.protocol = protocol
        self.username = username
        self.password = password

    def insert_from_list(self, list):
        """
        Insert data in the object from a list
        :param list:
        :return:
        """
        self.manufacturer = "".join(list[0].contents)
        self.model = "".join(list[1].contents)
        self.protocol = "".join(list[2].contents)
        self.username = "".join(list[3].contents)
        self.password = "".join(list[4].contents)

    def __str__(self):
        """
        Export the object to a string
        :return:
        """
        return self.manufacturer+";"+self.model+";"+self.protocol+";"+self.username+";"+self.password+"\n"


def clear_screen():
    """
    Clear the terminal
    :return:
    """
    if os.name == 'posix':
        os.system('clear')

    elif os.name == ('ce', 'nt', 'dos'):
        os.system('cls')

def export_to_csv(data):
    """
    Export a pickle file into CSV file
    :return:
    """
    with open("routers.csv", "wb") as f:
        f.write("Manufacturer;Model;Protocol;Username;Password\n")
        for router in data:
            f.write(router.__str__())


def load_data(file):
    """
    Load data inside a pickle file
    :param file:
    :return:
    """
    data = []
    try:
        with open(file) as f:
            data = pickle.load(f)
    except:
        data = []
    return data


def save_data(data, file):
    """
    Save data to a pickle file
    :param data:
    :param file:
    :return:
    """
    with open(file, 'wb') as f:
        pickle.dump(data, f)


def delete_invalid_tags(html):
    """
    Delete the tags unsupported by BeautifulSoap
    :param html:
    :return:
    """
    invalid_tags = ['b', 'i', 'u']
    for tag in invalid_tags:
        for match in html.findAll(tag):
            match.replaceWithChildren()
    return html


def get_manufacturers():
    """
    Retrieve the manufacturers of routerpasswords.com
    :return manufacturers:
    """

    r = requests.get("http://www.routerpasswords.com/")

    html = BeautifulSoup(r.text)
    html_models = html.findAll("option")

    manufacturers = [model['value'] for model in html_models]

    return manufacturers


def retrieve_all_info():
    """
    Get all the info in routerpasswords.com page
    :return retrieve_info:
    """

    retrieve_info = []

    manufacturers = get_manufacturers()

    for index in xrange(0, len(manufacturers)):
        post_data = {"findpass": 1, "router": manufacturers[index], "findpassword": "Find+Password"}
        r = requests.post("http://www.routerpasswords.com/", data=post_data)

        html = BeautifulSoup(r.text)
        html = delete_invalid_tags(html)
        html_info = html.table.findAll('td')

        for index2 in xrange(0, len(html_info), 5):
            router = Router()
            router.insert_from_list(html_info[index2:index2+5])
            retrieve_info.append(router)

        print "[+]Extraidos los routers de la marca " + manufacturers[index]
        time.sleep(1)

    return retrieve_info


if __name__ == "__main__":

    print "--------------------------------------------------"
    print "------- RouterPasswords.com info extractor -------"
    print "--------------------------------------------------"

    while True:
        try:

            print "1) Extract the manufacturers: "
            print "2) Extract all the info: "
            print "3) Save info to pickle file"
            print "4) Load info from pickle file"
            print "5) Save to CSV file"
            print "0) Exit"
            print
            option = int(input("What do you want to do? "))

            info = []
            if option == 1:
                manufacturers = get_manufacturers()
                print manufacturers
            elif option == 2:
                info = retrieve_all_info()
            elif option == 3:
                name_file = input("\nName of the file: ")
                save_data(info, name_file)
            elif option == 4:
                name_file = input("\nName of the file: ")
                info = load_data(name_file)
            elif option == 5:
                export_to_csv(info)
            elif option == 0:
                exit(0)
            else:
                exit(-1)
        except:
            pass