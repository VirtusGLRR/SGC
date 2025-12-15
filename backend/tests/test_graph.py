import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from services.graph.graph import graph

thread = {"configurable": {"thread_id": "1"}}

def main():
    while True:
        msg = input("Você: ")
        if msg.lower() in ['sair', 'exit', 'quit']:
            break
        for s in graph.stream({
            'user_input': msg,
        }, thread):
            print(s)

if __name__ == "__main__":
    main()