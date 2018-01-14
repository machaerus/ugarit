import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from scihub.scihub.scihub import SciHub
from scholar import scholar

class MyWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, 
			title="Ugarit")
		self.set_border_width(3)

		self.selected = {}

		self.wrapper = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(self.wrapper)
	
		self.searchForm = Gtk.ListBox()
		# self.searchForm.set_margin_top(5)
		self.searchForm.set_selection_mode(Gtk.SelectionMode.NONE)
		self.searchForm.set_vexpand(False)
		self.wrapper.pack_start(self.searchForm, True, True, 0)
		
		# SEARCH FORM
		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		row.add(hbox)
		labelAuthor = Gtk.Label("Author", xalign=0)
		self.inputAuthor = Gtk.Entry()
		# self.inputAuthor.set_width_chars(30)
		hbox.pack_start(labelAuthor, True, True, 0)
		hbox.pack_start(self.inputAuthor, True, True, 0)
		self.searchForm.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		row.add(hbox)
		labelKeyphrase = Gtk.Label("Keyphrase", xalign=0)
		self.inputKeyphrase = Gtk.Entry()
		# self.inputKeyphrase.set_width_chars(30)
		hbox.pack_start(labelKeyphrase, True, True, 0)
		hbox.pack_start(self.inputKeyphrase, True, True, 0)
		self.searchForm.add(row)

		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		row.add(hbox)
		sendButton = Gtk.Button.new_with_label("Search")
		sendButton.connect("clicked", self.on_submit)
		sendButton.set_halign(Gtk.Align.END)
		hbox.pack_start(sendButton, True, True, 0)
		self.searchForm.add(row)
		# END SEARCH FORM

		# MODEL
		# author, title, date
		self.articleListStore = Gtk.ListStore(str, str, str)
		self.articleListStore.append(["Test", "Test", "2018"])

		# VIEW
		self.resultList = Gtk.TreeView(self.articleListStore)
		self.resultList.set_vexpand(True)
		self.resultList.set_size_request(-1, 300)
		for i, column_title in enumerate(["Author", "Title", "Date"]):
			renderer = Gtk.CellRendererText()
			renderer.set_fixed_size(300, 30)
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			column.set_resizable(True)
			column.set_min_width(200)
			column.set_max_width(400)
			self.resultList.append_column(column)
		self.wrapper.pack_start(self.resultList, True, True, 0)

		self.resultSelect = self.resultList.get_selection()
		self.resultSelect.connect("changed", self.on_tree_selection_changed)

		# BUTTONS FOR LIST CONTROL

		listControls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
		listControls.set_vexpand(False)
		listControls.set_valign(Gtk.Align.START)

		buttonDownload = Gtk.Button.new_with_label("Download")
		buttonDownload.connect("clicked", self.on_click_download)
		buttonDownload.set_hexpand(False)
		buttonDownload.set_vexpand(False)
		buttonDownload.set_halign(Gtk.Align.START)
		buttonDownload.set_valign(Gtk.Align.START)
		listControls.pack_start(buttonDownload, True, True, 0)

		buttonCitation = Gtk.Button.new_with_label("BibTeX")
		buttonCitation.connect("clicked", self.on_click_citation)
		buttonCitation.set_hexpand(False)
		buttonCitation.set_vexpand(False)
		buttonCitation.set_halign(Gtk.Align.START)
		buttonCitation.set_valign(Gtk.Align.START)
		listControls.pack_start(buttonCitation, True, True, 0)

		buttonClose = Gtk.Button.new_with_label("Close")
		buttonClose.connect("clicked", self.on_click_close)
		buttonClose.set_hexpand(False)
		buttonClose.set_vexpand(False)
		buttonClose.set_halign(Gtk.Align.START)
		buttonClose.set_valign(Gtk.Align.START)
		listControls.pack_start(buttonClose, True, True, 0)

		self.wrapper.pack_start(listControls, True, True, 0)


	def on_tree_selection_changed(self, selection):
		model, treeiter = selection.get_selected()
		self.selected = {
			"author": model[treeiter][0],
			"title": model[treeiter][1],
			"year": model[treeiter][2]
		}

	def on_click_download(self, button):
		if self.selected == {}:
			print("Nothing selected")
		else:
			print("Trying to download article: {}".format(self.selected['title']))

	def on_click_citation(self, button):
		if self.selected == {}:
			print("Nothing selected")
		else:
			print("Looking for citation for article: {}".format(self.selected['title']))

	def on_click_close(self, button):
		print("Closing application")
		Gtk.main_quit()


	def on_submit(self, button):
		
		author = self.inputAuthor.get_text()
		keyphrase = self.inputKeyphrase.get_text()
		print("Author: {}".format(author))
		print("Keyphrase: {}".format(keyphrase))

		query = scholar.SearchScholarQuery()
		query.set_author(author)
		query.set_phrase(keyphrase)
		query.set_num_page_results(10)
		querier.send_query(query)

		print(scholar.txt(querier, with_globals=False))
		self.results = scholar.json(querier)

		self.articleListStore.clear()
		for article in self.results:
			self.articleListStore.append([
				", ".join(article['authors']),
				article['title'],
				article['year']
			])




querier = scholar.ScholarQuerier()
# settings = scholar.ScholarSettings()
# settings.set_citation_format(scholar.ScholarSettings.CITFORM_BIBTEX)
# querier.apply_settings(settings)

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()