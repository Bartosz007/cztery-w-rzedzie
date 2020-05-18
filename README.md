Bartosz Krawczyk
Album: 130534
# Projekt cztery w rzędzie
>Jest gra logiczna, w której toczy się dopóki jeden z graczy nie ułoży czterech pinków w rzędzie

### Opis zadania:
* Okno wyświetla siatkę 7 kolumn x 6 wierszy, przycisk nad każdą kolumną oraz informacje o turze gracza, przycisk, który resetuje grę, nie zamykając okna
* Okno również zawiera rozwijalną listę poziomów trudności
* Okno zawiera komunikaty z gry informujący o turach i wyniku gry
* Wystepuje opcja wyboru drugiego gracza komputerowego(domyślnie) lub człowieka
* Gracz komputerowy jest zrealizowany za pomocą algorytmu minimax
* Początkowo pola siatki są puste
* Gracze na przemian wrzucają monety do wybranych kolumn
* Wybór kolumny polga na naciśnięciu przycisku ponad nią
* Pola gracza 1 są czerwone, a gracza drugiego żółte
* Wygrywa gracz, który ułoży cztery monety w rzędzie - pionowo, poziomo lub skośnie
* Po zakończeniu gry pojawia się okno z komunikatem o wyniku gry oraz opcja dialogowa, w której można zakończyć program lub z zacząć od nowa grę
* Projekt jest podzielony na klasę generującą interfejs, klasę obsługującą grę oraz funkcje obsługującę gracza komputerowego

### Testy:
* Wykonanie po dwa ruchy przez każdego z graczy - monety spadają na dół pola gry lub zatrzymują się na już wrzuconym żetonie
* Ułożenie pionowej linii monet przez jednego gracza - oczekiwana informacja o jego wygranej
* Ułożenie poziomej linii monet przez drugiego gracza - oczekiwana informacja o jego wygranej
* Ułożenie skośnej linii przez dowolnego gracza - oczekiwana informacja o jego wygranej
* Zapełnienie pola gry tak, że żaden gracz nie ułożył linii - oczekiwana informacja o remisie
* Ułożenie linii dłuższej niż 4 przez jednego z graczy - oczekiwana informacja o jego wygranej
* Próba wrzucenia monety do zapełnionej kolumny - oczekiwana informacja o błędzie

> Link do GitHuba: https://github.com/Bartosz007/cztery-w-rzedzie