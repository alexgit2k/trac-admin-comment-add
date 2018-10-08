Trac-admin comment add plugin for trac
======================================

Adds function for trac-admin to add comments to tickets.

The code is based on tracopt/ticket/commit_updater.py of trac.

## Install

Install the plugin into your trac project's plugins dir. To enable the plugin
add this to the trac.ini file:

	[components]
	comment_add.* = enabled

## Usage

Syntax: <code>trac-admin <project-path> comment add <ticket> <user> <text></code><br />
Example: <code>trac-admin /home/trac comment add 12345 'name <email@example.com>' 'Hello World!\nThis is a comment'</code>
