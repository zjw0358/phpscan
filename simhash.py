#coding:utf-8
#!/usr/bin/python
# Implementation of Charikar simhashes in Python
# See: http://dsrg.mff.cuni.cz/~holub/sw/shash/#a1

class simhash():
    def __init__(self, tokens='', hashbits=128):
        self.hashbits = hashbits
        self.hash = self.simhash(tokens)

    def __str__(self):
        return str(self.hash)

    def __long__(self):
        return long(self.hash)

    def __float__(self):
        return float(self.hash)

    def simhash(self, tokens):
        # Returns a Charikar simhash with appropriate bitlength
        v = [0]*self.hashbits

        for t in [self._string_hash(x) for x in tokens]:
            bitmask = 0
            #print (t)
            #raw_input()
            for i in range(self.hashbits):
                bitmask = 1 << i
                #print(t,bitmask, t & bitmask)
                if t & bitmask:
                    v[i] += 1 #查看当前bit位是否为1，是的话则将该位+1 
                else:
                    v[i] -= 1 #否则得话，该位减1

        fingerprint = 0
        for i in range(self.hashbits):
            if v[i] >= 0:
                fingerprint += 1 << i 
#整个文档的fingerprint为最终各个位大于等于0的位的和
        return fingerprint

    def _string_hash(self, v):
        # A variable-length version of Python's builtin hash
        if v == "":
            return 0
        else:
            x = ord(v[0])<<7
            m = 1000003
            mask = 2**self.hashbits-1
            for c in v:
                x = ((x*m)^ord(c)) & mask
            x ^= len(v)
            if x == -1: 
                x = -2
            return x

    def hamming_distance(self, other_hash):
        x = (self.hash ^ other_hash.hash) & ((1 << self.hashbits) - 1)
        tot = 0
        while x:
            tot += 1
            x &= x-1
        return tot

    def similarity(self, other_hash):
        a = float(self.hash)
        b = float(other_hash)
        if a>b: return b/a
        return a/b

if __name__ == '__main__':
    s = file('2008.php').read()#.decode("utf-8")
    #s = "just a joke"

    #raw_input("按空格继续")
    #for x in s.split():
    	#print x
    	
    hash1 =simhash(s.split())
    #print("0x%x" % hash1)
    #print ("%s\t0x%x" % (s, hash1))

    #s = file('text2.txt').read().decode("utf-8")
    #s = "iust o ioke"
    s = file('misc.php').read()#.decode("utf-8")
    #for x in s.split():
    	#print x
    	
    	    
    hash2 = simhash(s.split())
    #print ("%s\t[simhash = 0x%x]" % (s, hash2))

    print (hash1.similarity(hash2), "percent similar")
    print (hash1.hamming_distance(hash2), "bits differ out of", hash1.hashbits)