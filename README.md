# karton-minhash
Aurora karton for calculating minhash from input dataset. 

**Consumes:**
```
{
    "type":     "feature",
    "stage":    "raw"
    "kind":     "strings" || "disasm"
    "payload": {
        "data":     "list of data to minhash",
        "sha256":   "sha256 of the sample containing the data"
    }
} 
```

**Produces:**
```
{
    "type":     "feature",
    "stage":    "minhash"
    "kind":     "strings" || "disasm"  
    "payload": {
        "seed":         "minhash seed"
        "hash_values":  "minhash hash values list"
        "sha256":       "sha256 of the sample containing the minhash"
    }
}
```