import logging
from collections import deque

# Настроим логирование
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node({self.value})"


def walk_tree(root, log_file):
    """Обход дерева в ширину (BFS) с логированием."""
    queue = deque([root])
    with open(log_file, "w") as f:
        while queue:
            node = queue.popleft()
            left_value = node.left.value if node.left else "None"
            right_value = node.right.value if node.right else "None"
            log_entry = f"{node.value} -> {left_value}, {right_value}\n"
            f.write(log_entry)
            logger.info(log_entry.strip())
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)


def restore_tree(log_file):
    """Восстанавливает бинарное дерево из лог-файла."""
    nodes = {}  # Словарь для хранения узлов по их значениям
    parent_map = {}  # Временный словарь для связей родитель -> дети

    with open(log_file, "r") as f:
        for line in f:
            parent, children = line.strip().split(" -> ")
            left, right = children.split(", ")

            parent = int(parent)
            left = int(left) if left != "None" else None
            right = int(right) if right != "None" else None

            if parent not in nodes:
                nodes[parent] = BinaryTreeNode(parent)
            if left and left not in nodes:
                nodes[left] = BinaryTreeNode(left)
            if right and right not in nodes:
                nodes[right] = BinaryTreeNode(right)

            parent_map[parent] = (left, right)

    for parent, (left, right) in parent_map.items():
        if left is not None:
            nodes[parent].left = nodes[left]
        if right is not None:
            nodes[parent].right = nodes[right]

    return nodes[min(nodes.keys())]  # Возвращаем корень (наименьшее значение)


# --- Тестируем ---
if __name__ == "__main__":
    root = BinaryTreeNode(1)
    root.left = BinaryTreeNode(2)
    root.right = BinaryTreeNode(3)
    root.left.left = BinaryTreeNode(4)
    root.left.right = BinaryTreeNode(5)

    log_file = "tree_log.txt"

    print("🔹 Записываем дерево в лог...")
    walk_tree(root, log_file)

    print("🔹 Восстанавливаем дерево из лога...")
    restored_root = restore_tree(log_file)

    print("✅ Восстановленный корень:", restored_root)
