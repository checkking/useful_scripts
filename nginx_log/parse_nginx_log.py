#!/usr/bin/python
import re
import sys
reload(sys)

conf = '$remote_addr - - [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$proxy_ip"'
regex = ''.join('(?P<' + g + '>.*?)' if g else re.escape(c) for g, c in re.findall(r'\$(\w+)|(.)', conf))

if __name__ == "__main__":
    for line in sys.stdin:
        m = re.match(regex, line.strip())
        if m:
            dict = m.groupdict()
            print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                    (dict['remote_addr'], \
                    dict['time_local'], \
                    dict['request'],\
                    dict['status'], \
                    dict['body_bytes_sent'],\
                    dict['http_referer'],\
                    dict['http_user_agent'], \
                    dict['proxy_ip']))
