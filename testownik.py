
"""
Pomysły na testy
1) Test zbieżnoci -> puscic 2 razy na dwolonej metodzie (select plus cross_over razy 6) graf 300 i pokazać ze total cost maleje po 1000 iteracji
2) Test na znajdowanie najktrószej ciezki w zaleznosci od iloci iteracji od 200 do 10000 -> grafy 50 - 300 2 razy
3) Test na  zwiększoną mutacje?? Jak?
4) miasta test?

Niech testy zapisują wyniki do pliku od razu po skończeniu danego algorytmu, a nie na sam koniec (dla wygody zbierania wyników)
3): Np na tym samym grafie co w 1) zwiększajmy/zmniejszajmy % mutacji (np. o 0.05 z 6 razy)
4): Może być tak jak zazwyczaj, czyli dla kilku wybranych miast posprawdzać, możemy tutaj np nie bawić się w zwiększanie mutacji czy iteracji
tylko uzależnić je od rozmiaru grafu (np dla grafu o rozmiarze n niech liczba mutacji wyjdzie coś w stylu 1/n, a liczba iteracji załóżmy n^2 / 2)
i dla tych argumentów parę razy puścić
Możemy tutaj ograniczyć się z metodami np używając tych które dawały lepsze wyniki w teście 1) żeby nie trwało za długo
"""