# Terraform Wars - Backend

Nova flow projektu:
- Uzivatel musi mit sparovany social account
- Uzivatel si vytvori projekt, sam si ho pojmenuje
    - Na pozadi se vytvori projekt v gcp
    - Zapnou se zakladni apicka v projektu
    - vytvori se service account
    - service account dostane potrebne role v projektu, tohle se teda muze dit az pri prvnim submitu kodu daneho tutorialu
    - service account grantne serviceAccountTokenCreator role na nase service accounty
- V komponentu tutorial detail bude uzivatel vzdycky mit moznost vybrat projekt, ktery se pouziva pro dany tutorial. POkud zadny nakonfigurovany neni, uzivatel je vyzvan k vytvorreni projektu
- Submission pak uz asi klasicky jako doted, navazany na konkretni projekt
