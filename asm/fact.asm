  li rx0, 0    
li rx1, 1  
li rx2, 2     

li rx5, 25    
add rx5, rx5, rx5   
li rx7, 25
add rx7, rx7, rx7   
addi rx7, rx7, 1     

outer: slt rx6, rx2, rx7   
 beq rx6, rx0, done 
 li rx3, 0   
 li rx4, 0    

inner: slt rx6, rx4, rx2   
 beq rx6, rx0, next 
 add rx3, rx3, rx1   
 addi rx4, rx4, 1    
 jmp inner

next:  addi rx1, rx3, 0   
 addi rx2, rx2, 1    
 jmp outer

done:  addi rx1, rx1, 0    
