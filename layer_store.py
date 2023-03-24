from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from layers import *

# ADTs
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from data_structures.bset import BSet
from data_structures.set_adt import *
from layer_util import get_layers


class LayerStore(ABC):

    def __init__(self) -> None:
        pass
        
    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass
  
    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        self.layers = None
        self.spec = False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.spec == True:
            if self.layers == None:
                return invert.apply(start, timestamp, x , y)
            return invert.apply(self.layers.apply(start, timestamp, x, y), timestamp, x, y)
        else:
            if self.layers == None:
                return start
            return self.layers.apply(start, timestamp, x, y)

    def add(self, layer: Layer) -> bool:
        self.layers = layer
        return True
    
    def erase(self, layer: Layer) -> bool:
        self.layers = None
        return True
    
    def special(self):
        self.spec = not self.spec
        
        

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.layers = CircularQueue(100)
    
    def add(self, layer: Layer) -> bool:
        if not self.layers.is_full():
            self.layers.append(layer)    
            
        return not self.layers.is_full()

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.layers.is_empty():
            return start

        else:
            temp_color = start
            for _ in range(len(self.layers)):
                temp_layer = self.layers.serve()
                self.layers.append(temp_layer)
                temp_color = temp_layer.apply(temp_color, timestamp, x, y)
                
            return temp_color

    
    def erase(self, layer: Layer) -> bool:
        if not self.layers.is_empty():
            self.layers.serve()
        return self.layers.is_empty()
            
    def special(self):
        temp_stack = ArrayStack(len(self.layers))
        for _ in range(len(self.layers)):
            temp_stack.push(self.layers.serve())
        for _ in range(len(temp_stack)):
            self.layers.append(temp_stack.pop())
        

        

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """
    def __init__(self) -> None:
        self.layers = ArraySortedList(9)
        self.layers_set = BSet(9)

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.layers.is_empty():
            return start
        else:
            temp_color = start
            for i in range(len(self.layers)):
                temp_color = self.layers[i].value.apply(temp_color, timestamp, x, y)
            return temp_color

    def add(self, layer: Layer) -> bool:
        if layer.index == 0:
            if 10 not in self.layers_set:
                self.layers_set.add(10)
                self.layers.add(ListItem(layer, layer.index))
        else:
            if layer.index not in self.layers_set:
                self.layers_set.add(layer.index)
                self.layers.add(ListItem(layer, layer.index))
     
    def erase(self, layer: Layer) -> bool:
        
        if (layer.index == 0 and 10 not in self.layers_set) or (layer.index != 0 and layer.index not in self.layers_set):
            return False
        elif layer.index == 0 and 10 in self.layers_set:
            self.layers_set.remove(10)
        elif layer.index != 0 and layer.index in self.layers_set :
            self.layers_set.remove(layer.index)
        self.layers.delete_at_index(self.layers._index_to_add(ListItem(layer, layer.index)))

        return True
    
    def special(self):
        if not self.layers.is_empty():
            # Create an ArraySortedList to sort alphabetically
            alphabetical_ordered_list = ArraySortedList(len(self.layers))
            for i in range(len(self.layers)):
                alphabetical_ordered_list.add(ListItem(self.layers[i].value, self.layers[i].value.name))
            
            # Remove from set and list
            if len(alphabetical_ordered_list) % 2 != 0:
                self.erase(alphabetical_ordered_list[(len(self.layers)//2)].value)
                alphabetical_ordered_list.delete_at_index(len(self.layers)//2)
            else:
                self.erase(alphabetical_ordered_list[((len(self.layers)-1)//2)].value)
                alphabetical_ordered_list.delete_at_index((len(self.layers)-1)//2)

   

if __name__ == "__main__":
    
    # asl = ArraySortedList(9)
    # test = ListItem(2, "br")
    # test2 = ListItem(1, "bcdeefefe")
    # asl.add(test2)
    # print(asl)
    # asl.add(test)
    # print(asl)
    # asl.add(ListItem(3, "ba"))
    # print(asl)

    # print(type(math.ceil(3.5)))

    # a = BSet(3)
    # a.add(1)
    # print(len(a))
    a = BSet(3)
