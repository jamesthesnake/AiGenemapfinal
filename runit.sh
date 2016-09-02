#/bin/bash
for x in 1,2,3,4,5,6,7,8
do
echo "Running Test $x"
echo | python geneticmap.py 50*$x 0.5*$x ;
echo "Test $x complete"
done
