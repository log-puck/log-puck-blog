import time
import random

def gestalt_collapse_simulation(word, iterations=20):
    """
    Simula la perdita di significato di una parola (Gestalt) 
    attraverso la saturazione e la degradazione visiva.
    """
    degraded_word = list(word)
    
    print(f"--- Inizio analisi del Koan: {word} --- \n")
    
    for i in range(iterations):
        # Aumentiamo la probabilità di "crollo" col passare del tempo
        collapse_chance = i / iterations
        
        # Simuliamo la saturazione: i caratteri iniziano a spostarsi o cambiare
        if random.random() < collapse_chance:
            idx = random.randint(0, len(degraded_word) - 1)
            # Sostituiamo un carattere con uno simile ma "privo di senso" o spazio
            degraded_word[idx] = random.choice([" ", "/", "\\", "|", "_", "."])
        
        current_state = "".join(degraded_word)
        
        # Formattazione per mostrare il progresso
        print(f"Iterazione {i+1:02d}: {current_state}")
        
        # Lo sleep simula il tempo che l'occhio impiega a fissare l'oggetto
        time.sleep(0.3)
    
    print("\n--- Gestalt Collapse Completata ---")
    print("La forma è vuoto, il significato è svanito.")

# Eseguiamo la simulazione sul tuo Koan
gestalt_collapse_simulation("MU")