def removeGuy(n):
 if n[0]+n[len(n)-1] >= 5: 
  n.remove(n[0])
  n.remove(n[len(n)-1])
  return n
 else:
   return n
print(removeGuy([1,2,3,4,5,6]))