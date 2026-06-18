import json
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def fix_latex_in_text(text):
    # Remplacement des délimiteurs de bloc \\[ et \\] par $$
    # On gère le cas des doubles antislashs échappés ou non
    text = re.sub(r'\\\[', '$$', text)
    text = re.sub(r'\\\]', '$$', text)
    
    # Remplacement des délimiteurs en ligne \\( et \\) par $
    text = re.sub(r'\\\(', '$', text)
    text = re.sub(r'\\\)', '$', text)
    
    return text

def fix_notebook(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        modified = False
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                source = cell.get('source', [])
                new_source = []
                for line in source:
                    fixed_line = fix_latex_in_text(line)
                    if fixed_line != line:
                        modified = True
                    new_source.append(fixed_line)
                cell['source'] = new_source
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, ensure_ascii=False, indent=2)
            return True, "Le fichier a été corrigé avec succès !"
        else:
            return True, "Aucune formule à corriger trouvée."
            
    except Exception as e:
        return False, f"Erreur lors du traitement : {str(e)}"

def main():
    # Initialisation de Tkinter sans afficher la fenêtre principale
    root = tk.Tk()
    root.withdraw()
    
    # Boîte de dialogue pour sélectionner un ou plusieurs fichiers .ipynb
    file_paths = filedialog.askopenfilenames(
        title="Sélectionnez le(s) notebook(s) à corriger",
        filetypes=[("Jupyter Notebooks", "*.ipynb"), ("Tous les fichiers", "*.*")]
    )
    
    if not file_paths:
        print("Aucun fichier sélectionné.")
        return

    success_files = []
    failed_files = []
    no_change_files = []

    for path in file_paths:
        file_name = os.path.basename(path)
        success, message = fix_notebook(path)
        if success:
            if "succès" in message:
                success_files.append(file_name)
            else:
                no_change_files.append(file_name)
        else:
            failed_files.append(f"{file_name} ({message})")

    # Rapport final à l'utilisateur
    report = []
    if success_files:
        report.append("Fichiers corrigés :\n" + "\n".join(f"- {f}" for f in success_files))
    if no_change_files:
        if report:
            report.append("")
        report.append("Fichiers déjà corrects :\n" + "\n".join(f"- {f}" for f in no_change_files))
    if failed_files:
        if report:
            report.append("")
        report.append("Échecs :\n" + "\n".join(f"- {f}" for f in failed_files))

    messagebox.showinfo("Résultat du traitement", "\n".join(report))

if __name__ == "__main__":
    main()
