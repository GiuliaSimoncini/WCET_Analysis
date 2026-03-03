## WCET ANALYSIS

### Organizzazione del codice

- `Con input di TACLeBench`:
    - `bench`: contiene i benchmark che sono stati usati per l'analisi e sono una parte di quelli presenti in TACLeBench
    - `calcolo_tempi_esecuzione.py` è il codice Python che è stato usato per calcolare i tempi di esecuzione dei vari benchmarks, riportandoli sia in un file .csv che in un diagramma a barre
    - `diagramma_a_barre_dei_tempi_di_esecuzione.png` è il diagramma a barre che riporta per ogni benchmark il relativo tempo di esecuzione
    - `tempi_di_esecuzione_benchmarks.csv` è il file .csv che contiene il nome del benchmark e il relativo tempo di esecuzione

- `Con input modificati`:
    - `bench`: contiene i benchmark che sono stati usati per l'analisi e sono una parte di quelli presenti in TACLeBench, a cui sono stati modificati gli input
    - `calcolo_tempi_esecuzione.py` è il codice Python che è stato usato per calcolare i tempi di esecuzione dei vari benchmarks, riportandoli sia in un file .csv che in un diagramma a barre
    - `diagramma_a_barre_dei_tempi_di_esecuzione.png` è il diagramma a barre che riporta per ogni benchmark il relativo tempo di esecuzione
    - `tempi_di_esecuzione_benchmarks.csv` è il file .csv che contiene il nome del benchmark e il relativo tempo di esecuzione

- `Simultaneous confidence bands DKW`:
    - `calcolo_tempo_esecuzione_bsort.py` è il codice Python che è stato usato per calcolare il tempo di esecuzione di ciascuna delle 1000 esecuzioni dell'algoritmo bubble sort sia nel caso di input randomici che nel caso di input parzialmente ordinati, per salvare tali tempi in due file .csv  (uno per ogni casistica) e per realizzare tre grafici (uno per l'esecuzione con input randomici, uno per quella con input parzialmente ordinati e uno riportante i due casi precedenti sovrapposti) aventi tre sottografici (un line plot, un istogramma e il grafico che mostra le simultaneous confidence bands DKW)
    - `bubble_sort_completely_random.c` è il codice C che effettua l'algoritmo bubble sort usando input randomici
    - `bubble_sort_partially_ordered.c` è il codice C che effettua l'algoritmo bubble sort usando input parzialmente ordinati
    - `bsort_random_times.csv` è il file .csv che contiene il tempo di esecuzione di ciascuna delle 1000 esecuzioni dell'algoritmo bubble sort con input randomici
    - `bsort_partial_times.csv` è il file .csv che contiene il tempo di esecuzione di ciascuna delle 1000 esecuzioni dell'algoritmo bubble sort con input parzialmente ordinati
    - `bsort_plot_random.png` è il grafico avente tre sottografici (un line plot, un istogramma e il grafico che mostra le simultaneous confidence bands DKW) relativo al caso delle 1000 esecuzioni dell'algoritmo bubble sort con input randomici
    - `bsort_plot_partial.png` è il grafico avente tre sottografici (un line plot, un istogramma e il grafico che mostra le simultaneous confidence bands DKW) relativo al caso delle 1000 esecuzioni dell'algoritmo bubble sort con input parzialmente ordinati
    - `bsort_plot_combined.png` è il grafico (avente tre sottografici) che mostra, sovrapposti, il grafico ottenuto nel caso delle 1000 esecuzioni dell'algoritmo bubble sort con input randomici e quello ottenuto nel caso di input parzialmente ordinati