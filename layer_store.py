from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from layers import *
from layer_util import get_layers

# ADTs
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from data_structures.bset import BSet
from data_structures.set_adt import *


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
        """
        Explanation:
        Initialises instance variables:
        - self.layers (Layer) : to store a singular layer object
        - self.spec (Boolean) :   to store a boolean which indicates whether the special effect is on/off
        
        Parameters: self
        Returns: None

        Complexity: O(1)
        """
        self.layers = None
        self.spec = False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Explanation:
        Gets the end-product color from the layer(s) in self.layers.
        Checks if self.spec is true or false (check whether to add special effects or not)
        if true then apply special effects, i.e invert the color
            then checks again whether the current layer exists or not, i.e not None
            if so apply the special effect using start, the base color
            else apply the invert using the color from the current layer
        
        else apply color without speciall effects, i.e apply original color not invert
            then checks again whether the current layer exists or not, i.e not None
            if so apply color using the start, the base color
            else apply the color using the current layer stored in self.layers

        Parameters:
        - self
        - start (tuple)[int, int, int]: base or bottom color represented in a tuple of 3 integers, RGB
        - timestamp (int): is used by some layers for dynamic effects.
        - x (int)   : x/horizontal coordinates of the grid
        - y(int)    : y/vertical coordinates of the grid

        Returns:
        - tuple[int, int, int]: a color tuple of 3 integers (RGB)

        Complexity: O(n)
        n: n is the length of the color tuple, we loop through the color tuple in the apply function
        """
        if self.spec == True:
            if self.layers == None:
                return invert.apply(start, timestamp, x , y) 
            return invert.apply(self.layers.apply(start, timestamp, x, y), timestamp, x, y)
        else:
            if self.layers == None:
                return start
            return self.layers.apply(start, timestamp, x, y)

    def add(self, layer: Layer) -> bool:
        """
        Explanation:
        Checks whether the layer we want to replace is the same as the current layer
        if same, return False
        if not, change the current layer and return true to indicate that the change is successful

        Parameters:
        - self
        - layer (Layer): a Layer object

        Returns:
        - bool: - True if the add process is successful, i.e if the layer we want to add is not the same as
                  the current layer in self.layers. 
                - False if the add process is unsuccessful, i.e if the layer we want to add is the same as
                  the current layer in self.layers. 

                Indicates whether the add process is successful or not.

        Complexity: O(1)
        """
        if layer != self.layers:
            self.layers = layer
            return True
        return False
    
    def erase(self, layer: Layer) -> bool:
        """
        Explanation: 
        Removes the current layer of this layerstore if there is an existing layer

        Parameters:
        - self
        - layer (Layer): a Layer object

        Returns:
        - bool: - True if the erase process is successful, i.e the current layer in self.layers is not None
                - False if the erase process is unsuccessful, i.e the current layer in self.layers is None

              Indicates whether the erase process is successful or not.

        Complexity: O(1)
        """
        if self.layers != None:
            self.layers = None
            return True
        return False
    
    def special(self):
        """
        Explanation:
        Toggles on and off the special effect of the layer.
        if special is toggled on then the color of the current layer is inverted
        if not then it remains the same, uninverted

        Parameters: None
        Returns:    None

        Complexity: O(1)
        """
        self.spec = not self.spec
        
        

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    
    MAX_LAYERS = 900

    def __init__(self) -> None:
        """
        Initialises a CircularQueue which is going to be used to store layers

        Complexity: O(1)
        """
        self.layers = CircularQueue(self.MAX_LAYERS)
    
    def add(self, layer: Layer) -> bool:
        """ 
        Explanation:
        Function to add a layer into self.layers (Circular Queue)

        Parameters:
        - self
        - layer (Layer): a Layer object which we want to add into self.layers

        Returns:
        - bool: - True if the add process is successful, i.e if the Queue is not full
                - False if the add process is unsuccessful, i.e if the Queue is full

              Indicates whether the add process is successful or not

        Complexity: O(1)
        """
        if not self.layers.is_full(): # Checks whether self.layers (Circular Queue) is full
            self.layers.append(layer) # if not, then append the layer we want to add
            return True 
        return False # if full, don't add

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Explanation:
        Gets the end-product color from the layer(s) in self.layers
        Checks whether self.layers is empty or not
        if empty, return start: base color
        if not, keep serving and applying colors from the Queue on top of each other

        Parameters:
        - self
        - start (tuple[int, int, int]) : base or bottom color represented in a tuple of 3 integers, RGB
        - timestamp (int) : an integer value which is used by some layers to create dynamic effects
        - x (int) : X/horizontal coordinates of the grid
        - y (int) : Y/vertical coordinates of the grid

        Returns:
        - tuple[int, int, int]: the end-product color from continuously applying colors stored in self.layers
                 on top of each other (RGB)
        
        Complexity: O(n)
        O(apply)
        n: length of the Circular Queue in self.layers
        """
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
        """
        Explanation:
        Removes the oldest layer in the Circular Queue

        Parameters: 
        - self
        - layer: a Layer object

        Returns:
        - bool: - True if the erase process is successful, i.e if the Queue in self.layers is not empty
                - False if the erase process is unsuccesssful, i.e if the Queue in self.layers is empty
        
        Complexity: O(1)
        """
        if not self.layers.is_empty():
            self.layers.serve()
            return True
        return False
            
    def special(self):
        """
        Explanation:
        Reverse the order of the layers inside the Circular Queue in self.layers

        Parameters: self
        Returns   : None

        Complexity: O(n)
        n: n is the length of Circular Queue in self.layers
        """
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

    NUMBER_OF_LAYERS = 9 # Indicates the number of layers

    def __init__(self) -> None:
        """
        Explanation:
        Initialises instance variables:
        - self.layers (ArrayR)   : a referential array which stores all of the existing arrays,
                                   e.g rainbow, invert, etc.
        - self.layers_set (BSet) : a BSet which is used to store all the layer indexes which
                                   have been added.
        """
        self.layers = get_layers()[:self.NUMBER_OF_LAYERS]
        self.layers_set = BSet(self.NUMBER_OF_LAYERS)

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Explanation:
        Gets the end-product of the color from the layer(s) which are currenty applied
        Checks whether self.layers_set is empty or not (checks whether there are any layers applying)
        if empty return start, the base color
        if not iterate through self.layers, keep on applying the colors whose index+1 are in self.layers_set

        Complexity: O(n)
        n: The length of self.layers
        """
        
        if self.layers_set.is_empty():
            return start
        else:
            temp_color = start
            for i in range(len(self.layers)):
                if self.layers[i].index+1 in self.layers_set:
                    temp_color = self.layers[i].apply(temp_color, timestamp, x, y)
            return temp_color

    def add(self, layer: Layer) -> bool:
        """
        Explanation:
        Function to make a layer apply, adds the layer's index+1 to self.layers_set

        Parameters:
        - layer (Layer): a Layer object

        Returns:
        - bool: - True if we made the layer apply, i.e if the layer's index+1 is not in self.layers_set
                - False if the layer is already applying, i.e if the layer's index+1 is already in self.layers_set

        Complexity: O(1)
        """
        if layer.index+1 not in self.layers_set:
            self.layers_set.add(layer.index+1)
            return True
        return False
            
    def erase(self, layer: Layer) -> bool:
        """
        Explanation:
        Function to make a layer NOT apply, removes the layer's index+1 from self.layers_set

        Parameters:
        - layer (Layer): a layer object

        Returns:
        - bool: - True if we manage to make the layer not apply, i.e if the layer's index+1 is in self.layers_set
                - False if the layer is already not applying, i.e if the layer's index+1 is not in self.layers_set

                Indicates whether the erase process is successful or not
        
        Complexity: O(1)
        """
        if layer.index+1 in self.layers_set:
            self.layers_set.remove(layer.index+1)
        else:
            return False
        return True
    
    def special(self):
        """
        Explanation:
        Function to remove the median applying layer lexicographically ordered

        Parameters: self
        Returns   : None

        Complexity: O(n) 
        n: the length of self.layers 
        """
        if not self.layers_set.is_empty():
            # Create an ArraySortedList to sort alphabetically/lexicographically
            alphabetical_ordered_list = ArraySortedList(len(self.layers_set))
            for i in range(len(self.layers)): # O(n)
                if self.layers[i].index+1 in self.layers_set:
                    alphabetical_ordered_list.add(ListItem(self.layers[i], self.layers[i].name)) 
            
            # Remove from set
            if len(alphabetical_ordered_list) % 2 != 0:
                self.erase(alphabetical_ordered_list[(len(alphabetical_ordered_list)//2)].value)
            else:
                self.erase(alphabetical_ordered_list[((len(alphabetical_ordered_list)-1)//2)].value)


   

if __name__ == "__main__":
    b = BSet(3)
    b.add(10)
    print(b)
