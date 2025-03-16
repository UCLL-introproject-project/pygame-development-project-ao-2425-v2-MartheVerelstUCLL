def count(file):
    with open(file, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        text = ''.join(lines[1:]) 
        words = text.split()
        number = len(words)
    print(f"Woorden: {number}")

count(r"pygame-development-project-ao-2425-v2-MartheVerelstUCLL\project-challenges\02. professional communication.txt")
count(r"pygame-development-project-ao-2425-v2-MartheVerelstUCLL\project-challenges\03. stack overflow.txt")