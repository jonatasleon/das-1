from typing import List
from pattern_matcher import WILDCARD
from db_interface import DBInterface

def _build_node_handle(node_type: str, node_name: str) -> str:
    return f'<{node_type}: {node_name}>'

def _build_link_handle(link_type: str, target_handles: List[str]) -> str:
    if link_type == 'Similarity' or link_type == 'Set':
        target_handles.sort()
    return f'<{link_type}: {target_handles}>'
    
class StubDB(DBInterface):

    def __init__(self):

        human = _build_node_handle('Concept', 'human')
        monkey = _build_node_handle('Concept', 'monkey')
        chimp = _build_node_handle('Concept', 'chimp')
        snake = _build_node_handle('Concept', 'snake')
        earthworm = _build_node_handle('Concept', 'earthworm')
        rhino = _build_node_handle('Concept', 'rhino')
        triceratops = _build_node_handle('Concept', 'triceratops')
        vine = _build_node_handle('Concept', 'vine')
        ent = _build_node_handle('Concept', 'ent')
        mammal = _build_node_handle('Concept', 'mammal')
        animal = _build_node_handle('Concept', 'animal')
        reptile = _build_node_handle('Concept', 'reptile')
        dinosaur = _build_node_handle('Concept', 'dinosaur')
        plant = _build_node_handle('Concept', 'plant')
    
        self.all_nodes = [human, monkey, chimp, snake, earthworm, rhino, triceratops, vine, ent, mammal, animal, reptile, dinosaur, plant]

        self.all_links = [
            ['Similarity', human, monkey],
            ['Similarity', human, chimp],
            ['Similarity', chimp, monkey],
            ['Similarity', snake, earthworm],
            ['Similarity', rhino, triceratops],
            ['Similarity', snake, vine],
            ['Similarity', human, ent],
            ['Inheritance', human, mammal],
            ['Inheritance', monkey, mammal],
            ['Inheritance', chimp, mammal],
            ['Inheritance', mammal, animal],
            ['Inheritance', reptile, animal],
            ['Inheritance', snake, reptile],
            ['Inheritance', dinosaur, reptile],
            ['Inheritance', triceratops, dinosaur],
            ['Inheritance', earthworm, animal],
            ['Inheritance', rhino, mammal],
            ['Inheritance', vine, plant],
            ['Inheritance', ent, plant],
            ['List', _build_link_handle('Inheritance', [dinosaur, reptile]), _build_link_handle('Inheritance', [triceratops, dinosaur])],
            ['Set', _build_link_handle('Inheritance', [dinosaur, reptile]), _build_link_handle('Inheritance', [triceratops, dinosaur])],
            ['List', human, ent, monkey, chimp],
            ['List', human, mammal, triceratops, vine],
            ['List', human, monkey, chimp],
            ['List', triceratops, ent, monkey, snake],
            ['Set', triceratops, vine, monkey, snake],
            ['Set', triceratops, ent, monkey, snake],
            ['Set', human, ent, monkey, chimp],
            #['Set', vine, monkey, plant, triceratops],
            ['Set', mammal, monkey, human, chimp],
            ['Set', human, monkey, chimp]
        ]


    def __repr__(self):
        return '<StubDB>'

    def node_exists(self, node_type: str, node_name: str) -> bool:
        return _build_node_handle(node_type, node_name) in self.all_nodes

    def link_exists(self, link_type: str, targets: List[str]) -> bool:
        return _build_link_handle(link_type, targets) in [_build_link_handle(link[0], link[1:]) for link in self.all_links]

    def get_node_handle(self, node_type: str, node_name: str) -> str:
        node_handle = _build_node_handle(node_type, node_name)
        for node in self.all_nodes:
            if node == node_handle:
                return node
        return None

    def is_ordered(self, handle: str) -> bool:
        for link in self.all_links:
            if _build_link_handle(link[0], link[1:]) == handle:
                return link[0] != 'Similarity' and link[0] != 'Set'
        return True

    def get_link_handle(self, link_type: str, target_handles: List[str]) -> str:
        for link in self.all_links:
            if link[0] == link_type and len(target_handles) == (len(link) - 1):
                if link_type == 'Similarity':
                    if all(target in target_handles for target in link[1:]):
                        return _build_link_handle(link_type, link[1:])
                elif link_type == 'Inheritance':
                    for i in range(0, len(target_handles)):
                        if target_handles[i] != link[i + 1]:
                            break
                    else:
                        return _build_link_handle(link_type, target_handles)
                else:
                    raise ValueError(f"Invalid link type: {link_type}")
        return None

    def get_link_targets(self, handle: str) -> List[str]:
        for link in self.all_links:
            if _build_link_handle(link[0], link[1:]) == handle:
                return link[1:]
        return None

    def get_matched_links(self, link_type:str, target_handles: List[str]) -> str:
        answer = []
        for link in self.all_links:
            if len(target_handles) == (len(link) - 1) and link[0] == link_type:
                if link[0] == 'Similarity' or link[0] == 'Set':
                    if all(target == WILDCARD or target in link[1:] for target in target_handles):
                        answer.append(_build_link_handle(link[0], link[1:]))
                elif link[0] == 'Inheritance' or link[0] == 'List':
                    for i in range(0, len(target_handles)):
                        if target_handles[i] != WILDCARD and target_handles[i] != link[i + 1]:
                            break
                    else:
                        answer.append(_build_link_handle(link[0], link[1:]))
                else:
                    raise ValueError(f"Invalid link type: {link[0]}")
        return answer

