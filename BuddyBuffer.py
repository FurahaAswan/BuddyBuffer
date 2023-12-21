import math

# Assignment #7
# Name: Furaha Aswan
# Date: 5/10/2023
#
# This is a program that implements a buddy memory allocator algorithm by using a linked list.  

#Class for the control word of the buffer / the buffer itself.
class Buffer:
    def __init__(self, size, address, next_buffer=None, last_buffer = None):
        self.size = size
        self.address = address
        self.next = next_buffer
        self.last = last_buffer
        self.next_same_size = None
        self.used = False

    #A representation of the Buffer as a string for debugging purposes 
    def __str__(self):
        return f"Buffer Data: Address = {self.address}, Size = {self.size}, used = {self.used}, Next of same size = {self.next_same_size.address if self.next_same_size is not None else self.next_same_size} \n  last: {self.last if self.last is None else self.last.address} next ===> {self.next}"
    
    def find_next_same_size(self):
        start = self
        while start.next != None:
            if start.next.size == self.size:
                self.next_same_size = start.next
                return start.next.used
            else:
                start = start.next

#An implementation of a Doubly linked list specific to this assignment. Just contains an append method for the initialize function.
#The rest of the functionality was done in the BuddyBuffer class. Things like removing, inserting, etc. I found it made it 
#easier to combine and split buffers.
class DoublyLinkedList:
    def __init__(self, head = None):
        self.head = head

    def __str__(self):
        return f"List ====> {self.head}"
    
    def __iter__(self):
        start = self.head
        while start:
            yield start
            start = start.next

    def append(self, node):
        if self.head is None:
            self.head = node
        else:
            start = self.head
            while start.next is not None:
                start = start.next
            start.next = node
            
    
    def update_next_same_size(self):
        for item in self:
            item.find_next_same_size()
          

class BuddyBuffer():
    def __init__(self, min_size, max_size):
        self.min_size = min_size
        self.max_size = max_size
        self.buffer_pool = None

    #Initializes the buffer pool to 10 of the max size buffers
    def initialize(self):
        for i in range(10):
            if i == 0:
                new_buffer = Buffer(self.max_size,0)
                self.buffer_pool = DoublyLinkedList(new_buffer)
            else:
                start = self.buffer_pool.head
                while start.next != None:
                    start = start.next
                new_buffer = Buffer(self.max_size,self.max_size+start.address+1,None,start)
                self.buffer_pool.append(new_buffer)

        self.buffer_pool.update_next_same_size()
        
    #Takes requested block size as input and returns the address of a buffer.
    def allocate(self, size):
        if size > self.max_size or size < self.min_size:
                return -2 # illegal request

        #Calculate the appropiate size buffer that the request should go in 
        buffer_size = 2 ** math.ceil(math.log2(size + 1)) - 1
        
        #If there exits buffer of appropiate size, find it and put request in buffer. 
        if self.count_empty_buffers(buffer_size) > 0:
            buffer = self.buffer_pointer(buffer_size)
            while(buffer.used):
                buffer = buffer.next_same_size
        #Otherwise, find a free buffer that's large enough to hold request
        else:
            buffer = self.find_suitable_buffer(buffer_size)
            if buffer is None:
                return -1 #cannot provide a buffer of that size because of lack of space

        #While buffer isn't the correct size, split it into two.
        while buffer.size != buffer_size:
            half_size = buffer.size // 2
            right_buffer = Buffer(half_size, buffer.address + half_size+1, buffer.next,buffer)
            buffer.size = half_size
            if buffer.next is not None:
                buffer.next.last = right_buffer 
            buffer.next = right_buffer


        buffer.used = True   
        self.buffer_pool.update_next_same_size()

        return buffer.address   

    #Takes the address of the buffer to deallocate as input and recombines buffers that are less than the maximum size if possible.
    def deallocate(self, address):
        buffer = self.find_buffer(address)
        if buffer:
            buffer.used = False
            
            #It's the left buffer
            if buffer.address/8 % 2 == 0:
                self.left_buffer_merge(address)
                    
            #It's the Right buffer
            else:
                left_buffer = buffer.last
                while(left_buffer is not None and left_buffer.size == buffer.size and left_buffer.used == False and left_buffer.size < self.max_size):
                    buffer.size = buffer.size*2+1
                    buffer.last = left_buffer.last
                    buffer.address = left_buffer.address
                    self.buffer_pool.update_next_same_size()

                    if(buffer.address == 0):
                        self.buffer_pool.head = buffer

                    left_buffer = buffer.last
                self.left_buffer_merge(buffer.address)                           
            
    
    #Returns the status of the buffer pool memory, if there are two or fewer max sized buffers it returns True otherwise False. 
    def status(self):
        if self.count_empty_buffers(self.max_size) < 2:
            return False
        else:
            return True
    
    #Returns the number of buffers in each buffer chain
    def debug(self):
        output = "Free Buffer Count: \n"
        output+=f"{self.count_empty_buffers(511)} 511 size buffers\n"
        output+=f"{self.count_empty_buffers(255)} 255 size buffers\n"
        output+=f"{self.count_empty_buffers(127)} 127 size buffers\n"
        output+=f"{self.count_empty_buffers(63)} 63 size buffers\n"
        output+=f"{self.count_empty_buffers(31)} 31 size buffers\n"
        output+=f"{self.count_empty_buffers(15)} 15 size buffers\n"
        output+=f"{self.count_empty_buffers(7)} 7 size buffers\n\n"

        return output
    
    #Looks for first buffer of suitibale size to use
    def find_suitable_buffer(self, size):
        for buffer in self.buffer_pool:
            if buffer.size >= size and buffer.used == False:
                return buffer
        return None   

    #Finds the first buffer of the inputed size, returns None if there aren't any.
    def buffer_pointer(self,size):
        for buffer in self.buffer_pool:
            if buffer.size == size:
                return buffer
        return None
    
    #Counts The Empty buffers available
    def count_empty_buffers(self, buffer_size):
        count = 0
        for buffer in self.buffer_pool:
            if buffer.size == buffer_size and not buffer.used:
                count+=1
        return count
    
    #Finds buffer with the given address.
    def find_buffer(self, address):
        for buffer in self.buffer_pool:
            if buffer.address == address:
                return buffer
        return None
    
    def left_buffer_merge(self, address):
        buffer = self.find_buffer(address)
        if buffer: 
            right_buffer = buffer.next
            #while the right buffer is the same size as left buffer, it's empty, and it's under the max buffer size, then combine the two buffers
            while(right_buffer is not None and right_buffer.size == buffer.size and right_buffer.used == False and right_buffer.size < self.max_size):
                buffer.size = buffer.size*2+1
                buffer.next = right_buffer.next
                if(buffer.next is not None):
                    buffer.next.last = buffer
                self.buffer_pool.update_next_same_size()

                #Increment right buffer for while loop
                right_buffer = buffer.next 

