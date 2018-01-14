import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from scihub.scihub.scihub import SciHub
from scholar import scholar

class MyWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, 
			title="Ugarit",
			default_height=400,
			default_width=500)
		self.set_border_width(3)

		self.wrapper = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(self.wrapper)

		self.searchForm = Gtk.ListBox()
		self.searchForm.set_selection_mode(Gtk.SelectionMode.NONE)
		self.wrapper.pack_start(self.searchForm, True, True, 0)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		labelAuthor = Gtk.Label("Author", xalign=0)
		self.inputAuthor = Gtk.Entry(max_length=20)
		hbox.pack_start(labelAuthor, True, True, 0)
		hbox.pack_start(self.inputAuthor, True, True, 0)
		self.searchForm.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		labelKeyphrase = Gtk.Label("Keyphrase", xalign=0)
		self.inputKeyphrase = Gtk.Entry(max_length=20)
		hbox.pack_start(labelKeyphrase, True, True, 0)
		hbox.pack_start(self.inputKeyphrase, True, True, 0)
		self.searchForm.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hbox)
		sendButton = Gtk.Button.new_with_label("Click Me")
		sendButton.connect("clicked", self.on_submit)
		hbox.pack_start(sendButton, True, True, 0)
		self.searchForm.add(row)


	def on_submit(self, button):
		
		author = self.inputAuthor.get_text()
		keyphrase = self.inputKeyphrase.get_text()
		print("Author: {}".format(author))
		print("Keyphrase: {}".format(keyphrase))

		query = scholar.SearchScholarQuery()
		query.set_author(author)
		query.set_phrase(keyphrase)
		querier.send_query(query)

		scholar.txt(querier, with_globals=True)




querier = scholar.ScholarQuerier()
settings = scholar.ScholarSettings()
settings.set_citation_format(scholar.ScholarSettings.CITFORM_BIBTEX)
querier.apply_settings(settings)

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()