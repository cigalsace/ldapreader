# LDAP Reader

## Description:

Script python de consultation d'un répertoire LDAP via l'API LDAPAdmin de geOrchestra.


## Installation:

ldapreader utilise les modules python "requests" pour interroger l'API de LDAPAdmin et "vobject" pour la génération de vcard.  
Ces modules sont intégrés au script (cf. répertoire "libs").
Pour un utilisation optimale, il est cependant conseillé de les installer directement dans python via ```$ pip install vobjects requests```.


## Utilisation:

Exemple: ```$ python ldapreader.py action --arg1 value1 --arg2 value2```


**"user": consulter la fiche d'un utilisateur LDAP.**

Options:

*--uid, -u <uid>*       : uid de l'utilsateur - obligatoire.  

*--vcard, -c <path>*    : chemin d'export de la vcard. l'uid est utilisé comme nom de fichier (ex.: 'pdupont.vcf'). Si non précisé, le résultat est affiché à l'écran - optionnel.  


**"users": consulter la liste des utilisateurs LDAP.**

Options:

*--word, -w <word>*     : terme pour filtrer la liste des utilisateurs. Conserve uniquement les utilisateur dont le nom (sn), le prénom (givenName) ou l'organisme (o) contient le terme <word>. La casse est ignorée. - optionnel.  

*--group, -g <group>*   : terme pour filtrer la liste des utilisateurs via un group. Conserve uniquement les utilisateur dont le group contient le terme <group>. La casse est ignorée - optionnel.  

*--vcard, -c <file>*    : nom du fichier d'export de la vcard. Si l'option --vctype est définie à 's', un chemin doit être indiqué et l'uid des utilisateurs est utilisé comme nom de fichier (ex.: 'pdupont.vcf'). Si non précisé, le résultat est affiché à l'écran - optionnel.  

*--vctype, -t <type>*   : type de vcard pour l'export. Utilisé conjointement avec l'option --vcard. Les valeurs possibles sont 'm' (vcard multiple - un fichier avec tous les utilisateurs) et 's' (vcard simple - un fichier par utilisateur). La valeur par défaut est 'm' - optionnel.  


**"groups": consulter la liste des groupes LDAP.**

Options:

*--word, -w <word>* : terme pour filtrer la liste des groupes. Conserve uniquement les groupes dont le nom (cn) ou la description ('description') contient le terme <word>. La casse est ignorée. - optionnel.


## Exemples:

**Impression à l'écran**

```
$ python ldapreader.py user -u gryckelynck      // consulter la fiche de gryckelynck

$ python ldapreader.py users                    // consulter la liste de l'ensemble 
                                                // des utilisateurs du LDAP

$ python ldapreader.py users -w pierre          // consulter la liste des utilisateurs 
                                                // dont le nom ou l'organisme contenient 
                                                // le terme "pierre"

$ python ldapreader.py users -g SV_             // consulter la liste des utilisateurs 
                                                // appartenant à un groupe dont le nom 
                                                // contient le terme "sv_"

$ python ldapreader.py users -w pierre -g SV_   // consulter la liste des utilisateurs 
                                                // dont le nom ou l'organisme contient 
                                                // le terme "pierre" et appartenant à 
                                                // un groupe dont le nom contient le terme "sv_" 

$ python ldapreader.py groups                   // consulter la liste des groupes LDAP

$ python ldapreader.py groups -w SV_            // consulter la liste des groupes LDAP 
                                                // contenant le terme 'sv_'
```


**Export vcard**

```
$ python ldapreader.py user -u gryckelynck -c files                 // exporter dans le dossier 'files', 
                                                                    // au format vcard, la fiche de gryckelynck 
                                                                    // ('files/gryckelynck.vcf')

$ python ldapreader.py users -c files/multivcard.vcf                // exporter dans le fichier 'files/multivcard.vcf',
                                                                    // au format vcard, la liste de l'ensemble des 
                                                                    // utilisateurs du LDAP

$ python ldapreader.py users -c files/vcards -t s                   // exporter dans le dossier 'file/vcards', 
                                                                    // individuellement, au format vcard, la liste
                                                                    // de l'ensemble des utilisateurs du LDAP au 
                                                                    // format vcard individuellement dans le dossier 
                                                                    // 'file/vcards'

$ python ldapreader.py users -w pierre -g SV_ -c files/vcards -t s  // exporter dans le dossier 'file/vcards',
                                                                    // individuellement, au format vcard, la liste 
                                                                    // des utilisateurs dont le nom ou l'organisme 
                                                                    // contient le terme "pierre" et appartenant à 
                                                                    // un groupe dont le nom contient le terme "sv_" 
```

## Versions:

**ldapreader 0.01: stable**  

- Version initiale.
