from .transducer import Transducer
from .science import HolisticScience
from .recorder import Recorder

def main():
    print("\n" + "="*50)
    print("   SYNTHIUM OMEGA v1.5")
    print("   Reality Compiler")
    print("="*50 + "\n")

    tool = Transducer()
    lab = HolisticScience()
    scribe = Recorder()

    while True:
        print("\n--- MENU ---")
        print("1. Quantify new phenomenon")
        print("2. Search lexicon")
        print("3. View statistics")
        print("4. Exit")
        
        choice = input("\nSelect: ").strip()

        if choice == "1":
            name = input("\nPhenomenon name: ").strip()
            desc = input(f"Describe '{name}': ").strip()
            
            try:
                vector = tool.quantify(desc)
                print(f"\n[VECTOR]: {vector}")
                
                analysis = lab.analyze(vector)
                print("\n[ANALYSIS]:")
                for k, v in analysis.items():
                    print(f"  {k}: {v}")
                
                if input("\nSave to lexicon? (y/n): ").lower() == 'y':
                    scribe.save_discovery(name, vector, analysis['derived_formula'])
            
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            term = input("\nSearch term: ").strip()
            entry = scribe.find_entry(term)
            if entry:
                print(f"\nFound: {entry['term']}")
                print(f"Formula: {entry['formula']}")
                print(f"Vector: {entry['vector']}")
            else:
                print("Not found.")

        elif choice == "3":
            stats = scribe.get_statistics()
            print(f"\nLexicon has {stats['total_entries']} entries")
            print(f"Last modified: {stats['last_modified']}")

        elif choice == "4":
            print("\nGoodbye.\n")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
