# Buddy Buffer Memory Management System

I undertook a project in CISC 310 - Operating Systems that involved developing a Buddy Buffer Memory Management System. This system is designed to handle the dynamic allocation and deallocation of memory blocks, adjusting to file sizes automatically. Here's a detailed explanation of the project:

## Objective and Functionality

- The primary goal is to efficiently allocate and deallocate memory blocks.
- The system operates dynamically, adjusting memory blocks based on the file size.

## Dynamic Memory Allocation

- Memory is allocated at runtime for flexibility in managing memory based on varying program needs.
- Dynamic data structures such as binary trees and linked lists are utilized for managing memory allocation.

## Binary Trees and Linked Lists

- Binary trees help organize and search for available memory blocks efficiently.
- Linked lists manage free memory blocks, updating as memory is allocated or deallocated.

## Buddy System

- The "buddy system" allocates memory in blocks that are powers of two, with each block having a corresponding "buddy."
- When a block is divided, resulting sub-blocks become buddies.
- This system simplifies allocation and deallocation by merging buddies when both are free.

## Benefits of Buddy Buffer Memory Management

- Efficient use of memory is achieved by minimizing fragmentation.
- Fast allocation and deallocation are possible through binary trees or linked lists.
- Automatic adjustment of memory blocks based on file size ensures resource efficiency.

## Learning Outcomes

- Developed insights into the intricacies of memory management in operating systems.
- Gained understanding of binary trees and linked lists in the context of practical memory management.
