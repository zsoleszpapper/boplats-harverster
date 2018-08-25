#!/usr/bin/awk -f

{
  last[$1] = $0;
}

END {
  for (x in last)
    print last[x]
}
