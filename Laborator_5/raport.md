# Raport – forensics și steganografie

## 1. Obiectivul lucrării

Scopul lucrării a fost studierea metodelor de analiză a datelor și fișierelor utilizate în domeniul securității cibernetice. Au fost implementate tehnici de decodificare a mesajelor, identificare a tipului real al fișierelor, extragere a metadatelor, recuperare a fișierelor ascunse și utilizare a steganografiei.

## 2. Realizarea lucrării

În prima parte a lucrării a fost dezvoltat un decoder universal în Python, capabil să recunoască și să decodifice reprezentări URL, hexadecimal și Base64. Au fost analizate diferențele dintre text și octeți, iar decodificarea succesivă a permis identificarea conținutului ascuns în mai multe straturi. De asemenea, au fost testate toate cele 256 de chei posibile pentru un XOR cu un octet și a fost implementat un atac cu dicționar pentru identificarea unei parole pe baza hash-ului.

În a doua parte au fost analizate semnăturile binare ale fișierelor pentru determinarea formatului real, independent de extensie. Cu ajutorul expresiilor regulate au fost extrase secvențe de text imprimabil dintr-un fișier binar. Biblioteca Pillow a fost utilizată pentru examinarea metadatelor EXIF și a coordonatelor GPS. Totodată, a fost recuperată o arhivă ZIP adăugată la sfârșitul unui fișier imagine, prin identificarea semnăturii sale.

Ultima etapă a constat în implementarea steganografiei LSB (Least Significant Bit). Un mesaj a fost ascuns prin modificarea ultimului bit al canalelor de culoare ale pixelilor unei imagini, iar rezultatul a fost salvat în format PNG. Ulterior, biții au fost extrași în aceeași ordine și reasamblați în octeți pentru recuperarea mesajului original.

## 3. Rezultatele obținute

În urma decodificării mesajului cu straturi multiple, a fost obținută valoarea textului ASCII 'SYWY'. În cadrul atacului XOR a fost identificată cheia '128', iar prin atacul cu dicționar a fost găsită parola 'password'.

Analiza fișierelor a permis verificarea tipurilor reale pe baza semnăturilor binare, identificarea textului imprimabil și examinarea metadatelor fotografiei, inclusiv a informațiilor GPS disponibile. Arhiva ZIP ascunsă a fost extrasă într-un fișier separat pentru examinarea conținutului său.

Prin aplicarea steganografiei LSB, mesajul 'FLAG{ascuns_in_pixeli}' a fost introdus în imagine și recuperat ulterior prin citirea biților de culoare. Acest rezultat a demonstrat că informația poate fi ascunsă într-un fișier aparent obișnuit, fără modificări vizuale evidente.

## 4. Concluzii

Lucrarea a demonstrat aplicarea practică a unor tehnici fundamentale de analiză criminalistică digitală. Decodificarea, atacurile XOR și cu dicționar, examinarea semnăturilor binare și extragerea metadatelor permit identificarea și recuperarea informațiilor care nu sunt imediat vizibile utilizatorului.

De asemenea, exercițiile au evidențiat importanța examinării conținutului real al fișierelor, nu doar a extensiilor acestora, precum și riscurile asociate divulgării metadatelor personale. Steganografia LSB a ilustrat posibilitatea ascunderii mesajelor în imagini, iar recuperarea lor a confirmat importanța analizei la nivel de octet și bit.

În concluzie, tehnicile studiate constituie instrumente utile pentru investigarea fișierelor suspecte, identificarea informațiilor ascunse și înțelegerea metodelor utilizate în analiza de securitate cibernetică.
