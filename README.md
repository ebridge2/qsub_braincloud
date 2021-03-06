# qsub_braincloud

## Usage  

This is a resource which will submit jobs. It has been tested on the Braincloud cluster.

Test:
Navigate to the folder:
```
qsub/tests
```

To run the test, type:
    
```
    python tests.py
```

Usage:  
    
Each line in cmd_file should be a command which would be run from terminal. IE:  
```
echo "$(cat /your/path/to/repo/qsub/tests/test1.txt)" >> /your/path/to/repo/qsub/tests/testo.txt  
echo "$(cat /your/path/to/repo/qsub/tests/test2.txt)" >> /your/path/to/repo/qsub/tests/testo.txt  
echo "$(cat /your/path/to/repo/qsub/tests/test3.txt)" >> /your/path/to/repo/qsub/tests/testo.txt  
echo "$(cat /your/path/to/repo/qsub/tests/test4.txt)" >> /your/path/to/repo/qsub/tests/testo.txt  
echo "$(cat /your/path/to/repo/qsub/tests/test5.txt)" >> /your/path/to/repo/qsub/tests/testo.txt  
echo "$(cat /your/path/to/repo/qsub/tests/test6.txt)" >> /your/path/to/repo/qsub/tests/testo.txt  
```

Each line in mem_file should be an amount of memory or none. IE:  
```




1M


```

Each line in dep_file should be the zero-indexed line of a command that the command at this line relies on. IE:
```
4


2



```

Running, from a python session:
```
    import qsub
    qsub.qsub_submit(cmd_file, dep_file, mem_file, wd)
```
Will submit your scripts thru qsub. If you use the above as a test, this would produce the result:
```
test2
test3
test6
test5
test4
test1
```

Navigate to qsub/tests for more details.
