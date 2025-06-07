import random

class Node:
    def __init__(self, name):
        self.name = name
        self.rating = 0
        self.next = None
        self.prev = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.current = None
        self.size = 0
    
    def add(self, name):
        new_node = Node(name)
        
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.current = new_node
        else:
            last = self.head.prev
            last.next = new_node
            new_node.prev = last
            new_node.next = self.head
            self.head.prev = new_node
        
        self.size += 1
    
    def move(self, steps, direction):
        if self.size == 0:
            return
            
        steps %= self.size
        if steps == 0:
            return
        
        if direction == "clockwise":
            for _ in range(steps):
                self.current = self.current.next
        else:
            for _ in range(steps):
                self.current = self.current.prev
    
    def get_players_sorted(self):
        if self.size == 0:
            return []
        
        players = []
        current = self.head
        order = 0
        player_order = {}
        
        for _ in range(self.size):
            player_order[current] = order
            players.append((current.name, current.rating, order))
            current = current.next
            order += 1
        
        players.sort(key=lambda x: (-x[1], x[2]))
        return players

print("=" * 50)
print("ИГРА 'ДОБРОЕ ДЕЛО'")
print("=" * 50)

try:
    with open("Students.txt", 'r', encoding='utf-8') as file:
        names = [line.strip() for line in file if line.strip()]
except:
    print("Ошибка при чтении файла Students.txt")
    exit()

cdll = CircularDoublyLinkedList()
for name in names:
    cdll.add(name)

print(f"\nВ игре участвуют {cdll.size} учеников:")
print(", ".join(names))

while True:
    try:
        rounds = int(input("\nВведите количество раундов игры: "))
        if rounds >= 0:
            break
        print("Количество раундов должно быть неотрицательным.")
    except:
        print("Число должно быть целым.")

print("\n" + "=" * 50)
print("НАЧАЛО ИГРЫ")
print("=" * 50)

for round_num in range(1, rounds + 1):
    number = random.randint(-10, 10)
    
    if number > 0:
        steps = number - 1
        cdll.move(steps, "clockwise")
    elif number < 0:
        steps = abs(number) - 1
        cdll.move(steps, "counterclockwise")
    
    cdll.current.rating += 1
    
    print(f"\nРаунд {round_num}:")
    print(f"Выпало число: {number}")
    print(f"Делает доброе дело: {cdll.current.name}")
    print(f"Текущий рейтинг: {cdll.current.rating}")
    
    if number >= 0:
        cdll.current = cdll.current.next
    else:
        cdll.current = cdll.current.prev

print("\n" + "=" * 50)
print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
print("=" * 50)
print("Рейтинг учеников (по убыванию):")

sorted_players = cdll.get_players_sorted()
for i, (name, rating, _) in enumerate(sorted_players, 1):
    print(f"{i}. {name}: {rating}")