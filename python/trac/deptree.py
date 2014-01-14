from collections import Counter
import re
from trac import TracProxy, WrongServer
import xmlrpclib

class Ticket(object):
    "A ticket that may have dependencies"

    def __init__(self, num, proxy):
        self.proxy = proxy
        self.num = num
        self.refresh()

    def refresh(self):
        "Refresh with data from trac"
        _, _, _, ticket = self.proxy.ticket.get( self.num )
        desc = self.desc = ticket["description"]
        reg = self._construct_regex()

        self.deps = []

        r = reg.match( desc )
        if r is None:
            "Ticket has no dependencies"
            self.prelude = desc
            self.deptitle = ""
            self.depspace = ""
            self.deplist = ""
            self.postscript = ""
            self.deplist_ends_in_newline = False
            self.list_prefix = ""
            return

        self.prelude = r.group("prelude")
        self.deptitle = r.group("deptitle")
        self.depspace = r.group("depspace")
        self.deplist = r.group("deplist")
        self.postscript = r.group("postscript")

        spacings = Counter()
        
        for asterisk, ticket_num, desc in  re.findall( r"^(\s*\*\s*)#([0-9]+)\s*(.*)$",
                                                       self.deplist,
                                                       re.MULTILINE | re.IGNORECASE ):
            spacings.update( [asterisk] )
            self.deps.append( int(ticket_num) )

        self.list_prefix = spacings.most_common(1)[0][0]
        self.deplist_ends_in_newline = (self.deplist[-1] == "\n")

    def cleanup(self, dry_run = False):
        "Clean-up the ticket's description"

        # Rebuild the deplist:
        d = self.prelude + self.deptitle + self.depspace

        for i, ticket_num in enumerate(self.deps):
            _, _, _, dep = self.proxy.ticket.get(ticket_num)

            d += "{prefix}#{num} {summary}".format( prefix = self.list_prefix,
                                                    num = ticket_num,
                                                    summary = dep["summary"] )

            if i != len(self.deps)-1 or self.deplist_ends_in_newline:
                d += "\n"

        d += self.postscript

        if d == self.desc:
            "Description has not changed"
            return False

        if not dry_run:
            self.proxy.ticket.update( self.num,
                                      "Synchronise dependency summaries with dependencies (automated edit).",
                                      { "description": d } )

        self.refresh()
        return True

    def _construct_regex(self):
        # Construct a regexp for splitting dependencies from the prelude
        # Prelude section:
        reg = r"(?P<prelude>.*)"

        # Dependencies line
        reg += r"(?P<deptitle>^Dependencies:?$)"

        # Possible newlines between dependencies line and dependency list
        reg += r"(?P<depspace>\s*\n)?"

        # Dependency list:
        reg += r"(?P<deplist>(^\s*\*[^\n]+($\n|\Z))*)"

        # Postscript after the dependency list:
        reg += r"(?P<postscript>.*)"

        return re.compile( reg,
                           re.MULTILINE | re.IGNORECASE | re.DOTALL )
