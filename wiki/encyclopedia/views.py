from django.shortcuts import render
from django import forms
from markdown2 import Markdown
import random
from . import util


# markdown conversion: use python-markdown2 package installed via pip3 install markdown2
marker = Markdown() # usage marker.convert(TARGET)


def index(request):
# update so we can click on each entry and go to its page
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# renders the page of the TITLE entry using get_entry(title)
# if the entry does not exist, display error 
def entry(request, title):
    if title.casefold() in [item.casefold() for item in util.list_entries()]:
        return render(request, "encyclopedia/entry.html", {
            "entry":marker.convert(util.get_entry(title)), # load entry
            "title":title
        })
    else: # marker broke our error handling above so we have this instead # ugly and redundant :(
        return render(request, "encyclopedia/entry.html", {
            "entry":util.get_entry(title), # get empty entry to show error on entry.html
            "title":title
        })


# search box in sidebar should find entries that match, else partially match e.g. py -> python
# search results page: if q in util.list_entries show entry
def search(request):
    q = request.GET.get('q').casefold()
    allwiki = [item.casefold() for item in util.list_entries()]
    results = []
    if q in allwiki: # whole match
        return entry(request, q)
    else: # find partial match
        for pagename in allwiki: # search for substrings
            if q in pagename: # if substring matches
                results.append(pagename) # add to results list
        return render(request, "encyclopedia/search.html", {"results":results}) # if no matches, results will be an empty list which gets error on search.html


# create new page: title, content textarea, save button. if title conflicts, error. on save, display the page.
class NewEntryForm(forms.Form):
    newtitle = forms.CharField(widget=forms.TextInput, label="Title")
    newentry = forms.CharField(widget=forms.Textarea, label="Content")

def new(request):
    if request.method == "GET": # show the new entry page
        return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
        }) 
    else: # when user submits the form
        form = NewEntryForm(request.POST) # fill the form with submitted data
        if form.is_valid():
            newentry = form.cleaned_data["newentry"]
            newtitle = form.cleaned_data["newtitle"]
            if newtitle not in util.list_entries(): # check for existing entry
                util.save_entry(newtitle, newentry) # save the new entry 
                return entry(request, newtitle) # go to the new page
            else: # error entry already exists
                return render(request, "encyclopedia/error.html")


# edit entry: click edit from an entry page, go to edit page textarea initialized with the entry content
class EditEntryForm(forms.Form):
    editentry = forms.CharField(widget=forms.Textarea, label="Edit") 

def edit(request, title):
    if request.method == "GET": # load the edit page
        initial = {"editentry":util.get_entry(title)}
        return render(request, "encyclopedia/edit.html", {
        "entry": util.get_entry(title),
        "title": title,
        "form": EditEntryForm(initial=initial) # prefill the form
        })
    else: # save changes
        form = EditEntryForm(request.POST)
        if form.is_valid():
            editentry = form.cleaned_data["editentry"]
            util.save_entry(title, editentry) 
            return entry(request, title) # go back to the entry page


# random page link
def randompage(request):
    allpages = util.list_entries()
    n = random.randrange(len(allpages))
    title = allpages[n]
    return entry(request, title)
