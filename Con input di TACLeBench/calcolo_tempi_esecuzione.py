import os
import subprocess
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt


# Funzione che compila ed esegue tutti i benchmarks
def run_all_benchmarks(base_path):
    # Lista per salvare i tempi di esecuzione di ogni benchmark
    execution_times = []
    
    # Verifica iniziale sul percorso: se base_path non corrisponde alla cartella in cui ci si trova, 
    # si estrae il percorso corretto (current working directory)
    if not os.path.exists(base_path):
        print(f"ERROR: la cartella '{base_path}' non esiste")
        print(f"Percorso attuale in cui ci si trova: {os.getcwd()}")
        return []

    # Inzio dell'analisi nella cartella base_path
    print(f"-- Inizio della scansione nella cartella {base_path} --")
    print()

    for root, directories, files in os.walk(base_path):
        
        # Si considerano solo i file che terminano con .c e si salvano nella variabile c_files
        c_files = [f for f in files if f.endswith('.c')]
        
        # Se non ci sono file .c nella cartella in esame, si riparte esaminando un'altra cartella
        if not c_files:
            continue

        # Nome del benchmark di cui il file c in esame fa parte
        benchmark_name = os.path.basename(root)
        
        # Nome del file oggetto generato per l'esecuzione test che serve per estrarre il tempo di esecuzione di ciascun benchmark
        exe_name = "test"
        
        # Fase di Compilazione
        cmd_compile = ["gcc"] + c_files + ["-o", exe_name, "-w"]
        
        try:
            # Si compila nella cartella in esame
            subprocess.check_call(cmd_compile, cwd=root)
        except subprocess.CalledProcessError:
            print(f"SKIP: compilazione fallita per: {benchmark_name}")
            continue

        # Fase di Esecuzione
        # Si specifica "./" così da eseguire il file nella directory in cui si trova (Linux)
        cmd_run = ["./" + exe_name]
        
        # Si costruisce il percorso assoluto, necessario per poi rimuovere il file oggetto
        exe_absolute_path = os.path.join(root, exe_name)
        
        # Calcolo del tempo di esecuzione di ciascun benchmark, usando perf_counter
        try:
            # Si prende il tempo in cui inizia l'esecuzione
            start_time = time.perf_counter()
            
            # Si esegue il run dell'exe del benchmark in esame
            subprocess.run(
                cmd_run, 
                cwd=root, 
                check=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            
            # Si prende il tempo in cui finisce l'esecuzione
            end_time = time.perf_counter()
            
            # Si calcola il tempo di esecuzione del benckmark in esame
            execution_time = end_time - start_time

            # Si appende il tempo di esecuzione appena calcolato alla lista dei tempi di esecuzione dei benchmark
            execution_times.append({'benchmark_name': benchmark_name, 'execution_time': execution_time})
            
            print(f"DONE: {benchmark_name.ljust(20)} {execution_time:.6f} s")

        except subprocess.CalledProcessError:
            print(f"RUNTIME ERROR: {benchmark_name}")
        except Exception as e:
            print(f"ERROR: {benchmark_name}: {e}")
        finally:
            # Rimozione del file eseguibile usato per calcolare il tempo di esecuzione del benchmark in esame
            if os.path.exists(exe_absolute_path):
                os.remove(exe_absolute_path)

    # Si ritorna la lista dei tempi di esecuzione
    return execution_times


# Funzione che crea il diagramma a barre per il calcolo dei tempi di esecuzione dei vari benchmarks 
def plot_barchart(name_csv_file):
    try:
        # Lettura dei dati dal file .csv
        df = pd.read_csv(name_csv_file)
    except FileNotFoundError:
        print(f"ERROR: Non è stato possibile trovare il file '{name_csv_file}'")
        return

    # Si ordinano i tempi di esecuzione dal più veloce al più lento
    df = df.sort_values(by='execution_time', ascending=True)

    plt.figure(figsize=(12, 10))

    # Si crea il diagramma a barre orizzontali usando barh, 
    # tenendo presente che sulle ascisse si trovano i nomi dei benchmark e 
    # sulle ordinate il tempo di esecuzione di ciascun benchmark
    bars = plt.barh(df['benchmark_name'], df['execution_time'], color='pink', edgecolor='pink')

    plt.xlabel('Tempo di Esecuzione in secondi', fontsize=13)
    plt.ylabel('Nome del Benchmark', fontsize=13)
    plt.title('Tempi di esecuzione dei vari benchmark in TACLeBench con input originali', fontsize=16)
    
    # Si aggiunge una griglia verticale
    plt.grid(axis='x', linestyle='--', alpha=0.6)

    # Si aggiunge il valore numerico in fondo a ogni barra
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, f'{width:.5f} s', va='center', ha='left', fontsize=8, color='black')

    # Si evita che i nomi lunghi vengano tagliati
    plt.tight_layout()

    # Salvataggio del diagramma a barre creato come immagine .png di elevata qualità
    plt.savefig('diagramma_a_barre_dei_tempi_di_esecuzione.png', dpi=300)



# Fase di Chiamata delle funzioni: run_all_benchmarks e plot_barchart

# Si inserisce il percorso dei benchmarks
benchmarks_path = "bench" 

if __name__ == "__main__":
    # Chiamata della funzione run_all_benchmarks
    if os.path.exists(benchmarks_path):
        execution_times = run_all_benchmarks(benchmarks_path)
    
    if execution_times:
        print("Risultati - nome benchmark tempo di esecuzione")
        print()

        # Si ordinano i tempi di esecuzione dal più piccola al più grande
        execution_times.sort(key=lambda x: x['execution_time'])
        
        # Stampa a schermo dei tempi di esecuzione per ogni benchmark
        for et in execution_times:
            print(f"{et['benchmark_name']}: {et['execution_time']:.6f} s")
        
        # Salvataggio dei tempi di esecuzione di ciascun benchmark in un file .csv
        with open('tempi_di_esecuzione_benchmarks.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['benchmark_name', 'execution_time'])
            writer.writeheader()
            writer.writerows(execution_times)

        # Chiamata della funzione plot_barchart
        plot_barchart('tempi_di_esecuzione_benchmarks.csv')