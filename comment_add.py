# Add comment to trac
# For trac 1.0
# Based on https://trac.edgewall.org/browser/branches/1.0-stable/tracopt/ticket/commit_updater.py?format=txt
#	https://trac.edgewall.org/wiki/TracDev/PluginDevelopment/ExtensionPoints/trac.admin.api.IAdminCommandProvider#Examples

from __future__ import with_statement

import re

from genshi.builder import tag

from trac.config import BoolOption, Option
from trac.core import Component, implements
from trac.admin import IAdminCommandProvider
from trac.ticket import Ticket
from trac.ticket.notification import TicketNotifyEmail
from trac.util.datefmt import datetime_now, utc
from trac.util.text import exception_to_unicode
from trac.util.text import print_table, printout

class CommentAdminCommandProvider(Component):

	implements(IAdminCommandProvider)

	notify = BoolOption('ticket', 'commit_ticket_update_notify', 'true',
		"""Send ticket change notification when updating a ticket.""")

	def get_admin_commands(self):
		yield ('comment add', '<ticket> <user> <text>',
			   'Add a comment to a ticket',
			   None, self._do_add_comment)

	def _do_add_comment(self, ticket, user, text):
		tickets = {}
		tickets.setdefault(int(ticket), [])
		comment = text.replace('\\n','[[BR]]\n')
		self._update_tickets(tickets, user, comment, datetime_now(utc))

	def _update_tickets(self, tickets, authname, comment, date):
		"""Update the tickets with the given comment."""
		for tkt_id, cmds in tickets.iteritems():
			try:
				self.log.debug("Updating ticket #%d", tkt_id)
				save = False
				with self.env.db_transaction:
					ticket = Ticket(self.env, tkt_id)
					ticket.save_changes(authname, comment, date)
					self._notify(ticket, date)
			except Exception, e:
				self.log.error("Unexpected error while processing ticket "
							   "#%s: %s", tkt_id, exception_to_unicode(e))

	def _notify(self, ticket, date):
		"""Send a ticket update notification."""
		if not self.notify:
			return
		tn = TicketNotifyEmail(self.env)
		try:
			tn.notify(ticket, newticket=False, modtime=date)
		except Exception, e:
			self.log.error("Failure sending notification on change to "
						   "ticket #%s: %s", ticket.id,
						   exception_to_unicode(e))
