from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import *
from wsgiref.util import FileWrapper
import xml.etree.ElementTree as ET
from collections import OrderedDict

# Create your views here.

def index(request):
	return render(request, "upload-file.html")

@require_http_methods(["POST"])
def write(request):
	xmlfile = request.FILES.get("xmlfile")

	strdict = extractStrings(xmlfile.file)

	context = {"strings": strdict, "filename": xmlfile.name}
	return render(request, "write-file.html", context)


def make(request):
	strings = OrderedDict()
	for key, value in request.POST.items():
		if (key[:2] == "__"):
			strkey = key[2:]
			strings[strkey] = value

	xmlResult = writeXMLfile(strings)

	f = open("strings.xml", "w")
	f.write(xmlResult)
	f.close()

	with open("strings.xml", "r") as f:
		response = HttpResponse(FileWrapper(f), content_type='application/xml')
		response['Content-Disposition'] = 'attachment; filename=strings.xml'
		return response

def extractStrings(f):
	e = ET.parse(f).getroot()

	strdict = OrderedDict()
	for string in e.findall('string'):
		current_text = string.text
		index = string.get('name')
		strdict[index] = current_text

	return strdict

def writeXMLfile(strings):
	resources = ET.Element("resources")
	for key, value in strings.items():
		stringrow = ET.SubElement(resources, "string", {"name": key})
		stringrow.text = value

	return ET.tostring(indent(resources), encoding='utf8', method='xml')

def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem
