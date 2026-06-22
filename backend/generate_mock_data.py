import pandas as pd
import os
from fpdf import FPDF

def generate_agents():
    data = {
        "Agent": ["Jett", "Omen", "Cypher", "Killjoy", "Reyna"],
        "Role": ["Duelist", "Controller", "Sentinel", "Sentinel", "Duelist"],
        "Agent Description": [
            "Jett's agile and evasive fighting style lets her take risks no one else can.",
            "A phantom of a memory, Omen hunts in the shadows.",
            "The Moroccan information broker, Cypher is a one-man surveillance network.",
            "The genius of Germany, Killjoy secures the battlefield with ease using her arsenal of inventions.",
            "Forged in the heart of Mexico, Reyna dominates single combat."
        ],
        "Ability Slot": ["Ultimate", "Ultimate", "Ultimate", "Ultimate", "Ultimate"],
        "Ability Type": ["Ultimate", "Ultimate", "Ultimate", "Ultimate", "Ultimate"],
        "Ability Name": ["Blade Storm", "From the Shadows", "Neural Theft", "Lockdown", "Empress"],
        "Ability Description": [
            "Equip a set of highly accurate throwing knives that recharge on killing an opponent.",
            "Equip a tactical map. Fire to begin teleporting to the selected location.",
            "Use on a dead enemy player in your crosshairs to reveal the location of all living enemy players.",
            "Equip the Lockdown device. Fire to deploy the device. After a long windup, the device Detains all enemies caught in the radius.",
            "Enter a frenzy, increasing firing speed, equip and reload speed dramatically."
        ]
    }
    df = pd.DataFrame(data)
    df.to_excel("../dataset/agents.xlsx", index=False)
    print("Generated agents.xlsx")

def generate_weapons():
    data = {
        "Weapon": ["Vandal", "Phantom", "Operator", "Sheriff", "Spectre"],
        "Category": ["Rifle", "Rifle", "Sniper", "Sidearm", "SMG"],
        "Cost": [2900, 2900, 4700, 800, 1600],
        "Magazine Size": [25, 30, 5, 6, 30],
        "Fire Rate": [9.75, 11, 0.6, 4, 13.33],
        "Reload Time": [2.5, 2.5, 3.7, 2.25, 2.25],
        "Wall Penetration": ["Medium", "Medium", "High", "High", "Medium"],
        "Head Damage": [160, 156, 255, 159, 78],
        "Body Damage": [40, 39, 150, 55, 26],
        "Leg Damage": [34, 33, 120, 46, 22]
    }
    df = pd.DataFrame(data)
    df.to_excel("../dataset/weapons.xlsx", index=False)
    print("Generated weapons.xlsx")

def generate_patch_notes():
    patches = ["12_11", "12_10", "12_09"]
    os.makedirs("../dataset/patch_notes", exist_ok=True)
    
    for patch in patches:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt=f"Valorant Patch Notes {patch.replace('_', '.')}", ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Welcome to patch {patch.replace('_', '.')}.", ln=True)
        pdf.cell(200, 10, txt="Agent Updates:", ln=True)
        if patch == "12_09":
            pdf.cell(200, 10, txt="- Jett received a nerf. Tailwind duration reduced.", ln=True)
            pdf.cell(200, 10, txt="- Omen received a buff. Paranoia speed increased.", ln=True)
        else:
            pdf.cell(200, 10, txt="- Various bug fixes and minor adjustments to ability timings.", ln=True)
            
        pdf.cell(200, 10, txt="Weapon Updates:", ln=True)
        if patch == "12_11":
            pdf.cell(200, 10, txt="- Vandal headshot damage remains at 160, but reload time increased.", ln=True)
        else:
            pdf.cell(200, 10, txt="- No major weapon changes in this patch.", ln=True)
            
        pdf.output(f"../dataset/patch_notes/patch_{patch}.pdf")
        print(f"Generated patch_{patch}.pdf")

if __name__ == "__main__":
    generate_agents()
    generate_weapons()
    generate_patch_notes()
    print("Mock data generation complete.")
