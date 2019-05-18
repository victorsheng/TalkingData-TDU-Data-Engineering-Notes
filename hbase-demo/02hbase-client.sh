docker exec -it hbase-vic /bin/bash

```
hbase shell


create 't1', 'f1', 'f2'

create 't2', {NAME=>'f1', VERSIONS=> 5}

desc 't1'

desc 't2'

list

put 't1' , 'rowkey1' , 'f1:c1','value1,1526200761'
put 't1' , 'rowkey1' , 'f1:c1','value2,1526200762'
put 't1' , 'rowkey1' , 'f1:c1','value3,1526200763'
put 't1' , 'rowkey1' , 'f1:c1','value4,1526200764'
put 't1' , 'rowkey1' , 'f1:c1','value5,1526200765'
put 't1' , 'rowkey1' , 'f1:c1','value6,1526200766'


scan 't1'


get 't1' , 'rowkey1'

get 't1','rowkey1','f1:c1'

get 't1','rowkey1',{COLUMN=>'f1:c1',VERSIONS=>5}

delete 't1','rowkey1','f1:c1',1526200765

disable 't1'

drop 't1'

list

exit

```