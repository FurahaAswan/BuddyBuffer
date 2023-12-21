from BuddyBuffer import BuddyBuffer

#Driver that tests out all of the functions and prints results as it goes.  
if __name__ == "__main__":
    b = BuddyBuffer(7,511)
    f = open("output.txt","w")


    #Initializing Buffers
    b.initialize()
    f.write("Initializing Buffers\n")
    f.write(f"Expected values: 10 512 size buffers, Status Ok \n\n")
    f.write(b.debug())
    f.write(f"Status: \n\n{'OK' if b.status else 'Tight'} \n\n\n")

    #Requesting 700
    f.write("Requesting 700\n")
    f.write("Expected values: \nAssigned address: -2\n\n")
    f.write(f"Actual = Assigned Address: {b.allocate(700)} \n\n")

    #Requesting buffer size 7
    f.write("Request buffer size 7\n")
    f.write("Expected values: \n9 511 size buffers, 1 255 size buffer, 1 127 size buffer,\n")
    f.write("1 63 size buffer, 1 31 size buffer, and 1 7 size buffer, Status Ok\n\n")
    f.write(f"Actual = Assigned Address: {b.allocate(7)} \n\n")
    f.write(b.debug())
    f.write(f"Status: \n\n{'OK' if b.status else 'Tight'} \n\n\n")

    #Returning buffer size 7
    f.write("Return buffer size 7\n")
    f.write("Expected values: \n10 511 size buffers, Status Ok\n\n")
    f.write(f"Actual = \n\n")
    b.deallocate(0)
    f.write(b.debug())
    f.write(f"Status: \n\n{'OK' if b.status else 'Tight'} \n\n\n")

    #Requesting 10 buffers size 511
    f.write("Request 10 Buffers\n")
    f.write("Expected values: \n0 511 buffers, 0 for all buffers, Status Tight\n\n")
    for i in range(10):
        f.write(f"Actual = Assigned Address: {b.allocate(511)} \n\n")
    f.write(b.debug())
    f.write(f"Status: \n\n{'OK' if b.status() else 'Tight'} \n\n\n")

    #Requesting buffer size 479
    f.write("Request buffer size 479\n")
    f.write("Expected values: \nAssigned address = -1\n0 511 buffers, 0 for all buffers, Status Tight\n\n")
    f.write(f"Actual = Assigned Address: {b.allocate(479)} \n\n")
    f.write(b.debug())
    f.write(f"Status: \n\n{'OK' if b.status() else 'Tight'} \n\n\n")
    
    #Returning 10 buffers
    f.write("Return 10 buffers size 511\n")
    f.write("Expected values: \n10 511 buffers, Status Ok\n\n")
    for i in range(10):
        b.deallocate(i*512)
    f.write(b.debug())
    f.write(f"Status: \n\n{'OK' if b.status() else 'Tight'} \n\n\n")

    f.write("====================================================================================\n")
    f.write("Additional Tesing\n")
    f.write("====================================================================================\n\n")

    f.write("The following is testing the deallocate merge from the right buffer:\n\n")

    #Request 2 buffers size 7
    f.write("Request 2 buffers size 7\n")
    f.write("Expected values: \n9 511 buffers, 1 of each except 7, 0 7 buffers, Status OK\n\n")
    b.allocate(7)
    b.allocate(7)
    f.write(b.debug())
    f.write(f"Status: \n\n{'OK' if b.status() else 'Tight'} \n\n\n")

    #Return buffer size 7
    f.write("Returning buffer size 7\n")
    f.write("Expected values: \n9 511 buffers, 1 of each, Status OK\n\n")
    b.deallocate(0)
    f.write(b.debug())
    f.write(f"Status: \n\n{'OK' if b.status() else 'Tight'} \n\n\n")

    #Return buffer size 7
    f.write("Returning buffer size 7\n")
    f.write("Expected values: \n10 511 buffers, Status Ok\n\n")
    b.deallocate(8)
    f.write(b.debug())
    f.write(f"Status: \n\n{'OK' if b.status() else 'Tight'} \n\n\n")

    f.close()
    






