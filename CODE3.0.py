import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import json
import os


class Expenshare() :
# classe à partir de laquelle tout sera créé et défini : fonctions, variables, éléments graphiques...
   
    def __init__(self) :
        """ fonction qui :
            - Crée et stocke la fenêtre Tkinter dans l’objet de la classe ;
            - définit la fenêtre graphique, sa géométrie, son titre
            - initialise le fichier csv
            - initialise le dictionnaire issu du csv
            - appelle la fonction creer_widgets_affichage_1 """
        
        self.racine = tk.Tk()
        self.racine.title("EXPENSHARE")
        self.racine.geometry("475x500")
        self.racine.configure(bg = '#3C3C3C')
        self.racine.update()
        self.logo = tk.PhotoImage(file = "logo.png")
        self.racine.iconphoto(True, self.logo)
        # Récupére la largeur
        self.width = self.racine.winfo_width() 
        # Récupére la hauteur
        self.height = self.racine.winfo_height()
        
        self.racine.resizable(width=False, height=False)
        
        #Initialisation de variables      
        self.dico = {}
        self.dico_affichage = {}
        self.dico1 = {}
        self.dico1_1 = {}
        self.lire_json()
        self.texte = ''
        self.photo1 = tk.PhotoImage(file = "retour.png")
        self.photo3 = tk.PhotoImage(file = "coche.png")

        self.creer_widgets_affichage_1(self)


    def lire_json(self) :
        if os.path.isfile('text.json'):
            with open('text.json', 'r+') as file :
                self.dico = json.load(file)
                # print(self.dico)
        else:
            with open('text.json', 'w') as f:
                self.dico = {}
                # print(self.dico)

        if os.path.isfile('text2.json'):
            with open('text2.json', 'r+') as file :
                self.dico_affichage = json.load(file)
                # print(self.dico_affichage)
        else:
            with open('text2.json', 'w') as f:
                self.dico_affichage = {}
                # print(self.dico_affichage)
                
                
    def creer_widgets_affichage_1(self, racine) :
        """ fonction qui crée tous les widgets de notre fenêtre au lancement du programme (affichage d’origine) : boutons, étiquettes et autres widgets nécessaires... """ 
        # Appelle la fonction creer_bouton_par_groupe si dictionnaire associé non-vide
        
        self.button_add = tk.Canvas(self.racine, width=61, height=78, highlightthickness=0, bg = '#3C3C3C')
        self.button_add.create_oval(0, 0, 60, 60, fill = '#A3CEEF', outline = '#A3CEEF')
        self.button_add.create_text(30, 29.5, text="+", font=("Helvetica", 38), fill = '#000000')
        self.button_add.bind("<Button-1>", self.creer_groupe)
        self.button_add.pack(side = tk.BOTTOM)

        self.label_add = tk.Label(self.racine, text= "Ajouter un groupe", font =("Courier", 14), bg = '#3C3C3C', fg = '#A3CEEF')
        self.label_add.pack(side= tk.BOTTOM)
        
        self.reinitialiser = tk.Button(self.racine, text="Reinitialiser")
        self.reinitialiser.pack(side= tk.TOP)
        self.reinitialiser.bind('<Button-1>', self.reinitialiser_json)
        
        self.canvas1 = tk.Canvas(self.racine, bg = '#3C3C3C')
        self.scrollbar = tk.Scrollbar(self.racine, orient=tk.VERTICAL, command=self.canvas1.yview)
        self.scrollable_frame1 = tk.Frame(self.canvas1)
        self.scrollable_frame1.pack(side = tk.TOP)
        self.scrollable_frame1.bind("<Configure>",lambda e: self.canvas1.configure(scrollregion=self.canvas1.bbox("all")))
        self.canvas1.create_window((0, 0), window=self.scrollable_frame1)
        self.canvas1.configure(yscrollcommand=self.scrollbar.set)
        self.canvas1.pack(side="left", fill="both", expand=True, anchor = 'center')
        self.scrollbar.pack(side="right", fill="y")


        if len(self.dico) != 0 :
           self.creer_bouton_par_groupe(self.racine)
            

    def creer_widgets_affichage_2(self) :
        """ fonction qui crée un nouvel affichage en fonction du widget sur lequel l’utilisateur clique """ 
       
        self.label_affichage = tk.Label(self.racine, text = '\nNOUVEAU GROUPE\n', font =("Courier 25 bold"),bg = '#3C3C3C',fg = '#A3CEEF')
        self.label_affichage.pack()
        
        self.label_nom_grp = tk.Label(self.racine, text =' \nNom du groupe ', font =("Courier", 17), bg = '#3C3C3C',fg = '#A3CEEF')
        self.label_nom_grp.pack()
        
        self.entry_nom = tk.Entry(self.racine)
        self.entry_nom.pack()
       
        self.valider = tk.Button(self.racine, text="valider", bg = '#4C4C4C', fg = '#A3CEEF')
        self.valider.pack()
        self.valider.bind("<Button-1>", self.creer_dico_groupe)

        self.participant = tk.Label(self.racine, text = "\n\nNom d'un participant",font =("Courier", 17), bg = '#3C3C3C',fg = '#A3CEEF')
        self.participant.pack()

        self.nom_participant = tk.Entry(self.racine)
        self.nom_participant.pack()
        
        self.add_participant = tk.Button(self.racine, text="ajouter ce participant", bg = '#4C4C4C', fg = '#A3CEEF')
        self.add_participant.pack()
        self.add_participant.bind("<Button-1>", self.fonctions_creer_personne)  

       
        self.retour = tk.Button(self.racine, image = self.photo1, bg = '#4C4C4C', highlightthickness=0) 
        self.retour.bind('<Button-1>', self.retour_2)
        self.retour.place(x = self.width/30, y = self.height/1.15)
       
        self.bouton_enregistrer_grp = tk.Button(self.racine, width = 10, height = 2, text = "enregistrer", font = "bold 16", bg = '#4C4C4C',fg = '#A3CEEF')
        self.bouton_enregistrer_grp.bind('<Button-1>', self.enregistrer_groupe)
        self.bouton_enregistrer_grp.place(x = self.width/(8/2.8), y = self.height/(15/13))
        
        self.duree = 200 # durée en secondes
        self.debut = time.time() # temps actuel en secondes depuis l'époque Unix

                  
    def creer_widgets_affichage_3(self) :
        """ fonction qui crée un nouvel affichage en fonction du widget sur lequel l’utilisateur clique """
        # Appelle la fonction creer_label_par_depense si dictionnaire associé non-vide
        self.label_affichage = tk.Label(self.racine, text = (f"\nGROUPE: {self.clee}\n"), font =("Courier 25 bold"), bg = '#3C3C3C', fg = '#A3CEEF')
        self.label_affichage.pack()
        
        self.button_add = tk.Canvas(self.racine, width=61, height=78, highlightthickness=0, bg = '#3C3C3C')
        self.button_add.create_oval(0, 0, 60, 60, fill = '#A3CEEF', outline = '#A3CEEF')
        self.button_add.create_text(30, 29.5, text="+", font=("Helvetica", 38), fill = '#000000')
        self.button_add.bind("<Button-1>", self.ajouter_dépenses)
        self.button_add.pack(side = tk.BOTTOM)
        
        self.label_add = tk.Label(self.racine, text="\nAjouter une dépense", font =("Courier", 14), bg = '#3C3C3C', fg = '#A3CEEF')
        self.label_add.pack(side= tk.BOTTOM)
        
        self.retour = tk.Button(self.racine, image = self.photo1, highlightthickness=0, bg = '#4C4C4C', fg = '#A3CEEF') 
        self.retour.bind('<Button-1>', self.retour_3)
        self.retour.place(x = self.width/30, y = self.height/1.15)
        
        self.bilan = tk.Button(self.racine, text="BILAN DU GROUPE", bg = '#4C4C4C', fg = '#A3CEEF') 
        self.bilan.bind('<Button-1>', self.ouvrir_bilan)
        self.bilan.pack(side = tk.BOTTOM)
        
        self.canvas3 = tk.Canvas(self.racine, bg = '#3C3C3C')
        self.scrollbar = tk.Scrollbar(self.racine, orient=tk.VERTICAL, command=self.canvas3.yview)
        self.scrollable_frame3 = tk.Frame(self.canvas3)
        self.scrollable_frame3.bind("<Configure>",lambda e: self.canvas3.configure(scrollregion=self.canvas3.bbox("all")))
        self.canvas3.create_window((self.width/4, 0), window=self.scrollable_frame3)
        self.canvas3.configure(yscrollcommand=self.scrollbar.set)
        self.canvas3.pack(side="left", fill="both", expand=True, anchor = 'center')
        self.scrollbar.pack(side="right", fill="y")

        if len(self.dico2_2) != 0 : 
           self.creer_labels_par_depense(self.racine)
        
        
    def creer_widgets_affichage_4(self) :
        """ fonction qui crée un nouvel affichage en fonction du widget sur lequel l’utilisateur clique """
       
        self.label_affichage = tk.Label(self.racine, text = '\nNOUVELLE DÉPENSE', font =("Courier 25 bold"), bg = '#3C3C3C', fg = '#A3CEEF')
        self.label_affichage.pack()
        
        self.label_nom_dep = tk.Label(self.racine, text =' \n\nNom de la dépense : ',font =("Courier", 17), bg = '#3C3C3C', fg = '#A3CEEF')
        self.label_nom_dep.pack()
        
        self.entry_dep= tk.Entry(self.racine)
        self.entry_dep.pack()
        
        self.label_participant = tk.Label(self.racine, text =' \nNom du participant : ',font =("Courier", 17), bg = '#3C3C3C', fg = '#A3CEEF')
        self.label_participant.pack()
        

        self.selected_option = tk.StringVar(self.racine)
        self.options = list(self.dico2.keys())
        self.selected_option.set(self.options[0])

        self.espace_participant = tk.OptionMenu(self.racine, self.selected_option, *self.options) 
        self.espace_participant.pack()
   

        self.label_coût_dep = tk.Label(self.racine, text =' \nCoût de la dépense (en €): ',font =("Courier", 17), bg = '#3C3C3C', fg = '#A3CEEF')
        self.label_coût_dep.pack()
        
        self.entry_cout= tk.Entry(self.racine)
        self.entry_cout.pack()
        
        self.retour = tk.Button(self.racine, image = self.photo1, highlightthickness=0, bg = '#4C4C4C', fg = '#A3CEEF') 
        self.retour.bind('<Button-1>', self.retour_4)
        self.retour.place(x = self.width/30, y = self.height/1.15)
        
        self.bouton_enregistrer_dep = tk.Button(self.racine, width = 10, height = 2, text = "enregistrer", font = "bold 15", bg = '#4C4C4C',fg = '#A3CEEF', command=lambda: self.enregistrer_dépense(name=self.selected_option.get()))
        self.bouton_enregistrer_dep.place(x = self.width/(8/2.8), y = self.height/(15/13))
        
        self.duree = 50 # durée en secondes
        self.debut = time.time() # temps actuel en secondes depuis l'époque Unix
          

    def creer_widgets_affichage_5(self) :
        """ fonction qui crée un nouvel affichage en fonction du widget sur lequel l’utilisateur clique """

        self.titre = tk.Label(self.racine, text =' \nBILAN DU GROUPE ', font =("Courier 25 bold"), bg = '#3C3C3C', fg = '#A3CEEF')
        self.titre.pack()

        self.canvas_graphe = tk.Canvas(self.racine, width=300, height=200, bg = '#3C3C3C')
        self.canvas_graphe.pack()

        self.virements = tk.Label(self.racine, text = (f'{self.texte}'), font = 'Helvetica 10 bold', bg = '#3C3C3C', fg = '#A3CEEF')
        self.virements.pack()

        self.retour = tk.Button(self.racine, image = self.photo1, highlightthickness=0, bg = '#4C4C4C', fg = '#A3CEEF') 
        self.retour.bind('<Button-1>', self.retour_5)
        self.retour.place(x = self.width/30, y = self.height/1.15)


    def creer_bouton_par_groupe(self, racine) :
        """ fonction qui utilise le dictionnaire dans lequel apparaitront les différents groupes créés afin de créer un nouveau bouton par groupe """
        self.mes_boutons= [] 
        i = 0
        for v in self.dico.keys() :
           self.creer_1_bouton_par_groupe(v,i)


    def creer_1_bouton_par_groupe(self, v, i) :

        self.bouton_grp = tk.Button(self.scrollable_frame1, text = str(v), bg = '#515151', fg = '#A3CEEF', font= ("Courier", 18), height='1', width='32', anchor= tk.CENTER)
        self.bouton_grp.bind('<Button-1>', self.ouvrir_groupe)
        self.bouton_grp.pack(side = 'top')
        self.mes_boutons.append(self.bouton_grp)
        

    def creer_labels_par_depense(self,racine) :
        """ fonction qui utilise le dictionnaire dans lequel apparaitront les différentes dépenses créées afin de créer une étiquette par dépense """
       
        for participant,v in self.dico2_2.items() :    
            for nom,cout in v.items() :
                self.creer_1_label_par_depense(participant,nom,cout)
    

    def creer_1_label_par_depense(self, participant,nom, cout) :
        
        self.label_dep = tk.Button(self.scrollable_frame3, text= (str(participant)+ ": " + str(nom) +"("+ str(cout)+"€)"), bg = '#515151', fg = '#A3CEEF', font= ("Courier", 18), width = '32')
        self.label_dep.pack(side = tk.TOP, fill= 'x', anchor = 'center')
        

    def fonctions_creer_personne(self,event):
        self.creer_dico_personne()
        self.message_personne = tk.Label(self.racine, text = (f'{self.nom_parti} a été ajouté'), bg = '#3C3C3C', fg = '#A3CEEF')
        self.message_personne.pack()
        self.message_personne.after(3000, self.message_personne.destroy)

     
    def retour_2(self, event) :
        """ fonction qui retourne l’affichage précédent (3) """
        # Appelle les fonctions effacer, et creer_widgets_affichage_3
        if self.temps_ecoule < self.duree :
            self.detruire_timer_suivant()
        elif self.temps_ecoule2 < self.duree2 :
            self.detruire_timer2_suivant()
        self.effacer()
        self.creer_widgets_affichage_1(self.racine)


    def retour_3(self, event) :
        """ fonction qui retourne l’affichage précédent (1) """
        # Appelle les fonctions effacer, et creer_widgets_affichage_1
        self.effacer()
        self.creer_widgets_affichage_1(self.racine)
   
       
    def retour_4(self, event) :
        """ fonction qui retourne l’affichage précédent (3) """
        # Appelle les fonctions effacer, et creer_widgets_affichage_3
        if self.temps_ecoule < self.duree :
            self.detruire_timer1_suivant()
        elif self.temps_ecoule2 < self.duree2 :
            self.detruire_timer2_suivant()
        self.effacer()
        self.creer_widgets_affichage_3()


    def retour_5(self, event) :
        """ fonction qui retourne l’affichage précédent (3) """
        # Appelle les fonctions effacer, et creer_widgets_affichage_3
        self.effacer()
        self.creer_widgets_affichage_3()


    def creer_dico_groupe(self, event) :

        self.nom_grp = self.entry_nom.get()
        self.dico[self.nom_grp] = {}
        self.dico_affichage[self.nom_grp] = {}
        # print("\ncreate dico group", self.dico, self.dico_affichage)
        
        self.valider = tk.Label(self.racine, image = self.photo3).place(x = self.width/(4/3), y = self.height/4)


    def creer_dico_personne(self) :
        
        self.nom_parti = self.nom_participant.get()
        if self.dico1_1.get(self.nom_parti, 0) == 0 :     
            self.dico1[self.nom_parti] = 0   #?????
            self.dico1_1[self.nom_parti] = {}
            # print(f"dico 1_1 {self.dico1_1}")
            self.nom_participant.delete(0, "end")

        else : 
            self.msg1 = tk.Message(self.racine, text="Vous avez rentré deux fois le même nom, quittez et recommencez")
            self.msg1.pack(fill = 'x', side = tk.TOP)  
            # print("test")
     
            
    def enregistrer_groupe(self, event) :
        """ fonction qui enregistre les données inscrites sur l’affichage 2 (via des ‘Entry’) dans un fichier csv, permettant ainsi d’enregistrer des données de manière globale et non locale. Puis qui retourne à l’affichage précédent (1) """
        self.dico[self.nom_grp] = self.dico1
        self.dico_affichage[self.nom_grp] = self.dico1_1

        # print(f'dico 1 {self.dico1}')
        # print(f'dico 1_2 {self.dico1_1}')

        self.dico1 = {}
        self.dico1_1 = {}

        self.effacer()
        self.creer_widgets_affichage_1(self.racine)
        if self.temps_ecoule < self.duree :
            self.detruire_timer_suivant()
        elif self.temps_ecoule2 < self.duree2 :
            self.detruire_timer2_suivant()
        self.enregistrer_json()
        

    def enregistrer_dépense_nom(self):
        
        self.nom_dep = self.entry_dep.get()
        self.cout = self.entry_cout.get()
        # self.nom_pers = self.dico2_2.keys()

        # print("avant update", self.dico2_2)
        for nom in list(self.dico2_2.keys()):
            if nom == self.nom_particip:
                #self.dico2[self.nom_particip] = {self.nom_dep : self.cout}
                self.dico2_2[self.nom_particip].update({self.nom_dep : self.cout})
                self.dico_affichage[self.clee] = self.dico2_2
        
        # print(f'dico affichage {self.dico_affichage}')

    
    def enregistrer_dépense(self, name) :
        """ fonction qui enregistre les données inscrites sur l’affichage 4 (via des 'Entry') dans un fichier csv, permettant ainsi d’enregistrer des données de manière globale et non locale. Puis qui retourne à l’affichage précédent (3) """
        # Appelle les fonctions completer_fichier_csv, effacer et creer_widgets_affichage_3
        self.nom_particip = name
        self.nom_dep = self.entry_dep.get()
        self.cout = self.entry_cout.get()
        nom_pers = self.dico2.keys()
        
        for nom in list(nom_pers):
            if nom == self.nom_particip:
                self.somme = 0
                self.somme += float(self.dico2[self.nom_particip]) + float(self.cout)
                self.dico2[self.nom_particip] = self.somme
                self.dico[self.clee] = self.dico2
        
        # print(f'dico principal {self.dico}')

        self.enregistrer_dépense_nom()
        self.effacer()
        self.creer_widgets_affichage_3()
        if self.temps_ecoule < self.duree :
            self.detruire_timer1_suivant()
        elif self.temps_ecoule2 < self.duree2 :
            self.detruire_timer2_suivant()
        self.enregistrer_json()


    def effacer(self) :
        """ fonction qui efface tout l’affichage actuel de la fenêtre """
        for widget in self.racine.winfo_children():
            widget.destroy()
        

    def creer_groupe (self, event) :
        """ Permet à l’utilisateur de créer un nouveau groupe de dépenses en 
        rentrant le nom du groupe, la description du groupe, ainsi que les infos 
        sur les différents participants (Nom, Prénom ...). Elle est appelée suite 
        à un clique sur un bouton « + » de l’interface 1. """
        # Appelle les fonctions effacer et creer_widgets_affichage_2
        self.effacer()
        self.creer_widgets_affichage_2()
        self.arreter_timer = True
        self.timer()


    def ouvrir_groupe(self, event) :
        """ Permet d’accéder aux dépenses d’un groupe déjà créé suite à un clique sur un bouton de notre premier affichage """
        # Appelle les fonctions effacer et creer_widgets_affichage_3
        ref_w = event.widget
        i=0
        while i < len(self.mes_boutons) and ref_w != self.mes_boutons[i]:
            i = i+1
        
        self.mon_bouton = self.mes_boutons[i]
        self.clee = self.mon_bouton['text']
        
        self.dico2 = {}
        self.dico2_2 = {}
        
        # print("tous les dict", self.dico, self.dico_affichage)
        
        for c,v in self.dico.items():
            if c == self.clee :
                # print(f'c : {c} et v : {v}')
                for c1, v1 in v.items():
                    # print(f'c1 : {c1} et v1 : {v1}')
                    self.dico2[c1]= v1
        # print(f' dico2 {self.dico2}')
        
        for a,b in self.dico_affichage.items():
            if a == self.clee :
                # print(f'a : {a} et b : {b}')
                for a1, b1 in b.items():
                    # print(f'a1 : {a1} et b1 : {b1}')
                    self.dico2_2[a1]= b1
        # print(f' dico2_2 {self.dico2_2}')
        
        self.effacer()
        self.creer_widgets_affichage_3()


    def ajouter_dépenses (self, event) :
        """ Permet d’ajouter les dépenses de chaque participant au sein d’un groupe suite à un clique sur un bouton « + » de l’affichage 3 """
        # Appelle les fonctions effacer et creer_widgets_affichage_4
        self.effacer()
        self.creer_widgets_affichage_4()
        self.arreter_timer1 = True
        self.timer1()


    def timer(self):
        self.temps_ecoule = time.time() - self.debut
        temps_restant = self.duree - self.temps_ecoule
        minutes = int(temps_restant / 60)
        secondes = int(temps_restant % 60)
        self.label_timer = tk.Label(self.racine, text="Temps restant : {:02d}:{:02d}".format(int(self.duree / 60), self.duree % 60))
        self.label_timer.configure(text="Temps restant : {:02d}:{:02d}".format(minutes, secondes))
        self.label_timer.place(x = 250, y = 40)
        if self.temps_ecoule >= self.duree:
            self.label_timer.configure(text="Etes-vous encore là?")
            self.label_timer.place(x=250,y=55)
            self.creer_bouton_timer()
        elif self.arreter_timer:
            # Planifier la prochaine exécution de la fonction timer
            self.racine.after(1000, self.timer)
        else:
            self.label_timer.destroy()


    def timer1(self):
        self.temps_ecoule = time.time() - self.debut
        temps_restant = self.duree - self.temps_ecoule
        minutes = int(temps_restant / 60)
        secondes = int(temps_restant % 60)
        self.label_timer1 = tk.Label(self.racine, text="Temps restant : {:02d}:{:02d}".format(int(self.duree / 60), self.duree % 60))
        self.label_timer1.configure(text="Temps restant : {:02d}:{:02d}".format(minutes, secondes))
        self.label_timer1.place(x = 250, y = 40)
        if self.temps_ecoule >= self.duree:
            self.label_timer1.configure(text="Etes-vous encore là?")
            self.label_timer1.place(x=250,y=55)
            self.creer_bouton_timer1()
        elif self.arreter_timer1:
            # Planifier la prochaine exécution de la fonction timer
            self.racine.after(1000, self.timer1)
        else:
            self.label_timer1.destroy()


    def timer2(self):
        self.temps_ecoule2 = time.time() - self.debut2
        temps_restant = self.duree2 - self.temps_ecoule2
        minutes = int(temps_restant / 60)
        secondes = int(temps_restant % 60)
        self.label_timer2 = tk.Label(self.racine, text="Temps restant : {:02d}:{:02d}".format(int(self.duree2 / 60), self.duree2 % 60))
        self.label_timer2.configure(text="Temps restant : {:02d}:{:02d}".format(minutes, secondes))
        self.label_timer2.place(x = 250, y = 40)
        if self.temps_ecoule2 >= self.duree2:
            with open('text.json', 'w+') as file :
                jsonStr = json.dumps(self.dico)
                file.write(jsonStr + '\n')
            with open('text2.json', 'w+') as file :
                jsonStr2 = json.dumps(self.dico_affichage)
                file.write(jsonStr2 + '\n')
            self.racine.destroy()
        elif self.arreter_timer2:
            # Planifier la prochaine exécution de la fonction timer
            self.racine.after(1000, self.timer2)
        else:
            self.label_timer2.destroy()
            
    
    def arreter_timer(self):
        self.arreter_timer = True


    def arreter_timer1(self):
        self.arreter_timer1 = True
    

    def arreter_timer2(self):
        self.arreter_timer2 = True
    
    
    def detruire_timer_suivant(self):
        # Annuler la prochaine exécution de la fonction timer
        self.racine.after_cancel(self.timer)
        # Supprimer le label du timer
        self.label_timer.destroy()
        # Réinitialiser la variable de classe arreter_timer
        self.arreter_timer = False
    

    def detruire_timer1_suivant(self):
        # Annuler la prochaine exécution de la fonction timer
        self.racine.after_cancel(self.timer1)
        # Supprimer le label du timer
        self.label_timer1.destroy()
        # Réinitialiser la variable de classe arreter_timer
        self.arreter_timer1 = False
    

    def detruire_timer2_suivant(self):
        # Annuler la prochaine exécution de la fonction timer
        self.racine.after_cancel(self.timer2)
        # Supprimer le label du timer
        self.label_timer2.destroy()
        # Réinitialiser la variable de classe arreter_timer
        self.arreter_timer2 = False


    def creer_bouton_timer(self) :
        self.bouton_oui = tk.Button(self.racine, text="oui")
        self.bouton_oui.place(x=290,y=75)
        self.bouton_oui.bind("<Button-1>", self.appelle_creer_widgets_affichage_2)
        self.duree2 = 10
        self.debut2 = time.time()
        self.arreter_timer2 = True
        self.timer2()


    def creer_bouton_timer1(self) :
        self.bouton_oui = tk.Button(self.racine, text="oui")
        self.bouton_oui.place(x=290,y=75)
        self.bouton_oui.bind("<Button-1>", self.appelle_creer_widgets_affichage_4)
        self.duree2 = 10
        self.debut2 = time.time()
        self.arreter_timer2 = True
        self.timer2()
    

    def appelle_creer_widgets_affichage_2(self, event):
        self.effacer()
        #self.detruire_timer_suivant()
        self.detruire_timer2_suivant()
        self.creer_widgets_affichage_2()
        self.timer()

        
    def appelle_creer_widgets_affichage_4(self, event):
        self.effacer()
        #self.detruire_timer1_suivant()
        self.detruire_timer2_suivant()
        self.creer_widgets_affichage_4()
        self.timer1()


    def ouvrir_bilan(self, event) :
        self.effacer() 
        self.virements_recommandes()
        self.creer_widgets_affichage_5()
        self.creer_widget_bilan()


    def depense_moyenne(self):
        """ fonction qui récupère les montants dépensés par chaque participant, les somme et les divise par le nombre de participants afin de calculer le montant égalitaire théorique que chaque participant doit débourser """
        # Appelle la fonction creer_dict
        Nombre_de_personnes = len(self.dico2)
        Valeur_totale_depense = 0

        # Valeur Totale depense par tous les participants
        for Valeurs in self.dico2.values():
            Valeur_totale_depense += Valeurs

        # Valeur moyenne depense par personne
        self.valeur_moyenne = Valeur_totale_depense / Nombre_de_personnes
        #print(self.valeur_moyenne)


    def bilan_fonction(self):
        """ fonction qui calcule combien chaque personne doit payer ou recevoir pour que les dépenses soient équilibrées """
        #Appel la fonction depense_moyenne
        self.depense_moyenne()
        self.a_payer = {}
        self.a_recevoir = {}

        for Personnes, Argent in self.dico2.items():
            if Argent < self.valeur_moyenne:
                Personne_doit = self.valeur_moyenne - Argent
                self.a_payer.update({Personnes: Personne_doit})
        #print(f"A PAYER : {self.a_payer}")

        for Personnes, Argent in self.dico2.items():
            if Argent > self.valeur_moyenne:
                Personne_reçoit = Argent - self.valeur_moyenne
                self.a_recevoir.update({Personnes: Personne_reçoit})
        #print(f"A RECEVOIR : {self.a_recevoir}")


    def creer_widget_bilan(self) :
        """ fonction qui affiche les résultats du bilan sous forme de graphique et les virements recommandés, suite à un clique sur un bouton ‘BILAN DU GROUPE’ de l’affichage 3. """
        # Appelle les fonctions bilan, effacer, creer_widgets_affichage_5 et creer_widget_virements
        self.fig = plt.Figure(figsize=(3, 2), dpi=100, facecolor = '#3C3C3C')

        labels = list(self.dico2.keys())
        valores = list(self.dico2.values())
        self.subplot = self.fig.add_subplot(111)
        self.subplot.pie(valores, labels=labels, startangle=90)
        self.subplot.set_title("Bilan dépenses")
        plt.show()

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.canvas_graphe)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack() 


    def virements_recommandes(self):
        """ fonction qui récupère les valeurs calculées par la fonction 'bilan' et trouve un moyen d'équilibrer toutes les dépenses afin que chaque participant paye la même somme d’argent, en minimisant le nombre de remboursement à effectuer """
        # Appelle la fonction bilan
        self.texte = ''
        self.bilan_fonction()
        pivot_1 = 0
        pivot_2 = 0

        doit_combient = list(self.a_payer.values())
        recoit_combient = list(self.a_recevoir.values())
        qui_doit = list(self.a_payer.keys())
        qui_recoit = list(self.a_recevoir.keys())

        for a in range(len(doit_combient)):
            for b in range(len(recoit_combient)):
                if doit_combient[a] == recoit_combient[b] and doit_combient[a] != 0:
                    #ICI ON A UN PETIT PROBLME. QUAND LE CODE PASSE PAR LA, IL AFFICHE BIEN LE VALEUR DU VIREMENT A EFETUER MAIS IL ME SAMBLE QUE LE BOUCLE NE FERME PAS. ET DONC LE PROGRAME BUG ET ON DOIT FEMER ET REOUVIR
                    self.texte = self.texte + f' {qui_doit[a]} doit {doit_combient[a]:.2f} € à {qui_recoit[b]} \n'
                    # print(f'AA {qui_doit[a]} doit {doit_combient[a]} euros à {qui_recoit[b]} ') 
                    doit_combient[a] = 0
                    recoit_combient[b] = 0
    

        while pivot_1 < len(doit_combient) and pivot_2 < len(recoit_combient):
            Virement = doit_combient[pivot_1] - recoit_combient[pivot_2]
            if Virement < 0:
                Virement = doit_combient[pivot_1]
                recoit_combient[pivot_2] = recoit_combient[pivot_2] - Virement
                self.texte = self.texte + f'{qui_doit[pivot_1]} doit {Virement:.2f} € à {qui_recoit[pivot_2]}\n' 
                #self.'text_area'.insert(tk.INSERT,texte)
                # print(f'{qui_doit[pivot_1]} doit {Virement} euros à {qui_recoit[pivot_2]}')
                pivot_1 += 1

            elif Virement > 0:
                Virement = recoit_combient[pivot_2]
                doit_combient[pivot_1] = doit_combient[pivot_1] - Virement
                self.texte = self.texte + f'{qui_doit[pivot_1]} doit {Virement:.2f} € à {qui_recoit[pivot_2]}\n'
                #self.'text_area'.insert(tk.INSERT,texte)
                # print(f'{qui_doit[pivot_1]} doit {Virement:.2f} euros à {qui_recoit[pivot_2]}')
                pivot_2 += 1

            elif Virement == 0 and doit_combient[pivot_1] != 0:
                Virement = doit_combient[pivot_1] 
                self.texte = self.texte + f'{qui_doit[pivot_1]} doit {Virement:.2f} € à {qui_recoit[pivot_2]}\n'
                #self.'text_area'.insert(tk.INSERT,texte)
                # print(f'{qui_doit[pivot_1]} doit {Virement:.2f} euros à {qui_recoit[pivot_2]}')
                pivot_1 += 1
                pivot_2 += 1  

            else:
                pivot_1 += 1
                pivot_2 += 1
    
    
    def enregistrer_json(self) :
        with open('text.json', 'w+') as file :
            jsonStr = json.dumps(self.dico)
            file.write(jsonStr + '\n')
        with open('text2.json', 'w+') as file :
                jsonStr2 = json.dumps(self.dico_affichage)
                file.write(jsonStr2 + '\n')
     
        
    def reinitialiser_json(self, event):
        self.effacer()
        with open('text.json', 'w+') as file :
            jsonStr = json.dumps({})
            file.write(jsonStr + '\n')
        with open('text2.json', 'w+') as file2 :
            jsonStr2 = json.dumps({})
            file2.write(jsonStr2 + '\n')
        
        self.lire_json()
        self.creer_widgets_affichage_1(self.racine)
    

if __name__ == "__main__":

    app = Expenshare()

    app.racine.mainloop()