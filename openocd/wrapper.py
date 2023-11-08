from typing import List
from .tclrpc import OpenOcdTclRpc

class OpenOcd(OpenOcdTclRpc):
    def reset_halt(self):
        """Halt MCU and raise an error if it returns an error"""
        return self.run("capture \"reset halt\"")
    
    def halt(self):
        """Halt MCU and raise an error if it returns an error"""
        return self.run("capture \"halt\"")
    
    def resume(self, address=None):
        """Resume the target at its current code position, or the optional address 
        if it is provided. 
        OpenOCD will wait 5 seconds for the target to resume."""
        if address is None:
            return self.run(f"capture \"resume\"")
        else:
            return self.run(f"capture \"resume {address:#0x}\"")
    
    def mww(self, addr:int, word:int):
        """Write the word on addr and raise an error if it returns an error"""
        return self.run(f"capture \"mww {addr:#0x} {word:#0x}\"")
    
    def write_memory(self, address:int, width:int, data:List[int]):
        """This function provides an efficient way to write to the target memory 
        from a Tcl script
        
        address ... target memory address
        
        width ... memory access bit size, can be 8, 16, 32 or 64
        
        data ... Tcl list with the elements to write """
        data_words: List[str] = []
        for word in data:
            data_words.append(str(f"{word:#0x}"))
        data_string = " ".join(data_words)
        return self.run(f"capture \"write_memory {address:#0x} {width} {{{data_string}}}\"")
    
    def write_word(self, address:int, word:int):
        return self.write_memory(address, 32, [word])

    def read_memory(self, address:int, width:int, count:int):
        """This function provides an efficient way to read the target memory from a Tcl script. 
        A Tcl list containing the requested memory elements is returned by this function.

        address ... target memory address
        
        width ... memory access bit size, can be 8, 16, 32 or 64
        
        count ... number of elements to read """
        data = self.run(f"capture \"read_memory {address:#0x} {width} {count}\"").split(" ")
        return list(map(lambda word: int(word, base=16), data))
    
    def read_word(self, address:int):
        """This function provides an efficient way to read the target memory from a Tcl script. 
        A Tcl list containing the requested memory elements is returned by this function.

        address ... target memory address
        
        width ... memory access bit size, can be 8, 16, 32 or 64
        
        count ... number of elements to read """
        data = self.run(f"capture \"read_memory {address:#0x} 32 1\"").split(" ")
        return int(data[0], base=16)

    def load_image(self, filename, address, min_address = "", max_length = "", file_format = ""):
        """Load image from file filename to target memory offset by address from its load address. 
        The file format may optionally be specified (bin, ihex, elf, or s19). 
        In addition the following arguments may be specified: 
            min_addr - ignore data below min_addr (this is w.r.t. to the target’s load address + address) 
            max_length - maximum number of bytes to load."""
        filename = filename.replace("\\", "\\\\")
        return self.run(f"load_image \"{filename}\" {address} {file_format} {min_address} {max_length}")
