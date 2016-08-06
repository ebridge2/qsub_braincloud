# qsub_braincloud

## Usage  

This is a resource which will submit jobs. It has been tested on the Braincloud cluster.

Usage:  
    python qsub_util.py cmd_file dep_file mem_file /path/to/working/dir
    
Each line in cmd_file should be a command which would be run from terminal. IE:  
      echo "$(cat /home/eric/qsub_braincloud/qsub/tests/test1.txt)" >> /home/eric/qsub_braincloud/qsub/tests/testo.txt  
      echo "$(cat /home/eric/qsub_braincloud/qsub/tests/test2.txt)" >> /home/eric/qsub_braincloud/qsub/tests/testo.txt  
      echo "$(cat /home/eric/qsub_braincloud/qsub/tests/test3.txt)" >> /home/eric/qsub_braincloud/qsub/tests/testo.txt  
      echo "$(cat /home/eric/qsub_braincloud/qsub/tests/test4.txt)" >> /home/eric/qsub_braincloud/qsub/tests/testo.txt  
      echo "$(cat /home/eric/qsub_braincloud/qsub/tests/test5.txt)" >> /home/eric/qsub_braincloud/qsub/tests/testo.txt  
      echo "$(cat /home/eric/qsub_braincloud/qsub/tests/test6.txt)" >> /home/eric/qsub_braincloud/qsub/tests/testo.txt  

Each line in mem_file should be an amount of memory or none. IE:  
      
      
      
      
      1MB
      
      

