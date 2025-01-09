

ecr't mo' un programe capable  de recuperer juste les message present 'c' et les envo't sur le json du robot 

ecrit moi un programme capable de recuperer les contact et de envoyer direcctement aur robot 


ecrit moi un code ameliorere permettant de de faire de sorte on puiisse editer un contenu de texte en y ajoutant des info pertiante venant du json de contact  genre on peu lui demander d ajouter name  description etautre et dans ce poup si le gar choisi un truc ca soi tres humain et convivial par conttre ca reste sur le json en terme ınformatıque 




erit moi un code nous permettant de programmer l heur et la date dans la uelle le programme pourra secuter 


redigerle programme permettant de desinstaller un isntanccce wa 



corriger la lngue avant de copiler 

ecrire un programme permettant d extraire les json sous format csv et vis versa 



en tinspirant du code que j ai partager avec toi tout a lheure de son style qui doit etre un minimum a defaut d enfaire plus 
propose moi un code complet avec des buttons futirite et un disigne futuriste egalement 

le programme doit permettre a partir dun fichier .db en lieu et place du .json 
d ajouter un media que ca soit une imge video ou document pdf 
de modifier un media de le supprimer etc...

un media doit etre stocher dans le dossier wa-ia-robot present dans telehargement de l ordinateur du user 


voici a  quoi resemble mon json actuelle 
{
    "posts": [
        {
            "text": "ok ok #ok o33666",
            "image": "C:\\Users\\cheic\\Downloads\\AI-WA-Robot\\media\\media1\\2.png"
        },
        {
            "text": "Media Description",
            "image": "C:\\Users\\cheic\\Downloads\\AI-WA-Robot\\media\\media1\\3.png"
        },
        {
            "text": "okkok #oklo 02555",
            "image": "C:\\Users\\cheic\\Downloads\\AI-WA-Robot\\media\\media1\\1.png"
        }
    ]
} 
ce qui signifie que dans ma base de donne les medias doivent avoir text corresposndant
 a la description imge contenant le lien du media 
aussi lors de lajout d un media jaimerais avoir le chox entre assossier un image ou ajouter juste le text
en realite ma table media doit stocker les contenues qui seront utiliser pour stocker les contenue en faites qui seront utiliser 
lors de mes campagnes de partage de contenue que sa soit sur facebook groupes shares ou sur wahatssap 
donc en plus des attribut specifier ajoute toute autre attribut que tu juge utile pour l objectif  
le button qui me permet d ajouer un media doit etre  futiriste et tres bien disigner permett
ant d ouvrir un  modal ou pupup qui me donne le 
droit de rediger une description dupplodder un ou plussieur media d ajouter des hastag d ajouter un contact et tout doit etre paramettrable avant la soumission






mainteant propose moi une fonction qui permet de recuperer de la base de donnee les donnee qui vas mettre sous ce format [

    {
      "text": "{name} Don't forget the meeting tomorrow",
      "image": null,
      "pdf": null,
      "video": null
    },
    {
      "text": "{name} Don't forget the meeting tomorrow",
      "image": null,
      "pdf": null,
      "video": null
    }
  ]
  ie si le media est de type image alors met sonsur image si cest de type 
  met le lien sur pdf et ainsi de suite maintant le json  sera enregistrer dans le dossier c
   wabon robot sous le nom de wamessage.json si un fichier portant ce nom existe deja alors renommer 
   l existant qui deviendra comme archive et utilsier le nom wamessage.json poour stocker ce json
    aussi format le contenu de ce que tu mettra dans le champs text doit correspondr auchamp
     description et aucas ou la description commence par par une salutation genre bonjour 
     hello hi et consort met automatiquement {name} entre le terme de salutation et le reste  ,de texte
      de la descripton qui serra mappper dans le champ text du json 


      mainteant j aimerais que tu fasse de sorte que l orsque aulieu quil part recuperere toutes les lignes present dans le db 
      j aimerais qu il recupere les donnee selectionner directement du tabeau jaimerais donner la possibilite a selectionner les ligne 
      quil aimerait envoyer au .json et que la fonction converti et envoie uniquement les lignes selectionner pour rappelle voila ma classe 
      qui traite du tableau 
